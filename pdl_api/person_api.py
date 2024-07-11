from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Hashable, Optional, TypeVar

from peopledatalabs import PDLPY  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict

from pdl_api.models.exceptions import PDLAccountLimitException, PDLUnknownException
from pdl_api.models.response import Response


class APIType(StrEnum):
    ENRICH = "enrich"
    SEARCH = "search"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


T = TypeVar("T", bound="PDLSettings")


class PDLSettings(BaseSettings):
    api_key: str = ""

    query_type: APIType = APIType.ENRICH

    model_config = SettingsConfigDict(env_prefix="pdl_")

def param_hash(d: dict | list | Hashable) -> int:
    """Convert dict/lists/primitives to a hash"""
    if isinstance(d, dict):
        items = sorted((key, param_hash(value)) for key, value in d.items())
        return hash(frozenset(items))
    # Convert lists to tuples of hashed elements
    elif isinstance(d, list):
        t = tuple(param_hash(item) for item in d)
        return hash(t)
    # For other types, use the default hash value
    else:
        return hash(d)


@dataclass
class PDLPersonAPI:
    settings: PDLSettings = field(default_factory=PDLSettings)

    ## Temporary cache for the queries to avoid repeated calls
    existing_queries: dict[int, Response] = field(default_factory=dict)

    ## PDL API client
    client: Optional[PDLPY] = None

    ## initialize the client with these kwargs
    init_kwargs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.client is None:
            self.client = PDLPY(api_key=self.settings.api_key, **self.init_kwargs)
    
    def save_queries(self, queries: dict[int, Response]):
        for hsh, r in queries.items():
            self.existing_queries[hsh] = r

    def find_existing_queries(
        self,
        params: dict[str, Any],
        limit: Optional[int] = None,
        only_person: Optional[bool] = None,
        **kwargs,
    ):
        """Find existing queries"""
        matches = []
        hsh = param_hash(params)
        if hsh in self.existing_queries:
            matches.append(self.existing_queries[hsh])
        if limit and len(matches) >= limit:
            return matches
        for key, list_values in params.items():
            for pr in self.existing_queries.values():
                if only_person:  ## We either want only people or only errors
                    ## skip if not a person
                    if only_person and pr.is_error:
                        continue
                    ## skip if not an error
                    if not only_person and pr.is_person:
                        continue
                person = pr.person
                if not person:
                    continue
                emails = person.get_emails()
                for email in emails:
                    for val in list_values:
                        if key == "email" and val == email.address:
                            if not pr.query:
                                print(f"Found {email.address} in {list_values} {pr.query}")
                                pr.query = {"email": val}
                                # save
                                self.save_queries({hsh: pr})
                            return [pr]

                pr_email = pr.query.get("email")
                if isinstance(pr_email, list):
                    pr_email = pr_email[0]

                match = True
                for val in list_values:
                    if key == "email" and pr_email and val == pr_email:
                        break
                else:
                    match = False
                if match:
                    matches.append(pr)
                    if limit and len(matches) >= limit:
                        return matches
        return matches

    def find_existing_query(self, params: dict[str, Any], **kwargs) -> Optional[Response]:
        """Find an existing person in the existing people"""
        l = self.find_existing_queries(params=params, limit=1, **kwargs)
        return l[0] if l else None

    def get_person_via_email(self, email: str) -> Response:
        return self.get_person(params={"email": [email]})

    def _get_response(self, params: dict[str, Any]) -> dict[str, Any]:
        if not self.client:
            raise ValueError("PDLPersonAPI: Client not initialized")
        if self.settings.query_type == APIType.ENRICH:
            return self.client.person.enrichment(**params).json()
        else:
            return self.client.person.search(**params).json()

    def get_person(self, params: dict[str, Any], use_cache: bool = True, **find_kwargs) -> Response:
        """Get a person from the API, while the api
        can take multiple this function is only for 1"""

        hsh = param_hash(params)

        if use_cache:
            existing = self.find_existing_query(params=params, **find_kwargs)
            ## remove existing people from params
            if existing:
                return existing

        json_response = self._get_response(params)
        status = json_response["status"]
        if status != 200:
            msg = json_response.get("error",{}).get("message", "")
            if status == 402:
                raise PDLAccountLimitException(json_response, msg)
            error_type = json_response.get("error", {}).get("type", None)
            if status == 404 and error_type != "not_found":
                ## If it's "not_found", do an ErrorResponse as normal, but otherwise
                ## raise an error
                raise PDLUnknownException(json_response, msg)

            pr = Response(query=params, **json_response)
            self.existing_queries[hsh] = pr
        else:
            pr = Response(query=params, **json_response)

        if use_cache:
            self.save_queries({hsh: pr})

        return pr

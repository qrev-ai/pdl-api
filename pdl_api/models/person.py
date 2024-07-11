from typing import Any, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    address_line_2: Optional[str] = Field(
        None, description="The street address line 2 of the company HQ address"
    )
    continent: Optional[str] = Field(default=None, description="The continent the company HQ is in")
    country: Optional[str] = Field(default=None, description="The country the company HQ is in")
    geo: Optional[str] = Field(
        None,
        description="City-center geo code of the company HQ, in the format 'latitude, longitude'",
    )
    locality: Optional[str] = Field(default=None, description="The locality the company HQ is in")
    metro: Optional[str] = Field(default=None, description="The metro area the company HQ is in")
    name: Optional[str] = Field(
        None,
        description="Our cleaned values for the company HQ location in the format 'locality, region, country'",
    )
    postal_code: Optional[str] = Field(
        None, description="The postal code of the company HQ address"
    )
    region: Optional[str] = Field(default=None, description="The region the company HQ is in")
    street_address: Optional[str] = Field(
        default=None, description="The street address of the company HQ"
    )


class Certification(BaseModel):
    end_date: Optional[str] = Field(
        default=None, description="The expiration date of the certification"
    )
    name: Optional[str] = Field(default=None, description="Certification name")
    organization: Optional[str] = Field(
        None, description="The organization awarding the certification"
    )
    start_date: Optional[str] = Field(
        default=None, description="The date the certification was awarded"
    )


class EducationSchool(BaseModel):
    domain: Optional[str] = Field(
        None, description="The primary website domain associated with the school"
    )
    facebook_url: Optional[str] = Field(default=None, description="The school's Facebook URL")
    id: Optional[str] = Field(
        None, description="The non-persistent ID for the school in our records"
    )
    linkedin_id: Optional[str] = Field(default=None, description="The school's LinkedIn ID")
    linkedin_url: Optional[str] = Field(default=None, description="The school's LinkedIn URL")
    location: Optional[Location] = Field(default=None, description="The location of the school")
    name: Optional[str] = Field(default=None, description="The name of the school")
    raw: Optional[list[str]] = Field(default=None, description="Raw school name")
    twitter_url: Optional[str] = Field(default=None, description="The school's Twitter URL")
    type: Optional[str] = Field(default=None, description="The school type")
    website: Optional[str] = Field(
        default=None, description="The website URL associated with the school"
    )


class Education(BaseModel):
    degrees: Optional[list[str]] = Field(
        None, description="The degrees the person earned at the school"
    )
    end_date: Optional[str] = Field(default=None, description="The date the person left the school")
    gpa: Optional[float] = Field(
        default=None, description="The GPA the person earned at the school"
    )
    majors: Optional[list[str]] = Field(
        None, description="All majors the person earned at the school"
    )
    minors: Optional[list[str]] = Field(
        None, description="All minors the person earned at the school"
    )
    raw: Optional[list[str]] = Field(default=None, description="Raw education data")
    school: Optional[str | EducationSchool] = Field(
        None, description="The school the person attended"
    )
    start_date: Optional[str] = Field(
        default=None, description="The date the person started at the school"
    )
    summary: Optional[str] = Field(
        default=None, description="User-inputted summary of their education"
    )


class Email(BaseModel):
    address: Optional[str] = Field(default=None, description="The fully parsed email address")
    first_seen: Optional[str] = Field(
        default=None, description="The date that this entity was first associated with the Person record"
    )
    last_seen: Optional[str] = Field(
        default=None, description="The date that this entity was last associated with the Person record"
    )
    num_sources: Optional[int] = Field(
        default=None,
        description="The number of sources that have contributed to the association of this entity with the Person record",
    )
    type: Optional[str] = Field(default=None, description="The type of email")

    def __str__(self) -> str:
        first_seen = self.first_seen if self.first_seen else ""
        last_seen = self.last_seen if self.last_seen else ""
        date_range = f"{first_seen} - {last_seen}" if first_seen or last_seen else ""
        return f"{self.address} ({self.type} {date_range})"

class Company(BaseModel):
    facebook_url: Optional[str] = Field(default=None, description="The company's Facebook URL")
    founded: Optional[int] = Field(default=None, description="The founding year of the company")
    id: Optional[str] = Field(default=None, description="The company's PDL ID")
    industry: Optional[str] = Field(
        default=None, description="The self-identified industry of the company"
    )
    linkedin_id: Optional[str] = Field(default=None, description="The company's LinkedIn ID")
    linkedin_url: Optional[str] = Field(default=None, description="The company's LinkedIn URL")
    location: Optional[Location] = Field(
        default=None, description="The location of the company's headquarters"
    )
    name: Optional[str] = Field(
        default=None, description="The company name, cleaned and standardized"
    )
    raw: Optional[list[str]] = Field(default=None, description="Raw company name")
    size: Optional[str] = Field(default=None, description="The self-reported company size range")
    ticker: Optional[str] = Field(default=None, description="The company ticker")
    twitter_url: Optional[str] = Field(default=None, description="The company's Twitter URL")
    type: Optional[str] = Field(default=None, description="The company type")
    website: Optional[str] = Field(
        default=None, description="The company's primary website, cleaned and standardized"
    )


class ExperienceTitle(BaseModel):
    levels: Optional[list[str]] = Field(default=None, description="The level(s) of the job title")
    name: Optional[str] = Field(default=None, description="The cleaned job title")
    raw: Optional[list[str]] = Field(default=None, description="Raw job title input")
    role: Optional[str] = Field(default=None, description="One of the Canonical Job Roles")
    sub_role: Optional[str] = Field(default=None, description="One of the Canonical Job Sub Roles")


class Experience(BaseModel):
    company: Optional[Company] = Field(
        default=None, description="The company where the person worked"
    )
    start_date: Optional[str] = Field(
        default=None, description="The date the person started at the company"
    )
    end_date: Optional[str] = Field(
        default=None, description="The date the person left the company"
    )
    first_seen: Optional[str] = Field(
        default=None, description="The date that this entity was first associated with the Person record"
    )
    is_primary: Optional[bool] = Field(
        default=None, description="Whether this is the person's current job or not"
    )
    last_seen: Optional[str] = Field(
        default=None, description="The date that this entity was last associated with the Person record"
    )
    location_names: Optional[list[str]] = Field(
        default=None,
        description="Locations where the person has worked while with this company (if different from the company HQ)",
    )
    num_sources: Optional[int] = Field(
        default=None,
        description="The number of sources that have contributed to the association of this entity with the Person record",
    )
    summary: Optional[str] = Field(
        default=None, description="User-inputted summary of their work experience"
    )
    title: Optional[ExperienceTitle] = Field(
        default=None, description="The person's job title while at the company"
    )


class Person(BaseModel):
    birth_date: Optional[str] = Field(default=None, description="The day the person was born")
    birth_year: Optional[int] = Field(default=None, description="The year the person was born")
    certifications: Optional[list[Certification]] = Field(
        default=None, description="Any certifications the person has"
    )
    countries: Optional[list[str]] = Field(
        default=None, description="All countries associated with the person"
    )
    education: Optional[list[Education]] = Field(
        default=None, description="The person's education information"
    )
    emails: Optional[list[Email]] = Field(
        default=None, description="Email addresses associated with the person"
    )
    experience: Optional[list[Experience]] = Field(
        default=None, description="The person's work experience"
    )
    facebook_friends: Optional[int] = Field(
        default=None, description="The number of Facebook friends the person has"
    )
    facebook_id: Optional[str] = Field(
        default=None, description="The person's Facebook profile ID based on source agreement"
    )
    facebook_url: Optional[str] = Field(
        default=None, description="The person's Facebook profile URL based on source agreement"
    )
    facebook_username: Optional[str] = Field(
        default=None, description="The person's Facebook profile username based on source agreement"
    )
    first_name: Optional[str] = Field(default=None, description="The person's first name")
    first_seen: Optional[str] = Field(
        default=None, description="The date when this record was first created in our data"
    )
    full_name: Optional[str] = Field(default=None, description="The person's full name")
    sex: Optional[str] = Field(default=None, description="The person's sex")
    github_url: Optional[str] = Field(
        default=None, description="The person's GitHub profile URL based on source agreement"
    )
    github_username: Optional[str] = Field(
        default=None, description="The person's GitHub profile username based on source agreement"
    )
    id: str = Field(default=None, description="A unique persistent identifier for the person")
    industry: Optional[str] = Field(
        default=None, description="The most relevant industry for this person based on their work history"
    )

    def get_emails(
        self,
        filter: Optional[dict[str, Any]] = None,
        sort_by_last_seen: bool = True,
        reverse: bool = True,
    ) -> list[Email]:
        """
        Get the emails of the person.
        Args:
            sort_by_start_date (bool): Sort the emails by start date
            reverse (bool): Reverse the order of the emails
        Returns:
            list[Email]: The emails of the person
        """
        if not self.emails:
            return []
        l = self.emails.copy()
        if filter is not None:
            l = [
                email
                for email in l
                if all(getattr(email, key) == value for key, value in filter.items())
            ]

        if sort_by_last_seen:
            return sorted(l, key=lambda x: str(x.last_seen) if x.last_seen else str(0), reverse=reverse)
        return l

    def get_experiences(
        self, sort_by_start_date: bool = True, reverse: bool = True
    ) -> list[Experience]:
        """Get the experiences of the person.
        Args:
            sort_by_start_date (bool): Sort the experiences by start date
            reverse (bool): Reverse the order of the experiences
        Returns:
            list[Experience]: The experiences of the person
        """
        if not self.experience:
            return []
        if sort_by_start_date:
            return sorted(
                self.experience, key=lambda x: str(x.start_date) if x.start_date else str(0), reverse=reverse
            )
        return self.experience

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from enum import Enum


class NotificationMessageBody(BaseModel):
    message_type: str
    message_issue_date: datetime
    message_id: str
    disclaimer: Optional[str]
    summary: Optional[str]
    notes: Optional[str]


parsed_and_cleaned_message_body_dict = {
    "message_type": "Space Weather Notification - Radiation Belt Enhancement",
    "message_issue_date": "2020-10-07T17:18:51Z",
    "message_id": "20201007-AL-001",
    "disclaimer": "NOAA's Space Weather Prediction Center (http://swpc.noaa.gov) is the United States Government official source for space weather forecasts. This \"Experimental Research Information\" consists of preliminary NASA research products and should be interpreted and used accordingly.",
    "summary": "Significantly elevated energetic electron fluxes in the Earth's outer radiation belt. GOES \"greater than 2.0 MeV\" integral electron flux is above 1000 pfu starting at 2020-10-07T14:05Z. The elevated energetic electron flux levels are caused by an S-type CME with ID 2020-09-30T12:09:00-CME-001. NASA spacecraft at GEO, MEO and other orbits passing through or in the vicinity of the Earth's outer radiation belt can be impacted. Activity ID: 2020-10-07T14:05:00-RBE-001."
}

print(
    NotificationMessageBody(
        **parsed_and_cleaned_message_body_dict
    ).json()
)


class MessageTypeAbbreviationEnum(str, Enum):
    FLR = "FLR"
    SEP = "SEP"
    CME = "CME"
    IPS = "IPS"
    MPC = "MPC"
    GST = "GST"
    RBE = "RBE"
    Report = "Report"


class NotificationMessage(BaseModel):
    insertion_date: datetime
    message_type_abbreviation: MessageTypeAbbreviationEnum
    message_url: HttpUrl
    message_body: NotificationMessageBody

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


parsed_and_cleaned_message_body_dict = {
    "message_type": "Space Weather Notification - Radiation Belt Enhancement",
    "message_issue_date": "2020-10-07T17:18:51Z",
    "message_id": "20201007-AL-001",
    "disclaimer": "NOAA's Space Weather Prediction Center (http://swpc.noaa.gov) is the United States Government official source for space weather forecasts. This \"Experimental Research Information\" consists of preliminary NASA research products and should be interpreted and used accordingly.",
    "summary": "Significantly elevated energetic electron fluxes in the Earth's outer radiation belt. GOES \"greater than 2.0 MeV\" integral electron flux is above 1000 pfu starting at 2020-10-07T14:05Z. The elevated energetic electron flux levels are caused by an S-type CME with ID 2020-09-30T12:09:00-CME-001. NASA spacecraft at GEO, MEO and other orbits passing through or in the vicinity of the Earth's outer radiation belt can be impacted. Activity ID: 2020-10-07T14:05:00-RBE-001."
}

parsed_and_cleaned_notification_message_dict = {
    "insertion_date": "2020-12-15T20:08:23.091Z",
    "message_type_abbreviation": "RBE",
    "message_url": "https://kauai.ccmc.gsfc.nasa.gov/DONKI/view/Alert/15920/1",
    "message_body": parsed_and_cleaned_message_body_dict
}

print(
    NotificationMessage(
        **parsed_and_cleaned_notification_message_dict
    ).model_dump_json()
)
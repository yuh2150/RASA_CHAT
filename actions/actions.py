
import logging
import json
import pytz

from typing import Any, Dict, List, Text, Optional
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)


class ActionCurrentTime(Action):
    def name(self) -> Text:
        return "action_current_time"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the current time in UTC.
        now_utc = datetime.now(pytz.utc)
        
        # Format the time in ISO 8601 format
        current_time_iso = now_utc.isoformat(timespec='milliseconds')
        
        # Send the formatted time to the user
        dispatcher.utter_message(text=f"The current time is {current_time_iso}")
        
        return []

class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the current time in UTC.
        
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_message(response="utter_greet_name", name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_message(response="utter_greet_noname")
                return []
            else:
                dispatcher.utter_message(response="utter_greet")
                # dispatcher.utter_message(response="utter_inform_privacypolicy")
                return [SlotSet("shown_privacy", True)]
        return []

# class ActionSubmitBookForm(Action):
#     def name(self) -> Text:
#         return "action_submit_book_ride_form"
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> List[EventType]:
#         """Once we have all the information, attempt to add it to the
#         Google Drive database"""

#         import datetime

#         budget = tracker.get_slot("budget")
#         company = tracker.get_slot("company")
#         email = tracker.get_slot("business_email")
#         job_function = tracker.get_slot("job_function")
#         person_name = tracker.get_slot("person_name")
#         use_case = tracker.get_slot("use_case")
#         date = datetime.datetime.now().strftime("%d/%m/%Y")

#         sales_info = [company, use_case, budget, date, person_name, job_function, email]

#         try:
#             gdrive = GDriveService()
#             gdrive.append_row(
#                 gdrive.SALES_SPREADSHEET_NAME, gdrive.SALES_WORKSHEET_NAME, sales_info
#             )
#             dispatcher.utter_message(template="utter_confirm_salesrequest")
#             return []
#         except Exception as e:
#             logger.error(
#                 f"Failed to write data to gdocs. Error: {e.message}",
#                 exc_info=True,
#             )
#             dispatcher.utter_message(template="utter_salesrequest_failed")
#             return []    
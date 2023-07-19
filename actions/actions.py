from typing import Dict, Text, Any, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.types import DomainDict

from fuzzywuzzy import process
#import actions.weather

# subject_map = {'children education advance':'CHEA','training need assesssment':'TNA','multi-purpose advance':'MPA'}
class ActionSender(Action):
    def name(self) -> Text:
        return "action_sender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            sender_name=tracker.sender_id
            print(sender_name)
            return [SlotSet("user",sender_name)]    

class ActionSubjectCheck(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_subject_check"

    # # validate user answers
    # @staticmethod
    # def subject_db() -> Dict[str, List]:
    #     """Database of multiple choice answers"""
    #     return {
    #         "subject": ["children education advance", "training need assessment", "multi-purpose advance","tna"],
    #         "subject_short": ['chea','tna','mpa']
    #     }


    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
        """Validate user input."""
        slot_value = tracker.get_slot('subject')
        if slot_value.lower() not in domain['slots']['subject_cat']['values']:
            # find the closest answer by some measure (edit distance?)
            choices = domain['slots']['subject_cat']['values']
            answer = process.extractOne(slot_value.lower(), choices)
            # check to see if distnace is greater than some threshold
            if answer[1] < 70:
                # if so, set slot to "other"
                # dispatcher.utter_message("please reframe your query")
                return [SlotSet("subject_cat",None)]
            else:
                return [SlotSet("subject_cat", answer[0])]
        else:
            return [SlotSet("subject_cat",slot_value.lower())]



    # create validation functions for each of our questions
    # validate_subject = create_validation_function(name_of_slot="subject")
    
# class FAQProcessResponse(Action):
#     """Detect the users dialect"""

#     def name(self) -> Text:
#         """Unique identifier of the action"""

#         return "FAQ_process_response"

#     def run(self, dispatcher, tracker, domain):
#         """get dialect classification """
#         # let user know the analysis is running
#         # dispatcher.utter_message(template="utter_working_on_it")

#         # get information from the form & format it
#         # for encoding
#         if tracker.get_slot("subject")=="CHEA":
#             print("CHEA")
#         else:
#             print("Not CHEA")

class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]

# class ActionRestarted(Action): 	
#     def name(self): 		
#         return 'action_restarted' 	
#     def run(self, dispatcher, tracker, domain): 
#         return[Restarted()] 

subject2_map = ['accomodation charges, hotel','payscale','travel allownace']

class ActionSubject2Check(Action):
    """Validating our form input using
    multiple choice answers from Harvard
    Dialect Study"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_subject2_check"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
        """Validate user input."""
        slot_value = tracker.get_slot('subject2')
        if isinstance(slot_value, str):
            if (slot_value.lower() not in subject2_map):
                # find the closest answer by some measure (edit distance?)
                answer = process.extractOne(slot_value.lower(),subject2_map)
                # check to see if distnace is greater than some threshold
                if answer[1] < 60:
                    # if so, set slot to "other"
                    # dispatcher.utter_message("please reframe your query")
                    return [SlotSet("subject2",None)]
                else:
                    return [SlotSet("subject2", answer[0])]
            else:
                return [SlotSet("subject2",slot_value.lower())]

class ActionLevelCheck(Action):
    """Validating our form input using
    multiple choice answers from Harvard
    Dialect Study"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_level_check"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
        """Validate user input."""
        slot_value = tracker.get_slot('level')
        if slot_value.lower() not in domain['slots']['level_cat']['values']:
            # find the closest answer by some measure (edit distance?)
            choices = domain['slots']['level_cat']['values']
            answer = process.extractOne(slot_value.lower(), choices)
            # check to see if distnace is greater than some threshold
            if answer[1] < 70:
                # if so, set slot to "other"
                # dispatcher.utter_message("please reframe your query")
                return [SlotSet("level_cat",None)]
            else:
                return [SlotSet("level_cat", answer[0])]
        else:
            return [SlotSet("level_cat",slot_value.lower())]

tables={'payscale': {'board level': {'CMD': '200000-370000',
   'Functional Director': '180000-340000'},
  'executives': {'E9': '150000-300000',
   'E8': '120000-280000',
   'E7': '100000-260000',
   'E6': '90000-240000',
   'E5': '80000-220000',
   'E4': '70000-200000',
   'E3': '60000-180000',
   'E2': '50000-160000'},
  'supervisors': {'SSG': '29000 - 119500',
   'S4': '28000 - 119000',
   'S3': '27000 - 118500',
   'S2': '26000 - 118000',
   'S1': '25000 - 117500'},
  'workmen': {'WSG': '29000 - 119500',
   'W11': '28000 - 119000',
   'W10': '27000 - 118500',
   'W9': '26000 - 118000',
   'W8': '25000 - 117500',
   'W7': '24000 - 108000',
   'W6': '23000 - 105000',
   'W5': '22500 - 100000',
   'W4': '22000 - 85000',
   'W3': '21500 - 74000',
   'W2': '21000 - 72000',
   'W1': '20500 - 68000',
   'W0': '20000 - 57500'}},
 'accomodation charges, hotel': {'board level': {'CMD': {'Principal Cities and State/UT capitals': 'Boarding & Lodging as per actual',
    'Other Principal Cities': 'Boarding & Lodging as per actual',
    'Oridnary Cities': 'Boarding & Lodging as per actual'},
   'Functional Director': {'Principal Cities and State/UT capitals': 'Boarding & Lodging as per actual',
    'Other Principal Cities': 'Boarding & Lodging as per actual',
    'Oridnary Cities': 'Boarding & Lodging as per actual'}},
  'executives': {'E9': {'Principal Cities and State/UT capitals': '14000',
    'Other Principal Cities': '11000',
    'Oridnary Cities': '8800'},
   'E8': {'Principal Cities and State/UT capitals': '9800',
    'Other Principal Cities': '7700',
    'Oridnary Cities': '6160'},
   'E7': {'Principal Cities and State/UT capitals': '5600',
    'Other Principal Cities': '4400',
    'Oridnary Cities': '3520'},
   'E6': {'Principal Cities and State/UT capitals': '5600',
    'Other Principal Cities': '4400',
    'Oridnary Cities': '3520'},
   'E5': {'Principal Cities and State/UT capitals': '4200',
    'Other Principal Cities': '3300',
    'Oridnary Cities': '2640'},
   'E4': {'Principal Cities and State/UT capitals': '4200',
    'Other Principal Cities': '3300',
    'Oridnary Cities': '2640'},
   'E3': {'Principal Cities and State/UT capitals': '3150',
    'Other Principal Cities': '2475',
    'Oridnary Cities': '1980'},
   'E2': {'Principal Cities and State/UT capitals': '3150',
    'Other Principal Cities': '2475',
    'Oridnary Cities': '1980'}},
  'supervisors': {'SSG': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S4': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S3': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S2': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S1': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'}},
  'workmen': {'WSG': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W11': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W10': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W9': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W8': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W7': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W6': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W5': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W4': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W3': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W2': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W1': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W0': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'}},
'trainees':{ 'Executive Trainee': {'Principal Cities and State/UT capitals': '1500',
  'Other Principal Cities': '1200',
  'Oridnary Cities': '900'},
 'Non-Excutive Trainee': {'Principal Cities and State/UT capitals': '1000',
  'Other Principal Cities': '800',
  'Oridnary Cities': '600'}}},
  'travel allowance': {'board level': {'CMD': {'Principal Cities and State/UT capitals': 'Boarding & Lodging as per actual',
    'Other Principal Cities': 'Boarding & Lodging as per actual',
    'Oridnary Cities': 'Boarding & Lodging as per actual'},
   'Functional Director': {'Principal Cities and State/UT capitals': 'Boarding & Lodging as per actual',
    'Other Principal Cities': 'Boarding & Lodging as per actual',
    'Oridnary Cities': 'Boarding & Lodging as per actual'}},
  'executives': {'E9': {'Principal Cities and State/UT capitals': '14000',
    'Other Principal Cities': '11000',
    'Oridnary Cities': '8800'},
   'E8': {'Principal Cities and State/UT capitals': '9800',
    'Other Principal Cities': '7700',
    'Oridnary Cities': '6160'},
   'E7': {'Principal Cities and State/UT capitals': '5600',
    'Other Principal Cities': '4400',
    'Oridnary Cities': '3520'},
   'E6': {'Principal Cities and State/UT capitals': '5600',
    'Other Principal Cities': '4400',
    'Oridnary Cities': '3520'},
   'E5': {'Principal Cities and State/UT capitals': '4200',
    'Other Principal Cities': '3300',
    'Oridnary Cities': '2640'},
   'E4': {'Principal Cities and State/UT capitals': '4200',
    'Other Principal Cities': '3300',
    'Oridnary Cities': '2640'},
   'E3': {'Principal Cities and State/UT capitals': '3150',
    'Other Principal Cities': '2475',
    'Oridnary Cities': '1980'},
   'E2': {'Principal Cities and State/UT capitals': '3150',
    'Other Principal Cities': '2475',
    'Oridnary Cities': '1980'}},
  'supervisors': {'SSG': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S4': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S3': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S2': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'S1': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'}},
  'workmen': {'WSG': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W11': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W10': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W9': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W8': {'Principal Cities and State/UT capitals': '2000',
    'Other Principal Cities': '1600',
    'Oridnary Cities': '1200'},
   'W7': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W6': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W5': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W4': {'Principal Cities and State/UT capitals': '1500',
    'Other Principal Cities': '1200',
    'Oridnary Cities': '900'},
   'W3': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W2': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W1': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'},
   'W0': {'Principal Cities and State/UT capitals': '1000',
    'Other Principal Cities': '800',
    'Oridnary Cities': '600'}},
'trainees':{ 'Executive Trainee': {'Principal Cities and State/UT capitals': '1500',
  'Other Principal Cities': '1200',
  'Oridnary Cities': '900'},
 'Non-Excutive Trainee': {'Principal Cities and State/UT capitals': '1000',
  'Other Principal Cities': '800',
  'Oridnary Cities': '600'}}}}


class ActionTables(Action):
    """Validating our form input using
    multiple choice answers from Harvard
    Dialect Study"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_tables"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
        subject = tracker.slots.get("subject2")
        level = tracker.slots.get("level")
        if tracker.slots.get("level")=="executives":
            grade = tracker.get_slot('grade_executives')
        elif tracker.slots.get("level")=="board level":
            grade = tracker.get_slot('grade_board_level')
        elif tracker.slots.get("level")=="workmen":
            grade = tracker.get_slot('grade_workmen')
        elif tracker.slots.get("level")=="supervisors":
            grade = tracker.get_slot('grade_supervisors')
        elif tracker.slots.get("level")=="trainees":
            grade = tracker.get_slot('grade_trainees')
        dispatcher.utter_message('\n'.join("{}: {}".format(k, v) for k, v in tables[subject][level][grade].items()))
        #dispatcher.utter_message(str(tables[subject][level][grade]))
        return []

class ValidateLevelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_level_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        slot_subject = tracker.slots.get("subject_cat")
        slot_level = tracker.slots.get("level")
        if (isinstance(slot_subject, str)) and (isinstance(slot_level,type(None))):
            if tracker.slots.get("subject_cat") in ['mobile','telecommunication','conveyance advance','tour and travel','optional holiday','casual leave','earned leave','half pay leave','sick leave']:
                additional_slots.append("level")
            return additional_slots + domain_slots
        if isinstance(slot_level,str):
            if tracker.slots.get("subject_cat") in ['payscale']:
                if tracker.slots.get("level")=="executives":
                    additional_slots.append("grade_executives")
                elif tracker.slots.get("level")=="board level":
                    additional_slots.append("grade_board_level")
                elif tracker.slots.get("level")=="workmen":
                    additional_slots.append("grade_workmen")
                elif tracker.slots.get("level")=="supervisors":
                    additional_slots.append("grade_supervisors")
                elif tracker.slots.get("level")=="trainees":
                    additional_slots.append("grade_trainees")
            return additional_slots + domain_slots
        return domain_slots

class ValidateLevel2Form(FormValidationAction):
    def name(self) -> Text:
        return "validate_level2_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slot_level = tracker.slots.get("level")
        additional_slots = []
        if isinstance(slot_level,str):
            if tracker.slots.get("level")=="executives":
                additional_slots.append("grade_executives")
            elif tracker.slots.get("level")=="board level":
                additional_slots.append("grade_board_level")
            elif tracker.slots.get("level")=="workmen":
                additional_slots.append("grade_workmen")
            elif tracker.slots.get("level")=="supervisors":
                additional_slots.append("grade_supervisors")
            elif tracker.slots.get("level")=="trainees":
                additional_slots.append("grade_trainees")
            return additional_slots + domain_slots
        return domain_slots

class ValidateLevel3Form(FormValidationAction):
    def name(self) -> Text:
        return "validate_level3_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        slot_subject = tracker.slots.get("subject_cat")
        print(slot_subject)
        slot_level = tracker.slots.get("level")
        if (isinstance(slot_subject, str)) and (isinstance(slot_level,type(None))):
            if tracker.slots.get("subject_cat") in ['promotion','grievance']:
                additional_slots.append("level")
            return additional_slots + domain_slots
        if isinstance(slot_level,str):
            if tracker.slots.get("subject_cat") in ['payscale']:
                if tracker.slots.get("level")=="executives":
                    additional_slots.append("grade_executives")
                elif tracker.slots.get("level")=="board level":
                    additional_slots.append("grade_board_level")
                elif tracker.slots.get("level")=="workmen":
                    additional_slots.append("grade_workmen")
                elif tracker.slots.get("level")=="supervisors":
                    additional_slots.append("grade_supervisors")
                elif tracker.slots.get("level")=="trainees":
                    additional_slots.append("grade_trainees")
            return additional_slots + domain_slots
        return domain_slots

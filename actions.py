from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import logging
import warnings
from policy import AllisonPolicy
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
import json
from random import randint
logger = logging.getLogger(__name__)
no_data="{'present': {}, 'missing': []}"
date_missing="{'present': {}, 'missing': ['dateFilter']}"
missing_patient="{'present': {}, 'missing': ['patientNameFilter']}"
date_patient_missing="{'present': {}, 'missing': ['dateFilter','patientNameFilter']}"
def encodeif(intent,entity):
    result=dict()
    result['intent']=intent["name"].encode('ascii','ignore')
    result['data']=entity
    return json.dumps(result)

class ActionDefault(Action):
    def name(self):
        return 'action_default_fallbacks'

    def run(self, dispatcher, tracker, domain):
        intent={}
        intent["name"]="No Intent"
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
    
class ActionOpenImmunization(Action):
    def name(self):
        return 'action_open_immunization'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is None:
            result=encodeif(intent,no_data)
            dispatcher.utter_message(result)
        else:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
    
class ActionOpenSummary(Action):
    def name(self):
        return 'action_open_summary'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is None:
            result=encodeif(intent,no_data)
            dispatcher.utter_message(result)
        else:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionOpenAddressBook(Action):
    def name(self):
        return 'action_open_address_book'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is None:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        else:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots    
    
class ActionUnreadPatientMessagesCount(Action):
    def name(self):
        return 'action_unread_patient_messages_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionUnreadOfficeMessagesCount(Action):
    def name(self):
        return 'action_unread_office_messages_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots  
    
class ActionLastImmunized(Action):
    def name(self):
        return 'action_last_immunized'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
    
class ActionOpenLastEncounters(Action):
    def name(self):
        return 'action_open_last_encounters'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionOpenPatientList(Action):
    def name(self):
        return 'action_open_patient_list'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        temp=next(tracker.get_latest_entity_values("PERSON"), None)
        if temp is None:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
            return_slots = []
            for slot in tracker.slots:
                return_slots.append(SlotSet(slot, None)) 
            return return_slots    
        else:            
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots
    
class ActionOpenHistory(Action):
    def name(self):
        return 'action_open_history'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))         
        return return_slots

class ActionOpenProfile(Action):
    def name(self):
        return 'action_open_profile'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))     
        return return_slots

class ActionOpenLastMedication(Action):
    def name(self):
        return 'action_open_last_medication'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))  
        return return_slots

class ActionOpenSchedulerSettings(Action):
    def name(self):
        return 'action_open_scheduler_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
    
class ActionOpenTemplateSettings(Action):
    def name(self):
        return 'action_open_template_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionFuck(Action):
    def name(self):
        return 'action_fuck'

    def run(self, dispatcher, tracker, domain):
        responses=['shut up sir','hey fuck you','you are dumb ass','please dont say that','does your mother know that you talk like that','are you angry doctor','i am sorry','i am just an A I','please apologise','you are harassing me','is this how you speak to your mother','not me doctor','sorry i am not intelligent as you',]
        pos=randint(0,len(responses)-1)
        utter={"data": "{'present': {}, 'missing': [],'sentence':'"+responses[pos]+"'}", "intent": ""}
        dispatcher.utter_message(json.dumps(utter))
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots    
    
class ActionMarriage(Action):
    def name(self):
        return 'action_marriage'

    def run(self, dispatcher, tracker, domain):
        responses=['i prefer to be single','i can only marry binary language','you must be male','i am glad you asked that, the answer is no by the way','A I can not marry any one','you seem to be flirty','hey naughty shut up','dont ask personal questions','if i could marry anyone that would be Mr.Hassan','Mr.Hassan is my love']
        pos=randint(0,len(responses)-1)
        utter={"data": "{'present': {}, 'missing': [],'sentence':'"+responses[pos]+"'}", "intent": ""}
        dispatcher.utter_message(json.dumps(utter))
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots  
    
class ActionGreeting(Action):
    def name(self):
        return 'action_greeting'

    def run(self, dispatcher, tracker, domain):
        responses=['hi doctor','ohh hello doctor','hi my love','hey baby','Welcome doctor','hi doctor, how can i help you','do you need my help','hello doctor','hi','good to see you','miss you doctor']
        pos=randint(0,len(responses)-1)
        utter={"data": "{'present': {}, 'missing': [],'sentence':'"+responses[pos]+"'}", "intent": ""}
        dispatcher.utter_message(json.dumps(utter))
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots 

class ActionFamily(Action):
    def name(self):
        return 'action_family'

    def run(self, dispatcher, tracker, domain):
        responses=['i have two brothers','seemab and romail are my only brothers','dont ask about my family','please dont ask private question','not in a mood to tell you','i have no sister only two brothers']
        pos=randint(0,len(responses)-1)
        utter={"data": "{'present': {}, 'missing': [],'sentence':'"+responses[pos]+"'}", "intent": ""}
        dispatcher.utter_message(json.dumps(utter))
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots 
    

class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        responses=['it doesnt look romantic at all','it is normal','my temprature is high','internal weather matters not external','ask something i am capable of','i am not your google doctor','i am not in a mood to tell you that']
        pos=randint(0,len(responses)-1)
        utter={"data": "{'present': {}, 'missing': [],'sentence':'"+responses[pos]+"'}", "intent": ""}
        dispatcher.utter_message(json.dumps(utter))
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots     
    
class ActionOpenHPI(Action):
    def name(self):
        return 'action_open_hpi'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots

class ActionOpenReports(Action):
    def name(self):
        return 'action_open_reports'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionOpenWeeklyAppointment(Action):
    def name(self):
        return 'action_open_weekly_appointment'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionOpenDailyAppointment(Action):
    def name(self):
        return 'action_open_daily_appointment'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
        
class ActionAddEncounter(Action):
    def name(self):
        return 'action_add_encounter'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots

class ActionOpenPatientHealthRecord(Action):
    def name(self):
        return 'action_open_patient_health_record'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots

class ActionOpenMedicationList(Action):
    def name(self):
        return 'action_open_medication_list'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots   

class ActionAllergyCount(Action):
    def name(self):
        return 'action_allergy_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots  

class ActionOpenReorderActiveMedicationForPatient(Action):
    def name(self):
        return 'action_open_reorder_active_medication_for_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots 

class ActionOpenEncounters(Action):
    def name(self):
        return 'action_open_encounters'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)    
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result) 
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionSignTheEncounter(Action):
    def name(self):
        return 'action_sign_the_encounter'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots  

class ActionOpenDiagnosisList(Action):
    def name(self):
        return 'action_open_diagnosis_list'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots

class ActionOpenProcedureList(Action):
    def name(self):
        return 'action_open_procedure_list'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots
    
class ActionOpenLastLabWork(Action):
    def name(self):
        return 'action_open_last_labwork'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else: 
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots  
    
class ActionReorderLabWork(Action):
    def name(self):
        return 'action_reorder_labwork'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots 
    
class ActionPendingTasksCount(Action):
    def name(self):
        return 'action_pending_tasks_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None)) 
        return return_slots  

class ActionCreateTask(Action):
    def name(self):
        return 'action_create_task'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots:
            return_slots.append(SlotSet(slot, None))
        return return_slots  
    
class ActionUsePreviousHPI(Action):
    def name(self):
        return 'action_use_previous_hpi'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionSaveHPI(Action):
    def name(self):
        return 'action_save_hpi'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenCCDAExport(Action):
    def name(self):
        return 'action_open_ccda_export'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenLabSetup(Action):
    def name(self):
        return 'action_open_lab_setup'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenPhysicianQualityReportingSystem(Action):
    def name(self):
        return 'action_open_physician_quality_reporting_system'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenRefillRequests(Action):
    def name(self):
        return 'action_open_refill_requests'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenMessages(Action):
    def name(self):
        return 'action_open_messages'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots      
    
class ActionEnterVitalSign(Action):
    def name(self):
        return 'action_enter_vital_sign'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenVitalSigns(Action):
    def name(self):
        return 'action_open_vital_signs'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenMedicationPrescribedLastVist(Action):
    def name(self):
        return 'action_open_medication_prescribed_last_vist'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
    
class ActionNextVisitForPatient(Action):
    def name(self):
        return 'action_next_visit_for_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   

class ActionOpenActivity(Action):
    def name(self):
        return 'action_open_activity'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   
    
class ActionOpenSettings(Action):
    def name(self):
        return 'action_open_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenFaxSettings(Action):
    def name(self):
        return 'action_open_fax_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)       
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenUserManagement(Action):
    def name(self):
        return 'action_open_user_management'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots    
          
class ActionOpenLocationSettings(Action):
    def name(self):
        return 'action_open_location_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots
    
class ActionOpenDrugInteractionAlerts(Action):
    def name(self):
        return 'action_open_drug_interaction_alerts'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenClinicalDecisionSupport(Action):
    def name(self):
        return 'action_open_clinical_decision_support'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenOfficeTest(Action):
    def name(self):
        return 'action_open_office_test'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots    
    
class ActionOpenDocumentType(Action):
    def name(self):
        return 'action_open_document_type'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots    
    
class ActionOpenOfficeMessages(Action):
    def name(self):
        return 'action_open_office_messages'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots     
    
class ActionOpenUnsignedDocuments(Action):
    def name(self):
        return 'action_open_unsigned_documents'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots    
    
class ActionOpenUnsignedEncounters(Action):
    def name(self):
        return 'action_open_unsigned_encounters'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   

class ActionOpenRoleMatrix(Action):
    def name(self):
        return 'action_open_role_matrix'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
        
class ActionOpenUnsignedLabResults(Action):
    def name(self):
        return 'action_open_unsigned_lab_results'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenTasks(Action):
    def name(self):
        return 'action_open_tasks'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenScheduler(Action):
    def name(self):
        return 'action_open_scheduler'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('DATE') is not None) and (tracker.get_slot('TIME') is not None):
            date=tracker.get_slot('DATE')
            time=tracker.get_slot('TIME')
            data="{'present': {'dateFilter': '"+date+"','timeFilter': '"+time+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('DATE') is not None:
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter':'"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('TIME') is not None:
            time=tracker.get_slot('TIME')
            data="{'present': {'timeFilter':'"+time+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            data=date_missing
            result=encodeif(intent,data)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionAddClaim(Action):
    def name(self):
        return 'action_add_claim'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionSaveTemplate(Action):
    def name(self):
        return 'action_save_template'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionPrintEncounter(Action):
    def name(self):
        return 'action_print_encounter'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenReviewOfSystem(Action):
    def name(self):
        return 'action_open_review_of_system'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenDocuments(Action):
    def name(self):
        return 'action_open_documents'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionAddAppointment(Action):
    def name(self):
        return 'action_add_appointment'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

    
class ActionMarkPatientInactive(Action):
    def name(self):
        return 'action_mark_patient_inactive'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionDeletePatient(Action):
    def name(self):
        return 'action_delete_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenBI(Action):
    def name(self):
        return 'action_open_bi'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionStatusUpdate(Action):
    def name(self):
        return 'action_status_update'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionUnsignedLabResultsCount(Action):
    def name(self):
        return 'action_unsigned_lab_results_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionUnsignedEncountersCount(Action):
    def name(self):
        return 'action_unsigned_encounters_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionTotalUnreadMessagesCount(Action):
    def name(self):
        return 'action_total_unread_messages_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionRefillRequestsCount(Action):
    def name(self):
        return 'action_refill_requests_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenVisitType(Action):
    def name(self):
        return 'action_open_visit_type'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenPatientLetter(Action):
    def name(self):
        return 'action_open_patient_letter'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenDirectMessages(Action):
    def name(self):
        return 'action_open_direct_messages'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenDashboard(Action):
    def name(self):
        return 'action_open_dashboard'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenClaims(Action):
    def name(self):
        return 'action_open_claims'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
            
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionLogout(Action):
    def name(self):
        return 'action_logout'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenTodaysScheduledPatients(Action):
    def name(self):
        return 'action_open_todays_scheduled_patients'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionAddPatient(Action):
    def name(self):
        return 'action_add_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenFirstAppointment(Action):
    def name(self):
        return 'action_open_first_appointment'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionFirstPatient(Action):
    def name(self):
        return 'action_open_first_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenFaxes(Action):
    def name(self):
        return 'action_open_faxes'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenPatientMessages(Action):
    def name(self):
        return 'action_open_patient_messages'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenUserSetup(Action):
    def name(self):
        return 'action_open_user_setup'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenEPrescriptionSetup(Action):
    def name(self):
        return 'action_open_eprescription_setup'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   

class ActionOpenAutomatedReminderCalls(Action):
    def name(self):
        return 'action_open_automated_reminder_calls'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   

class ActionOpenImportPatient(Action):
    def name(self):
        return 'action_open_import_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenAutoLockSettings(Action):
    def name(self):
        return 'action_open_auto_lock_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots      

class ActionOpenPatientCommunicate(Action):
    def name(self):
        return 'action_open_patient_communicate'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenPracticeSettings(Action):
    def name(self):
        return 'action_open_practice_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots    
    
class ActionTodaysAppointmentsCount(Action):
    def name(self):
        return 'action_todays_appointments_count'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenBalanceReminderCalls(Action):
    def name(self):
        return 'action_open_balance_reminder_calls'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)       
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenInviteToPHR(Action):
    def name(self):
        return 'action_open_invite_to_phr'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenICheckinSettings(Action):
    def name(self):
        return 'action_open_icheckin_settings'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        for slot in tracker.slots:           
            return_slots.append(SlotSet(slot, None))     
        return return_slots
    
class ActionOpenImmunizationRegistry(Action):
    def name(self):
        return 'action_open_immunization_registry'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenImmunizationInventory(Action):
    def name(self):
        return 'action_open_immunization_inventory'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenLabsConnectivity(Action):
    def name(self):
        return 'action_open_labs_connectivity'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenPatientIntakeForm(Action):
    def name(self):
        return 'action_open_patient_intake_form'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenPhysicalExam(Action):
    def name(self):
        return 'action_open_physical_exam'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenPayerList(Action):
    def name(self):
        return 'action_open_payer_list'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        for slot in tracker.slots:        
            return_slots.append(SlotSet(slot, None))      
        return return_slots
    
class ActionOpenServerClock(Action):
    def name(self):
        return 'action_open_server_clock'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenBillingSolution(Action):
    def name(self):
        return 'action_open_billing_solution'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        for slot in tracker.slots:           
            return_slots.append(SlotSet(slot, None))    
        return return_slots
    
class ActionOpenEligibility(Action):
    def name(self):
        return 'action_open_eligibility'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenEPrescriptionForCtrlSubstances(Action):
    def name(self):
        return 'action_open_eprescription_for_ctrl_substances'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenFeeStructure(Action):
    def name(self):
        return 'action_open_fee_structure'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)       
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenEncountersType(Action):
    def name(self):
        return 'action_open_encounters_type'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionActiveMedicationForPatient(Action):
    def name(self):
        return 'action_active_medication_for_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionNextPatient(Action):
    def name(self):
        return 'action_next_patient'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionCreateClaimForEncounter(Action):
    def name(self):
        return 'action_create_claim_for_encounter'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('PERSON') is not None) and (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"','dateFilter': '"+date+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('DATE') is not None):
            date=tracker.get_slot('DATE')
            data="{'present': {'dateFilter': '"+date+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif (tracker.get_slot('PERSON') is not None): 
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['dateFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,date_patient_missing)
            dispatcher.utter_message(result)        
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenEncountersOfNextAppointment(Action):
    def name(self):
        return 'action_open_encounters_of_next_appointment'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenLabOrderTemplate(Action):
    def name(self):
        return 'action_open_lab_order_template'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionPrescribeLastMedication(Action):
    def name(self):
        return 'action_prescribe_last_medication'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,missing_patient)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    

class ActionAddAllergy(Action):
    def name(self):
        return 'action_add_allergy'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('ALLERGY') is not None) and (tracker.get_slot('PERSON') is not None):
            name=tracker.get_slot('PERSON')
            allergy=tracker.get_slot('ALLERGY')
            data="{'present': {'patientNameFilter': '"+name+"','allergyFilter': '"+allergy+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('ALLERGY') is not None:
            allergy=tracker.get_slot('ALLERGY')
            data="{'present': {'allergyFilter': '"+allergy+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['allergyFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,no_data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionAddDiagnosis(Action):
    def name(self):
        return 'action_add_diagnosis'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        if (tracker.get_slot('DIAGNOSIS') is not None) and (tracker.get_slot('PERSON') is not None):
            name=tracker.get_slot('PERSON')
            diagnosis=tracker.get_slot('DIAGNOSIS')
            data="{'present': {'patientNameFilter': '"+name+"','diagnosisFilter': '"+diagnosis+"'}, 'missing': []}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            data="{'present': {'patientNameFilter': '"+name+"'}, 'missing': ['diagnosisFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        elif tracker.get_slot('DIAGNOSIS') is not None:
            diagnosis=tracker.get_slot('DIAGNOSIS')
            data="{'present': {'diagnosisFilter': '"+diagnosis+"'}, 'missing': ['patientNameFilter']}"
            result=encodeif(intent,data)
            dispatcher.utter_message(result)
        else:
            result=encodeif(intent,no_data)
            dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots
    
class ActionOpenAdvanceDirective(Action):
    def name(self):
        return 'action_open_advance_directive'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots      

class ActionOpenAlerts(Action):
    def name(self):
        return 'action_open_alerts'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots
    
class ActionOpenCancerRegistry(Action):
    def name(self):
        return 'action_open_cancer_registry'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots
    
class ActionOpenCarePlan(Action):
    def name(self):
        return 'action_open_care_plan'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenChartNotes(Action):
    def name(self):
        return 'action_open_chart_notes'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenCognitiveStatus(Action):
    def name(self):
        return 'action_open_cognitive_status'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenFamilyHistory(Action):
    def name(self):
        return 'action_open_family_history'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  
    
class ActionOpenFlowSheet(Action):
    def name(self):
        return 'action_open_flow_sheet'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots

class ActionOpenFunctionalStatus(Action):
    def name(self):
        return 'action_open_functional_status'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots  

class ActionOpenOutgoingReferral(Action):
    def name(self):
        return 'action_open_outgoing_referral'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots

class ActionOpenSocialHistory(Action):
    def name(self):
        return 'action_open_social_history'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots

class ActionOpenTemplateProcedure(Action):
    def name(self):
        return 'action_open_template_procedure'

    def run(self, dispatcher, tracker, domain):
        intent=tracker.latest_message.intent
        result=encodeif(intent,no_data)
        dispatcher.utter_message(result)
        return_slots = []
        for slot in tracker.slots: 
            return_slots.append(SlotSet(slot, None))   
        return return_slots   
    
def train_dialogue(domain_file="restaurant_domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/babi_stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            RestaurantPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('data/franken_data.json')
    trainer = Trainer(config.load("nlu_model_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")

    return model_directory


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("core/nlu/sibtain/default/current")
    agent = Agent.load("core/dialogue/sibtain", interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    #parser = argparse.ArgumentParser(
            #description='starts the bot')

    #parser.add_argument(
            #'task',
            #choices=["train-nlu", "train-dialogue", "run"],
            #help="what the bot should do - e.g. run or train?")
    #task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    #if task == "train-nlu":
        #train_nlu()
    #elif task == "train-dialogue":
        #train_dialogue()
    #elif task == "run":
    run()

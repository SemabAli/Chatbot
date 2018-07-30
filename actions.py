from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from policy import RestaurantPolicy
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


class Actionshowlive(Action):
    def name(self):
        return 'action_show_live'

    def run(self, dispatcher, tracker, domain):
        #date=tracker.get_slot("date")
        dispatcher.utter_message("Showing Live")       
        return []
    
class Actionopenhistory(Action):
    def name(self):
        return 'action_open_history'

    def run(self, dispatcher, tracker, domain):       
        #date=tracker.get_slot("date")
        dispatcher.utter_message("opening history of event")
        return []
    
class Actionshowscore(Action):
    def name(self):
        return 'action_show_score'

    def run(self, dispatcher, tracker, domain):
       #d#ate=tracker.get_slot("date")
        dispatcher.utter_message("Showing score of match")
        #name=tracker.get_slot("name")
        return []











class ActionOpenLastMedication(Action):
    def name(self):
        return 'action_open_last_medication'

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('PERSON') is not None:
            name=tracker.get_slot('PERSON')
            dispatcher.utter_message("opening last medication of "+name)
        else:
            dispatcher.utter_message("Please specify Patient Name")
        return []

class ActionOpenDailyAppointment(Action):
    def name(self):
        return 'action_open_daily_appointment'

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('DATE') is not None:
            dispatcher.utter_message("opening daily Appointment")
        else:
            dispatcher.utter_message("Please specify appointment details")
        return_slots = []
        for slot in tracker.slots:
            if slot != "PERSON":
                return_slots.append(SlotSet(slot, None))
        return return_slots

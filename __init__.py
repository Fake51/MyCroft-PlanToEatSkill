"""Mycroft AI skill for querying PlanToEat"""

from bs4 import BeautifulSoup
from datetime import datetime
from mycroft import MycroftSkill, intent_file_handler
from requests import Session
from urllib.parse import urlencode, quote

import json
from . import plantoeatapi


__author__ = "Peter Lind"
__version__ = "0.4.1"
__copyright__ = "Copyright 2021, Peter Lind"
__license__ = "MIT"


class PlanToEat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__(name="PlanToEatSkill")
        self.logged_in = False
        self.api = None

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self._setup()

    def on_settings_changed(self):
        self._setup()

    def _setup(self):
        if not self.settings:
            self.log.info("settings is not set")
            return

        if not self.settings.get('username'):
            self.log.info("username setting is not set")
            return

        if not len(self.settings.get('username')):
            self.log.info("username setting is empty")
            return

        if not self.settings.get('password'):
            self.log.info("username setting is not set")
            return

        if not len(self.settings.get('password')):
            self.log.info("username setting is empty")
            return

        try:
            self.api = plantoeatapi.create(
                self.settings.get('username'), 
                self.settings.get('password')
            )

            self.logged_in = True

        except Exception as inst:
            self.log.info(inst)
            return

    @intent_file_handler('WhatIsForDinner.intent')
    def handle_whats_for_dinner(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        today = datetime.today().strftime('%Y-%m-%d')
        events = self.api.fetchDateEvents(today)

        dinner = ", ".join([event["description"] for event in events])

        if "" == dinner:
            self.speak_dialog('WhatIsForDinner_failure')
        else:
            self.speak_dialog('WhatIsForDinner_success', {'dinner': dinner})


    @intent_file_handler('AddToList.intent')
    def handle_add_to_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        item_name = message.data.get('item')

        try:
            self.api.addItemToList(item_name)
            self.speak_dialog('AddToList_success', {'item': item_name})
        except Exception as inst:
            self.log.info(inst)
            self.speak_dialog('AddToList_failure', {'item': item_name})

    @intent_file_handler('RevealList.intent')
    def reveal_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        items = self.api.fetchShoppingListItems()

        if len(items) > 0:
            itemList = ", ".join(item["title"] for item in items)
            self.speak_dialog('RevealList_items', {'items': items})
        elif items == "":
            self.speak_dialog('RevealList_empty')
        else:
            self.speak_dialog('RevealList_failure')


def create_skill():
    return PlanToEat()


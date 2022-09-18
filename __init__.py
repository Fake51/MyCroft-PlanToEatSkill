"""Mycroft AI skill for querying PlanToEat"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_file_handler
from requests import Session
from urllib.parse import urlencode, quote

import json
from . import plantoeatapi


__author__ = "Peter Lind"
__version__ = "0.5.1"
__copyright__ = "Copyright 2022, Peter Lind"
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

        when = message.data.get('when')

        if 'today' == when or 'tonight' == when:
            date = datetime.today().strftime('%Y-%m-%d')

        elif 'tomorrow' == when:
            date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        else:
            date = datetime.today().strftime('%Y-%m-%d')

        dinner = self.api.getDinnerDescription(date)

        if "" == dinner:
            self.speak_dialog('WhatIsForDinner_failure')
        else:
            self.speak_dialog('WhatIsForDinner_success', {'dinner': dinner})


    @intent_file_handler('IsItemOnList.intent')
    def handle_is_item_on_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        itemName = message.data.get('item')

        if self.api.isItemOnList(itemName):
            self.speak_dialog('IsItemOnList_yes', {'item': itemName})
        else:
            self.speak_dialog('IsItemOnList_no', {'item': itemName})


    @intent_file_handler('RemoveFromList.intent')
    def handle_remove_from_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        itemName = message.data.get('item')

        if self.api.removeItemFromList(itemName):
            self.speak_dialog('RemoveFromList_success', {'item': itemName})
        else:
            self.speak_dialog('RemoveFromList_failure', {'item': itemName})


    @intent_file_handler('AddToList.intent')
    def handle_add_to_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        itemList = [message.data.get('item1')]

        item = message.data.get('item2')
        if item != "":
            itemList.append(item)

        item = message.data.get('item3')
        if item != "":
            itemList.append(item)

        try:
            self.api.addItemToList(itemList)

            lastItem = itemList.pop()

            if len(itemList) > 0:
                items = "{0} and {1}".format(", ".join(itemList), lastItem)
            else:
                items = lastItem

            self.speak_dialog('AddToList_success', {'items': items})
        except Exception as inst:
            self.log.info(inst)

            lastItem = itemList.pop()

            if len(itemList) > 0:
                items = "{0} and {1}".format(", ".join(itemList), lastItem)
            else:
                items = lastItem

            self.speak_dialog('AddToList_failure', {'items': items})


    @intent_file_handler('RevealList.intent')
    def reveal_list(self, message):
        if not self.logged_in:
            self._setup()

            if not self.logged_in:
                self.speak_dialog('NotLoggedIn')
                return

        items = self.api.fetchShoppingListItems()

        if len(items) > 0:
            itemList = ", ".join([item["title"] for item in items if item["title"]])
            self.speak_dialog('RevealList_items', {'items': itemList})
        elif items == "":
            self.speak_dialog('RevealList_empty')
        else:
            self.speak_dialog('RevealList_failure')


def create_skill():
    return PlanToEat()


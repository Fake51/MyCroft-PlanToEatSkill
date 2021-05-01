from mycroft import MycroftSkill, intent_file_handler
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urlencode, quote
import json

userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

submitString = 'shopping_list_id={0}&autoStore=1&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D={1}&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D={2}&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0&ingredients%5B%5D%5Bamount%5D=&ingredients%5B%5D%5Bunit%5D=&ingredients%5B%5D%5Btitle%5D=&ingredients%5B%5D%5Bnote%5D=&ingredients%5B%5D%5Bcategory%5D=&ingredients%5B%5D%5Bstore%5D=0'

baseUrl = "https://www.plantoeat.com/{0}"

class PlanToEat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__(name="PlanToEatSkill")
        self.session = Session()
        self.logged_in = False
        self.shopping_list_id = None

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self._setup()

    def on_settings_changed(self):
        self._setup()

    def _setup(self):
        if not self.settings:
            self.log.debug("settings is not set")
            return

        if not self.settings.get('username'):
            self.log.debug("username setting is not set")
            return

        if not len(self.settings.get('username')):
            self.log.debug("username setting is empty")
            return

        if not self.settings.get('password'):
            self.log.debug("username setting is not set")
            return

        if not len(self.settings.get('password')):
            self.log.debug("username setting is empty")
            return

        response = self.session.get(
            baseUrl.format("login"),
            headers = {
                'User-Agent': userAgent,
            }
        )

        if 200 != response.status_code:
            self.log.debug("Response from getting login page was {0}".format(response.status_code))
            return

        soup = BeautifulSoup(response.text, "html.parser")

        csrf = soup.find_all("meta", attrs = {"name": "csrf-token"})

        if not csrf or len(csrf) < 1:
            self.log.debug("Failed to extract CSRF token")
            return

        data = {
            'authenticity_token': csrf[0]['content'],
            'login[email]': self.settings.get('username'),
            'login[password]': self.settings.get('password'),
        }

        login_response = self.session.post(
            baseUrl.format("login"),
            headers = {
                'User-Agent': userAgent,
                'Referer': baseUrl.format('login'),
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data = urlencode(data)
        )

        if 200 != login_response.status_code:
            self.log.debug("Login request failed - status code: {0}".format(login_response.status_code))
            return

        soup = BeautifulSoup(login_response.text, "html.parser")
        logout = soup.find_all('a', attrs = {"href": "/logout"})

        if not logout:
            self.log.debug("Failed to login")
            return

        shopping_lists = self.session.get(
            baseUrl.format("shopping_lists"),
            headers = {
                'User-Agent': userAgent,
            }
        )

        if 200 != shopping_lists.status_code:
            self.log.debug("Failed to fetch shopping lists page - status code: {0}".format(shopping_lists.status_code))
            return

        soup = BeautifulSoup(shopping_lists.text, "html.parser")
        list_id_input = soup.find_all("input", id="shopping_list_id")

        if not list_id_input:
            self.log.debug("Failed to find shopping list id")
            return

        self.shopping_list_id = list_id_input[0]['value']
        self.logged_in = True

    @intent_file_handler('AddToList.intent')
    def handle_add_to_list(self, message):
        item_name = message.data.get('item')

        if self._add_item_to_list(item_name):
            self.speak_dialog('AddToList_success', {'item': item_name})
        else:
            self.speak_dialog('AddToList_failure', {'item': item_name})

    def _add_item_to_list(self, item_name):
        category_suggestion = self._get_category_suggestion(item_name)

        requestData = submitString.format(self.shopping_list_id, quote(item_name), category_suggestion)

        add_item_response = self.session.post(
            baseUrl.format("shopping_lists/update"),
            headers = {
                'User-Agent': userAgent,
            },
            data = requestData
        )

        if 200 != add_item_response.status_code:
            self.log.debug("Failed to add item to shopping list - status code: {0}".format(add_item_response.status_code))
            return False

        return True

    def _get_category_suggestion(self, item_name):
        response = self.session.post(
            baseUrl.format("recommend_category"),
            headers = {'User-Agent': userAgent},
            data = urlencode({'title': item_name})
        )

        if response.status_code != 200:
            return ""
        self.log.info(response.text)
        result = json.loads(response.text)

        if result and len(result) == 3 and result[2]:
            return result[2]
        
        return ''
    
def create_skill():
    return PlanToEat()


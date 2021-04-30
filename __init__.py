from mycroft import MycroftSkill, intent_file_handler
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urlencode
from mycroft.util.log import getLogger 

userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

LOGGER = getLogger(__name__)

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
            LOGGER.error("settings is not set")
            return

        if not self.settings.get('username'):
            LOGGER.error("username setting is not set")
            return

        if not len(self.settings.get('username')):
            LOGGER.error("username setting is empty")
            return

        if not self.settings.get('password'):
            LOGGER.error("username setting is not set")
            return

        if not len(self.settings.get('password')):
            LOGGER.error("username setting is empty")
            return

        response = self.session.get(
            "https://www.plantoeat.com/login",
            headers = {
                'User-Agent': userAgent,
            }
        )

        LOGGER.info(response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")

        csrf = soup.find_all("meta", attrs = {"name": "csrf-token"})
        data = {
            'authenticity_token': csrf[0]['content'],
            'login[email]': self.settings.get('username'),
            'login[password]': self.settings.get('password'),
        }

        login_response = self.session.post(
            "https://www.plantoeat.com/login",
            headers = {
                'User-Agent': userAgent,
                'Referer': 'https://www.plantoeat.com/login',
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data = urlencode(data)
        )

        LOGGER.info(urlencode(data))

        LOGGER.info(login_response.status_code)

        shopping_lists = self.session.get(
            "https://www.plantoeat.com/shopping_lists",
            headers = {
                'User-Agent': userAgent,
            }
        )

        LOGGER.info(shopping_lists.status_code)

        soup = BeautifulSoup(shopping_lists.text, "html.parser")
        list_id_input = soup.find_all("input", id="shopping_list_id")
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
        data = {
            'shopping_list_id': self.shopping_list_id,
            'autoStore': 1,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': item_name,
            'ingredients[][note]': '',
            'ingredients[][category]': 'Other',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
            'ingredients[][amount]': '',
            'ingredients[][unit]': '',
            'ingredients[][title]': '',
            'ingredients[][note]': '',
            'ingredients[][category]': '',
            'ingredients[][store]': 0,
        }

        add_item_response = self.session.post(
            "https://www.plantoeat.com/shopping_lists/update",
            headers = {
                'User-Agent': userAgent,
            },
            data = urlencode(data)
        )

        LOGGER.info(add_item_response.status_code)

        return True
    
def create_skill():
    return PlanToEat()


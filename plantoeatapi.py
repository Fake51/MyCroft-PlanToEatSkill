from requests import Session


userAgent = 'Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/98.0'

baseUrl = "https://api.plantoeat.com/{0}"

class PlanToEatApi():
    def __init__(self, username, password):
        self.session = Session()
        self.authToken = None

        response = self.session.post(
            baseUrl.format("oauth/token"),
            headers = self._makeApiHeaders(),
            json = {
                'email': username,
                'password': password,
                'grant_type': 'password',
            }
        )

        if 200 != response.status_code:
            raise Exception("Login request failed - status code: {0}".format(response.status_code))

        jsonResponse = response.json()

        if "access_token" not in jsonResponse:
            raise Exception("Responsse from login request does not contain access token")

        self.authToken = jsonResponse["access_token"]


    def _makeApiHeaders(self, extraHeaders = {}):
        defaultHeaders = {
            'User-Agent': userAgent,
            "X-PTE-CLIENT-VERSION": "2.9.3",
        }

        for key in extraHeaders:
            defaultHeaders[key] = extraHeaders[key]

        if self.authToken:
            defaultHeaders["Authorization"] = "Bearer " + self.authToken

        return defaultHeaders


    def fetchShoppingListItems(self):
        itemsResponse = self.session.get(
            baseUrl.format("api/v1/shopping_list/items"),
            headers = self._makeApiHeaders()
        )

        if 200 != itemsResponse.status_code:
            self.log.info("Failed to get items from shopping list - status code: {0}".format(itemsResponse.status_code))
            return None

        items = []

        for item in itemsResponse.json():
            if item["recipe_ids"] == [] and item["event_ids"] == [] and item["purchased"] == None:
                items.append(item["title"])

        return ", ".join(items)

    def addItemToList(self, itemName):
#        categorySuggestion = self._getCategorySuggestion(itemName)

        addItemResponse = self.session.post(
            baseUrl.format("api/v1/shopping_list/items"),
            headers = self._makeApiHeaders(),
            json = {"item": {"title": itemName}}
        )

        if 200 < addItemResponse.status_code and 300 >= addItemResponse.status_code:
            raise Exception("Failed to add item to shopping list - status code: {0}".format(addItemResponse.status_code))

    def _getCategorySuggestion(self, itemName):
        response = self.session.post(
            baseUrl.format("recommend_category"),
            headers = {'User-Agent': userAgent, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            data = "title={0}".format(quote(itemName))
        )

        if response.status_code != 200:
            return ""

        result = response.json()

        if result and len(result) == 3 and result[2]:
            return result[2]
        
        return ''


def create(username, password):
    return PlanToEatApi(username, password)

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

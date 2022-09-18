from requests import Session
import re

userAgent = 'Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/98.0'
baseUrl = "https://api.plantoeat.com/{0}"
clientVersion = "2.9.3"

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
            "X-PTE-CLIENT-VERSION": clientVersion,
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
                items.append({"id": item["item_ids"][0], "title": item["title"]})

        return items


    def isItemOnList(self, itemName):
        for item in self.fetchShoppingListItems():
            if re.search(itemName, item["title"]):
                return True

        return False


    def addItemToList(self, itemList):
        categorySuggestionId = self._getCategorySuggestion(itemName)

        for itemName in itemList:
            addItemResponse = self.session.post(
                baseUrl.format("api/v1/shopping_list/items"),
                headers = self._makeApiHeaders(),
                json = {"item": {"title": itemName, "grocery_category_id": categorySuggestionId, "store_id": None}}
            )

            if not addItemResponse.ok:
                raise Exception("Failed to add item to shopping list - status code: {0}".format(addItemResponse.status_code))


    def removeItemFromList(self, itemName):
        itemIds = []

        for item in self.fetchShoppingListItems():
            if re.search(itemName, item["title"]):
                itemIds.append(item["id"])

        if 0 < len(itemIds):
            removeItemResponse = self.session.delete(
                baseUrl.format("api/v1/shopping_list/items"),
                headers = self._makeApiHeaders(),
                json = {"item_ids": itemIds}
            )

            return removeItemResponse.ok

        return false

    def _getCategorySuggestion(self, itemName):
        response = self.session.get(
            baseUrl.format("api/v1/ingredients/suggestion?title={0}".format(itemName)),
            headers = self._makeApiHeaders()
        )

        if not response.ok:
            return None

        result = response.json()

        if result and "category_id" in result:
            return result["category_id"]
        
        return None


    def fetchDateEvents(self, date):
        response = self.session.get(
            baseUrl.format("api/v1/events?start_date={0}&end_date={0}".format(date)),
            headers = self._makeApiHeaders()
        )

        if not response.ok:
            return None

        return response.json()


    def fetchRecipes(self, recipeIds):
        if 0 == len(recipeIds):
            return []

        ids = [str(id) for id in recipeIds]

        response = self.session.get(
            baseUrl.format("api/v1/recipes?ids={0}".format(",".join(ids))),
            headers = self._makeApiHeaders()
        )

        if response.ok:
            return response.json()

        return []


    def getDinnerDescription(self, date):
        events = self.fetchDateEvents(date)

        if 0 == len(events):
            return ""

        parts = []
        recipeIds = []

        for event in events:
            if event["description"]:
                parts.append(event["description"])
            elif event["recipe_id"]:
                recipeIds.append(event["recipe_id"])

        if 0 < len(recipeIds):
            for recipe in self.fetchRecipes(recipeIds):
                if "title" in recipe:
                    parts.append(recipe["title"])


        return ", ".join(parts)

def create(username, password):
    return PlanToEatApi(username, password)

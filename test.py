import plantoeatapi
import sys

api = plantoeatapi.create(sys.argv[1], sys.argv[2])

#api.addItemToList("butter")

#items = api.fetchShoppingListItems()
#itemList = ", ".join(item["title"] for item in items)
#print(itemList)

categories = api._getCategorySuggestion("butter")

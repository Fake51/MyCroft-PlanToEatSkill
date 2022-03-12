import plantoeatapi
import sys

api = plantoeatapi.create(sys.argv[1], sys.argv[2])

#api.addItemToList("butter")

#items = api.fetchShoppingListItems()
#itemList = ", ".join(item["title"] for item in items)
#print(itemList)

#api.addItemToList("bacon")
#dateEvents = api.fetchDateEvents("2022-03-12")

#dinner = ", ".join([event["description"] for event in dateEvents if event["description"]])
#print(dinner)


items = api.fetchShoppingListItems()
print(items)
itemList = ", ".join([item["title"] for item in items if item["title"]])
print(itemList)

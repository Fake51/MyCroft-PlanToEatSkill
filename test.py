import plantoeatapi

api = plantoeatapi.create(email, password)

#api.addItemToList("butter")

items = api.fetchShoppingListItems()
print(items)

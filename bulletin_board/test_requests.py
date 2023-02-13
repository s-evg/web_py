import requests


#GET for all
resp = requests.get('http://localhost:5555/api/v1/advs/').json()
print(resp)

# # POST
# resp = requests.post('http://localhost:5555/api/v1/advs/',
#                           json={"author": "Test",
#                                 "title": "test",
#                                 "description": "test"})

resp = requests.post('http://localhost:5555/api/v1/advs/',
                          json={"author": "grey",
                                "title": "Super-puper",
                                "description": "Bla-bla-bla"})
print(resp)


# GET by id
resp = requests.get('http://localhost:5555/api/v1/adv/1').json()
print(resp)


# PUT by id
# response = requests.put('http://localhost:5555/api/v1/adv/1',
#                           json={"title": "sometitle", "description": "somedescription"})
# print(response)


# DELETE by id
# response = requests.delete('http://localhost:5555/api/v1/adv/3')
# print(response)

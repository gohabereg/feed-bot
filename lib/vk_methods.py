#pip install requests
#https://oauth.vk.com/authorize?client_id=7664884&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline,stories,photos,app_widget,groups,docs,manage,wall&response_type=token&v=5.52

import requests
import json

token = ''
user_id = ''
app_id = '7664884'

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

def sendRequest(method, parameters):
    api_url = 'https://api.vk.com/method/'
    method_name = method
    response = requests.get(
        api_url + method_name + '?' + 'access_token=' + token + '&', params=parameters + '&v=5.52').json()
    write_json(response, 'response.json')
    #result = response.text
    #print(response)

def loadProfile():
    sendRequest('users.get', "{'user_ids': "+user_id+", 'fields': 'photo_100'}")

def loadNews():
    sendRequest('newsfeed.get', "{'filters': 'post', 'count': 2}")

loadNews()
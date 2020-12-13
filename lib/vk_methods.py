#pip install requests
#https://oauth.vk.com/authorize?client_id=7664884&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline,stories,photos,app_widget,groups,docs,manage,wall&response_type=token&v=5.52

import requests
import json
import vk_api

token = '190e4717df7e39b682e0b248d7e9b528ebe323dbdcfc2ec61db21c60449917c0b2ca6437e21c50bd49e37'
user_id = '106131559'
app_id = '7664884'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

def loadProfile():
    response = vk.users.get(user_ids=user_id, fields='photo_100')
    write_json(response, 'response.json')

def loadNews():
    response = vk.newsfeed.get(filters='post', count=0)
    write_json(response, 'response.json')

loadNews()

#print(vk.users.get(user_ids=user_id, fields='photo_100'))

# def sendRequest(method, parameters):
#     api_url = 'https://api.vk.com/method/'
#     method_name = method
#     response = requests.get(
#         api_url + method_name + '?' + 'access_token=' + token + '&', params=parameters + '&v=5.52').json()
#     write_json(response, 'response.json')
#     #result = response.text
#     #print(response)

# def loadProfile():
#     sendRequest('users.get', "{'user_ids': "+user_id+", 'fields': 'photo_100'}")
#
# def loadNews():
#     sendRequest('newsfeed.get', "{'filters': 'post', 'count': 2}")

import requests
import json
import vk_api
import os
from pymongo import MongoClient


class VkMethods:

    def write_json(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    # def loadProfile():
    #     response = vk.users.get(user_ids=user_id, fields='photo_100')
    #     return response

    def getUserData(self):
        user_list = []
        client = MongoClient('db', username='root', password='root')
        db = client['bot']
        doc = db.users.find({}, {"vk_id": 1, "vk_token": 1})
        for i in doc:
            user_list.append(str(i["vk_id"]))
            user_list.append(str(i["vk_token"]))

        list_length = len(user_list)
        print(user_list[0:list_length])
        return user_list

    def loadNews(self, vk_token):
        vk_session = vk_api.VkApi(token=vk_token)
        vk = vk_session.get_api()
        response = vk.newsfeed.get(filters='post', count=10)
        print(response)
        return response

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

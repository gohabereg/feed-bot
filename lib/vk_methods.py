import requests
import json
import vk_api
import os

class VkMethods:

    vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
    vk = vk_session.get_api()

    # def write_json(data, filename):
    #     with open(filename, 'w') as file:
    #         json.dump(data, file, indent=2)

    # def loadProfile():
    #     response = vk.users.get(user_ids=user_id, fields='photo_100')
    #     return response

    def loadNews():
        response = vk.newsfeed.get(filters='post', count=10)
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

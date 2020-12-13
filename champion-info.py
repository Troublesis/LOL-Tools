import requests
import urllib.request as request
from lxml import html
import json
# import datetime
# from datetime import date
# from datetime import timedelta
#
# today = date.today()
#
# main_url = "http://ddragon.leagueoflegends.com/cdn/10.18.1/data/en_US/champion.json"
# # response = requests.get(main_url)
# # champion_info_tree = html.fromstring(response.content)
# # # print(champion_info_tree.text)
# # champion_info_list = champion_info_tree.text
# # # print(champion_info_list)
# # champion_data = json.loads(champion_info_list)
# #
# # champion_data_file = json.dumps(champion_data["data"])
# # # print(champion_data)
# # with open('champion-data.txt', 'w') as f:
# #     print('today is: ', today)
# #
# #     print('\n\n\n' + champion_data_file, file=f)
# # f.close()
#
#
#
# # champion = input("Please input champion name:")
# # url = "http://ddragon.leagueoflegends.com/cdn/10.18.1/data/en_US/champion/{}.json".format(champion)
# # print(url)
# # page = BeautifulSoup(requests.get(url).content)
# # print(page.text)
#
# #
# # url = "http://ddragon.leagueoflegends.com/cdn/10.18.1/data/en_US/champion/Amumu.json"
# # response = requests.get(url)
# # champion_detail_info_tree = html.fromstring(response.content)
# # # # print(champion_info_tree.text)
# # champion_detail_info_list = champion_detail_info_tree.text
# # with open('champion-detail-data.json', 'w') as f:
# #     json.dump(champion_detail_info_list, f)
# # f.close()
# #
# #
# # with open('champion-detail-data.json', 'r') as f:
# #     champion_detail_info_dict = json.load(f)
# # f.close()
# # print(champion_detail_info_dict)


version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
response = requests.get(version_url)
version_list = html.fromstring(response.content)
version_list = version_list.text
# print(version_list)
# convert json into list
version_list = json.loads(version_list)
# print(type(version_list))
# print(version_list)
# get current version
current_version = version_list[0]
print("current version is: " + current_version)

champion_list_url = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/data/en_US/champion.json"
print(champion_list_url)
# response = requests.get(champion_list_url)
# champions_dict = html.fromstring(response.content).text
# champions_dict = json.loads(champions_dict)
# champions_dict = champions_dict["data"]
# # print(champions_dict)
#
# def getList(dict):
#     return list(dict.keys())
#
# champion_list = getList(champions_dict)
with request.urlopen(champion_list_url) as response:
    source = response.read()
    champion_dict = json.loads(source)
champion_dict = champion_dict["data"]
# print(champion_dict)

def getList(dict):
    return list(dict.keys())

champion_list = getList(champion_dict)
print(champion_list)

champion_name = input("please input champion name: ").capitalize()
champion_dict_url = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/data/en_US/champion/" + champion_name + ".json"
print(champion_dict_url)
# response = requests.get(champion_dict_url)
# champion_dict = html.fromstring(response.content).text
#
# with open('champion-detail-data.json', 'w') as f:
#     json.dump(champion_dict, f)
#     f.close()
#
# with open('champion-detail-data.json') as json_file:
#     champion_detail = json.load(json_file)
# print(champion_detail)
# print("Type:", type(champion_detail))

with request.urlopen(champion_dict_url) as response:
    source = response.read()
    champion_detail = json.loads(source)
print(champion_detail)
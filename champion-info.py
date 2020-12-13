import requests
import urllib.request as request
from lxml import html
import json
def champion_info():
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

    with request.urlopen(champion_dict_url) as response:
        source = response.read()
        champion_detail = json.loads(source)
    champion_data = champion_detail["data"][champion_name]

    champion_stats = champion_detail["data"][champion_name]["stats"]
    # print(champion_stats)

    champion_spells = champion_detail["data"][champion_name]["spells"]
    print("===Champion Info===\n")
    # todo: add champion stats info, also check if more level info need to be added
    # print("\n" + str(champion_stats) + "\n")
    for spell in range(3):
        print(                                   str(champion_spells[spell]["id"]) + ": " + str(champion_spells[spell]["name"]))
        print("Spell cooldown per level: " + str(champion_spells[spell]["cooldown"]))
        print("Spell cost per level    : " + str(champion_spells[spell]["costBurn"]))
        print("Spell range per level   : " + str(champion_spells[spell]["range"]) + "\n")
        # print("\n")


while True:
    champion_info()
    repeat = input("Press enter to select a new champion.")
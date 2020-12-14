import urllib.request as request
import json
import re

def champion_info():
    # setup initial lol version check url
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    with request.urlopen(version_url) as response:
        source = response.read()
        version_list = json.loads(source)
    # get latest version number
    current_version = version_list[0]


    # get champion list
    champion_list_url = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/data/en_US/champion.json"
    print(champion_list_url)
    with request.urlopen(champion_list_url) as response:
        source = response.read()
        champion_dict = json.loads(source)
    champion_dict = champion_dict["data"]
    # print(champion_dict)

    # return dict key value
    def getList(dict):
        return list(dict.keys())

    champion_list = getList(champion_dict)
    # print(champion_list)
    index = 0
    for champion in champion_list:
        print(str(index) + ": " + champion)
        index += 1

    print("\nCurrent League of Legends version is: " + current_version)
    # get champion info

    while True:
        while True:
            try:
                # todo: smart champion name input method
                champion_name = input("Please input champion name or index number: ").capitalize()
                if not re.search('[a-zA-Z]', champion_name):
                    champion_name = champion_list[int(champion_name)]

                print("Champion name: ", champion_name)
                champion_dict_url = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/data/en_US/champion/" + champion_name + ".json"
                # print(champion_dict_url)
                with request.urlopen(champion_dict_url) as response:
                    source = response.read()
                    champion_detail = json.loads(source)
                champion_data = champion_detail["data"][champion_name]
                break
            except:
                print("Please enter correct champion name or index number.")

        champion_stats = champion_detail["data"][champion_name]["stats"]
        # print(champion_stats)

        champion_spells = champion_detail["data"][champion_name]["spells"]
        print("===Champion Info===\n")
        # todo: add champion stats info, also check if more level info need to be added
        # print("\n" + str(champion_stats) + "\n")

        spell_list = ["Q", "W", "E", "R"]
        for spell in range(4):
            print(spell_list[spell] + ": " + str(champion_spells[spell]["id"]) + " - " + str(champion_spells[spell]["name"]))
            print("CD   : " + str(champion_spells[spell]["cooldown"]))
            print("Cost : " + str(champion_spells[spell]["costBurn"]))
            print("Range: " + str(champion_spells[spell]["range"]) + "\n")
            # print("\n\n")


champion_info()
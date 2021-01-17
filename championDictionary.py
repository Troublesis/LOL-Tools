'''
===================================================================================================
                         This is League of Legends Champion Library                                                                          
                           The key of the dictionary is the champion name 
                           The Value of the key is different skin image file names
                           If more skins updated                                                                      
                           Enter new champion skins follow by the key (champion name)                 
                                                                                                   

===================================================================================================
'''

import os
champion_dict = {}
# path = os.path.join(os.path.abspath(__file__), 'Champion Icon')
championIconFolder = os.path.dirname(os.path.abspath(__file__))
championIconFolder = championIconFolder + "/Champion Icon/"
# championIconFolder = championIconFolder.replace('\\','/')

championNameList = os.listdir(championIconFolder)
# print(championIconFolder)

for championName in championNameList:
  try:
    skinList = os.listdir(os.path.join(championIconFolder, championName))
    champion_dict.update({championName:skinList})
    # print(skinList)
  except:
    continue

# print(championDict)
# /Volumes/Google/Bamboo/Cloud Doc/Code/Python/PyCharmProjects/LOL-Tools/Champion Icon/Aatrox
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
championIconFolder = os.path.dirname(os.path.abspath( __file__ ))+'/'+'Champion Icon/'
championIconFolder = championIconFolder.replace('\\','/')

championNameList = os.listdir(championIconFolder)
# print(championIconFolder)

for championName in championNameList:
  skinList = os.listdir(championIconFolder+championName)
  champion_dict.update({championName:skinList})
  # print(skinList)

# print(championDict)

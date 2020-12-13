import os
import shutil
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image
from pynput.keyboard import Key, Controller

from championDictionary import champion_dict


'''
===================================================================================================
                                       lolDetectGameMode                                                            
                         This function will detect the League of Legends video game mode                                                  
                              based on the grass pixel color percentage in the video frame                                                                  
                               to determine normal or aram                                                                    
                                                                                                   
                              Function will return the pixel color percentage  eg. 17.5                       
===================================================================================================
'''

def lolDetectGameMode(source,videoName,frameImagePath):

    print('===> Checking GameMode')
    
    cap= cv2.VideoCapture(source+videoName)
    ret, frame = cap.read()

    cv2.imwrite(frameImagePath,frame)

    cap.release()
    cv2.destroyAllWindows()  


    img = cv2.imread(frameImagePath)

    # league of legends green (grass) pixel RGB color
    pixelColor = [54, 77, 30]  # RGB
    #  Pixel RGB tolerance
    diff = 20
    boundaries = [([pixelColor[2]-diff, pixelColor[1]-diff, pixelColor[0]-diff],
                [pixelColor[2]+diff, pixelColor[1]+diff, pixelColor[0]+diff])]
    # in order BGR as opencv represents images as numpy arrays in reverse order

    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        ratio_pixelColor = cv2.countNonZero(mask)/(img.size/3)
        pixelColorPercentage = np.round(ratio_pixelColor*100, 2)
        print('===> grass pixel percentage: ', pixelColorPercentage)
    return pixelColorPercentage

############################### FUNCTION END ###############################


'''
===================================================================================================
                                       lolChampionIconCrop                                                            
                         This function will crop champion icon image from a bigger image                                                                          
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
===================================================================================================
'''

def imageCrop(sourceImageFilePath,sourceFolderPath, leftPercent, topPercent, rightPercent, bottomPercent,resultImageFileName):
   
    # Opens a image in RGB mode
    frameImage = Image.open(sourceImageFilePath)  
    # Size of the image in pixels (size of original image)
    # (This is not mandatory) 
    width, height = frameImage.size 

    # Setting the points for cropped image 
    left = leftPercent*width
    top = topPercent*height
    right = rightPercent*width
    bottom = bottomPercent*height
    # print(left,top,right,bottom)
    
    # Cropped image of above dimension 
    # (It will not change original image)
    croppedImage = frameImage.crop((left, top, right, bottom))
    
    # Shows the image in image viewer 
    # im1.show() 

    return croppedImage.save(sourceFolderPath+resultImageFileName, 'JPEG')
############################### FUNCTION END ###############################

'''
===================================================================================================
                                           lolDetectChampion                                                        
                               This function will compare champion icon image with the video frame                                                                    

                                if will return the counter when match found                                                                   
                                                                                                   
                                                              
===================================================================================================
'''

def lolDetectChampion(mainImage, championIconFolder, source, threshold, gameMode, championName, championIconSkinName, gameModeDestination, videoFolderName):

    # set champion icon file path
    championIconPath = championIconFolder+championName+'/'+championIconSkinName

    # Read the main image 
    img_rgb = cv2.imread(mainImage)

    # Convert it to grayscale 
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    # Read the template 
    template = cv2.imread(championIconPath,0)
    # Store width and height of template in w and h 
    w, h = template.shape[::-1]
    
    # Perform match operations. 
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 
    
    # Specify a threshold 
    # threshold = 0.7
    
    # Store the coordinates of matched area in a numpy array 
    loc = np.where( res >= threshold)  
    
    # Draw a rectangle around the matched region. 
    counter = 0
    for pt in zip(*loc[::-1]): 
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
        counter += 1
    # Show the final image with the matched area. 
    # cv2.imshow('Detected',img_rgb) 

    # when the match champion found ===> store the file
    if counter > 0:
        dest_folder = gameModeDestination+championName+'/'+videoFolderName
        dest = shutil.move(source, dest_folder)
        print('===> This champion is: ', championName)
        print('===> Folder moved to: ', dest_folder)
        print('Done\n\n-------------------------')

        return counter        
    else: 
        return counter
    ##################################################################


def overwolf_lol_videos_sort():
    file_moved = 0
    champion_not_found = 0
    champion_icon_folder = os.path.dirname(os.path.abspath(__file__)) + '/' + 'Champion Icon/'
    champion_icon_folder = champion_icon_folder.replace('\\', '/')
    # initial root folder setting

    # input the root folder path of where you store all of your recorded League of Legends videos
    # root_folder = input('Please enter the source folder path (Sample: w:/Videos/Video Records/Games/Overwolf/Game Summary/League of Legends/): ')
    # enable the following line and comment the upper line if you don't want to enter the folder path every time
    root_folder = 'F:/bambo/Videos/Overwolf/Game Summary/League of Legends/'
    # root_folder = 'w:/Videos/Video Records/Games/Overwolf/Game Summary/League of Legends/'
    # sort_folder = input('Please enter the new folder path where you want to store League of Legends Game Videos (Sample: w:/Videos/Video Records/Games/Overwolf/Game Summary/Sorted/): ')

    sort_folder = 'F:/bambo/Videos/Overwolf/Game Summary/League of Legends Sorted/'
    # sort_folder = 'w:/Videos/Video Records/Games/Overwolf/Game Summary/'
    normal_game_mode_destination = sort_folder + 'Normal/'
    aram_game_mode_destination = sort_folder + 'ARAM/'

    # root_folder = inputSourceFolder.replace('\\','/')+'/'
    # return the correct format for root folder path
    print('Your root folder is: ', root_folder)
    print('========================================\n')

    ##################################################################

    folderList = os.listdir(root_folder)
    print('Folders List for your root folder is: \n', folderList)
    print('========================================\n')
    # source = os.path.dirname(os.path.abspath( __file__ ))+'/'

    # undefined champion icon index number for rename the undefined champion icon images cropped from the video frame
    undefinedChampionIndex = 0

    # loop to check each folder inside the root folder
    for folderName in folderList:
        # if '.' not in folderName:

        # get the folder path of each folder inside the root folder
        source = root_folder + folderName + '/'
        print('===> Checking folder: ' + source)

        # todo: still working on these lines... need to fix if there was no file found in the selected folder
        # select a video inside the folder

        file_list = os.listdir(source)
        # print(file_list)
        video_name = 0
        for fileName in file_list:
            if '.mp4' in fileName:
                video_name = fileName
                print('video_name' + video_name)
                break

        frame_image_name = 'frame.jpg'
        video_frame_file_path = source + frame_image_name
        try:
            pixel_color_percentage = lolDetectGameMode(source, video_name, video_frame_file_path)
        except WindowsError:
            break

        champion_icon_file_name = 'championIcon.jpg'
        champion_icon_file_path = source + champion_icon_file_name
        champion_icon_area_file_name = 'championIconArea.jpg'
        champion_icon_area_file_path = source + champion_icon_file_name
        print('===> championIcon.jpg stored at: ' + champion_icon_file_path)
        print('')
        # get the video frame image file path

        # set the crop coordinates in order to crop a champion icon image from the captured champion frame
        left_percent = 0.2
        top_percent = 0.85
        right_percent = 0.4
        bottom_percent = 1

        # lolChampionIconCrop will crop a champion icon image from frame.jpg and save it in video folder
        imageCrop(video_frame_file_path, source, left_percent, top_percent, right_percent, bottom_percent,
                  champion_icon_area_file_name)
        left = 385 / 1280
        top = 643 / 720
        right = 433 / 1280
        bottom = 683 / 720

        imageCrop(video_frame_file_path, source, left, top, right, bottom, champion_icon_file_name)

        # set initial value of variable championFound as 0 for break a loop when champion detected
        championFound = 0
        # set initial value of champion skin icon index as 0 for counting how many skins for each champion stored in our champion dictionary
        champion_skin_icon_index = 0
        # get the total number of champion skins
        # total_number_of_skins = len(champion_dict)

        # loop to check all of champion name in champion dictionary
        for champion_name in champion_dict:
            # get the current name of champion skin in the loop
            # name_of_champion_skins = len(champion_dict[champion_name])
            # loop to check all of skins for each champion
            for skin in champion_dict[champion_name]:
                # when champion is found, break the loop
                if championFound > 0:
                    # championFound = 0
                    print('current skin is: ', skin)
                    file_moved += 1
                    break
                # print current comparing skin name
                skin_name = champion_dict[champion_name][champion_skin_icon_index]
                print('===> Comparing ' + skin_name)
                # when game mode is normal
                if pixel_color_percentage > 2:
                    # set normal game video store location
                    # normal_game_mode_destination = 'F:/bambo/Videos/Overwolf/Game Summary/Normal/'
                    # run function lolDetectChampion
                    championFound = lolDetectChampion(champion_icon_area_file_path, champion_icon_folder,
                                                      source, 0.9,
                                                      'normal', champion_name, skin_name,
                                                      normal_game_mode_destination, folderName)
                    # when game mode is aram

                elif pixel_color_percentage < 2:
                    # set normal game video store location
                    # aram_game_mode_destination = 'F:/bambo/Videos/Overwolf/Game Summary/ARAM/'
                    # run function lolDetectChampion
                    championFound = lolDetectChampion(champion_icon_area_file_path, champion_icon_folder,
                                                      source, 0.9,
                                                      'aram', champion_name, skin_name,
                                                      aram_game_mode_destination,
                                                      folderName)

                else:
                    print('===> Game Mode Undefined')
                    champion_not_found += 1
                    break
                # todo: these lines might have some issue.
                # when all of champion skins have been checked move the undefined champion icon
                if champion_name == list(champion_dict.keys())[-1]:
                    if skin_name == champion_dict[list(champion_dict.keys())[-1]][len(champion_dict[champion_name]) - 1]:
                        undefinedChampionIconFolder = sort_folder
                        # undefinedChampionIconFolder = champion_icon_folder
                        try:
                            os.rename(champion_icon_file_path,
                                      undefinedChampionIconFolder + 'undefinedChampion' + str(
                                          undefinedChampionIndex) + '.jpg')
                            os.rename(video_frame_file_path,
                                      undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
                                          undefinedChampionIndex) + '.jpg')
                            print('===> Undefined champion icon moved to: ', champion_icon_folder)
                            print('\n\n------------------------->')

                        except WindowsError:
                            os.remove(undefinedChampionIconFolder + 'undefinedChampion' + str(
                                undefinedChampionIndex) + '.jpg')
                            os.remove(undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
                                undefinedChampionIndex) + '.jpg')
                            os.rename(champion_icon_file_path,
                                      undefinedChampionIconFolder + 'undefinedChampion' + str(
                                          undefinedChampionIndex) + '.jpg')
                            os.rename(video_frame_file_path,
                                      undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
                                          undefinedChampionIndex) + '.jpg')
                        undefinedChampionIndex += 1
                        print('===> Undefined champion icon moved to: ', champion_icon_folder)
                        print('\n\n------------------------->')

                champion_skin_icon_index += 1

            champion_skin_icon_index = 0
    print('Total number of file moved: ', file_moved)
    print('Total number of champion icon undefined: ', champion_not_found)


def takeScreenShot(screenshotsFolderPath, screenshotName):
    my_screenshot = pyautogui.screenshot()
    screenshotsFolderPath = screenshotsFolderPath.replace('\\', '/')
    screenshotFilePath = screenshotsFolderPath + screenshotName
    my_screenshot.save(screenshotFilePath)

def compareImage(mainImageFilePath, templateImageFilePath, threshold):
    # Read the main image
    img_rgb = cv2.imread(mainImageFilePath)

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Read the template
    template = cv2.imread(templateImageFilePath, 0)
    # Store width and height of template in w and h
    w, h = template.shape[::-1]

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    # threshold = 0.9

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region.
    matchFound = 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        matchFound += 1
    # Show the final image with the matched area.
    # cv2.imshow('Detected',img_rgb)

    # when the match champion found ===> store the file
    return matchFound, loc


def lol_call_position():

    print('''
    ===================================================================================================
         This is a little script which will automatically call league of legends position for you                                                                       
                   Step 1: select which position you want to play from the list
                   Step 2: start a game, leave the league of legends windows open your computer                                                                                    
                   Step 3: the script will automatically search the game accept button every 5 seconds
                           once the game is found, script will press the accept button for you
                           Once you are in the game, it will automatically search the chat box and 
                           enter the position you selected for 3 times, after once second it will enter
                           the position once again
                   Step 4: once the script is done, you can enter 0 to start over the script                      
                           or enter any other value to exit the script.                                                                                                                                                                         
    ===================================================================================================
    ''')

    # stage 1 - choose position which you want to call
    stage = 1
    # while loop = 0 keep the script running
    loop = '0'
    while loop == '0':
        # when stage 1 - choose position which you want to call
        if stage == 1:
            # position dictionary
            positionDict = {'1': 'Top Please', '2': 'Mid Please', '3': 'Jungle Please', '4': 'Bot Please',
                            '5': 'Duo Bot Please', '6': 'Fill'}
            # print(positionDict)
            print(positionDict)
            select = input('Select which position you want to play from 1 - 6, then press enter: ')
            # set position
            position = positionDict[select]
            print('You have selected ===> ', position)

        # set screenshot template image files path
        screenshotsFolderPath = os.path.dirname(os.path.abspath(__file__)) + '/' + 'Screenshots/'
        matchFound = 0
        counter = 0
        acceptButtonFilePath = screenshotsFolderPath + 'acceptButton.jpg'
        screenshotsFolderPath = os.path.dirname(os.path.abspath(__file__)) + '/' + 'Screenshots/'
        screenshot_name = 'screenshot.jpg'
        screenshotFilePath = screenshotsFolderPath + screenshot_name
        # search for the accept button
        while matchFound == 0:
            # stage 2 - search accept button
            stage = 2
            takeScreenShot(screenshotsFolderPath, screenshot_name)
            matchFound, loc = compareImage(screenshotFilePath, acceptButtonFilePath, 0.9)
            # if match is found, press the accept button, start search champion select lobby
            if matchFound > 0:
                x = loc[1][0]
                y = loc[0][0]
                print('found at ', x, y)
                pyautogui.click(x + 100, y + 30)
                chatBoxTemplateFilePath = screenshotsFolderPath + 'championSelectLobby.jpg'
                screenshotName1 = 'chat_box.jpg'
                screenshotFilePath1 = screenshotsFolderPath + screenshotName1
                # search champion select lobby in 10 seconds, if not found, maybe someone decline the game or someone else forget to click on accept button
                # start to search the accept button again.
                for timer in range(0, 10):
                    stage = 3
                    takeScreenShot(screenshotsFolderPath, screenshotName1)
                    chat_box, pos = compareImage(screenshotFilePath1, chatBoxTemplateFilePath, 0.9)
                    # once the champion select lobby is found, call position in chat box.
                    if chat_box > 0:

                        x_pos = pos[1][0]
                        y_pos = pos[0][0]
                        print('found at ', x_pos, y_pos)
                        pyautogui.click(x_pos, y_pos + 830)

                        for a in range(0, 3):
                            keyboard = Controller()
                            keyboard.type(position)
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            time.sleep(0.5)
                            print('call position for first times')
                        # wait for 1 second and enter the position again.
                        time.sleep(1)
                        keyboard.type(position)
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                        print('call position for second time')
                        # decision to run the script again
                        loop = input('Enter 0 to call another position, any other number to EXIT\n')
                        stage = 1
                        matchFound = 1
                        break
                    else:
                        print('===> Searching Chat Box')
                        time.sleep(1)
            else:
                print('===> Searching Accept Button ', counter)
                counter += 1
                time.sleep(5)
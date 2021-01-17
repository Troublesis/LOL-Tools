import os
import re
import shutil
import time
from multiprocessing import Pool
from functools import partial
import multiprocessing
import cv2
import numpy as np
from PIL import Image
import gevent.pool
import gevent.monkey

import datetime

now = datetime.datetime.now()
timenow = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)

gevent.monkey.patch_all()

from championDictionary import champion_dict

# todo: change source folder path
source_folder = "/Volumes/F/Videos/Overwolf/Outplayed/League of Legends/"

normal_game_mode_destination = source_folder + 'Normal/'
aram_game_mode_destination = source_folder + 'ARAM/'


def imageCrop(source_file_path, leftPercent, topPercent, rightPercent, bottomPercent,
              resultImageFileName):
    file_folder = os.path.dirname(os.path.abspath(source_file_path))
    if resultImageFileName not in os.listdir(file_folder):

        # Opens an image in RGB mode
        frame_img_path = os.path.join(file_folder, "frame.jpg")
        frameImage = Image.open(frame_img_path)
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        width, height = frameImage.size

        # Setting the points for cropped image
        left = leftPercent * width
        top = topPercent * height
        right = rightPercent * width
        bottom = bottomPercent * height
        # print(left,top,right,bottom)

        # Cropped image of above dimension
        # (It will not change original image)
        croppedImage = frameImage.crop((left, top, right, bottom))

        # Shows the image in image viewer
        # im1.show()
        result_image_path = os.path.join(file_folder + "/" + resultImageFileName)
        print('===>image saved: %s' % result_image_path)
        return croppedImage.save(result_image_path, 'JPEG')
    else:
        # print('===>image file already cropped\n')
        pass


def lolDetectChampion(mainImage, championIconFolder, source, threshold, gameMode, championName, championIconSkinName,
                      gameModeDestination, videoFolderName):
    # set champion icon file path
    championIconPath = championIconFolder + championName + '/' + championIconSkinName

    # Read the main image
    img_rgb = cv2.imread(mainImage)

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Read the template
    template = cv2.imread(championIconPath, 0)
    # Store width and height of template in w and h
    w, h = template.shape[::-1]

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    # threshold = 0.7

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # Draw a rectangle around the matched region.
    counter = 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        counter += 1
    # Show the final image with the matched area.
    # cv2.imshow('Detected',img_rgb)

    # when the match champion found ===> store the file
    if counter > 0:
        dest_folder = gameModeDestination + championName + '/' + videoFolderName
        dest = shutil.move(source, dest_folder)
        print('===> This champion is: ', championName)
        print('===> Folder moved to: ', dest_folder)
        print('Done\n\n-------------------------')

        return counter
    else:
        return counter
    ##################################################################


def get_frame_from_video(video_path, video_folder):
    # get an image from video
    cap = cv2.VideoCapture(video_path)
    frame_no = 300
    cap.set(1, frame_no)
    ret, frame = cap.read()
    # save image
    frame_img_path = os.path.join(video_folder, "frame.jpg")
    print('===> frame: %s\n' % frame_img_path)
    cv2.imwrite(frame_img_path, frame)

    cap.release()
    cv2.destroyAllWindows()
    return frame_img_path


def lolDetectGameMode(video_path):
    # print('===> detecting: %s\n' % video_path)
    folder_file_list = os.listdir(os.path.dirname(os.path.abspath(video_path)))
    video_folder = os.path.dirname(os.path.abspath(video_path))
    # print(video_folder)

    if "frame.jpg" not in folder_file_list:
        print('===> getting video frame: \n', video_path)
        frame_img_path = get_frame_from_video(video_path, video_folder)
    else:
        # print('===>frame already exist\n')
        frame_img_path = os.path.join(video_folder, "frame.jpg")
        pass
    img = cv2.imread(frame_img_path)

    # league of legends green (grass) pixel RGB color
    pixelColor = [54, 77, 30]  # RGB
    #  Pixel RGB tolerance
    diff = 20
    boundaries = [([pixelColor[2] - diff, pixelColor[1] - diff, pixelColor[0] - diff],
                   [pixelColor[2] + diff, pixelColor[1] + diff, pixelColor[0] + diff])]
    # in order BGR as opencv represents images as numpy arrays in reverse order

    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        ratio_pixelColor = cv2.countNonZero(mask) / (img.size / 3)
        pixelColorPercentage = np.round(ratio_pixelColor * 100, 2)
        # print('===> grass pixel percentage: %s\n' % pixelColorPercentage)

    with open(os.path.join(video_folder, "result.txt"), 'w', encoding='utf-8') as f:
        f.write("Result generated by: " + timenow)
        f.write('\n===> grass pixel percentage: %s\n' % pixelColorPercentage)
        f.write('\n')
    return pixelColorPercentage


def get_videos_path(source_folder):
    videos_list = []
    for f in os.listdir(source_folder):
        folder_name_matched = re.search(
            r"^League of Legends_[0-9]{0,2}-[0-9]{0,2}-[0-9]{0,4}_[0-9]{0,2}-[0-9]{0,2}-[0-9]{0,2}-[0-9]{0,3}$",
            f)
        if folder_name_matched is not None:
            # print('===> folder name:', f)
            video_folder = os.listdir(os.path.join(source_folder, f))
            for v in video_folder:
                # print('===> video name:', v)
                if 'mp4' in v:
                    # print('===> video:', v)
                    videos_path = os.path.join(source_folder, f, v)
                    videos_list.append(videos_path)

                else:
                    pass
        else:
            pass
    return videos_list


def main():
    # create new folder in source folder
    try:
        new_folder_name = source_folder + "sorted"
        os.mkdir(new_folder_name)
    except:
        pass
    # print('===> ', os.listdir(source_folder))

    # get folder list from source folder
    videos = get_videos_path(source_folder)
    print("===> folder number:", len(videos))

    jobs = [gevent.spawn(lolDetectGameMode, v) for v in videos]
    gevent.joinall(jobs)

    # check game mode

    file_moved = 0
    champion_not_found = 0
    champion_icon_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Champion Icon/')
    # champion_icon_folder = champion_icon_folder.replace('\\', '/')

    champion_icon_file_name = 'championIcon.jpg'
    champion_icon_file_path = os.path.join(source_folder + champion_icon_file_name)
    champion_icon_area_file_name = 'championIconArea.jpg'
    champion_icon_area_file_path = os.path.join(source_folder + champion_icon_file_name)
    # print('===> championIcon.jpg stored at: ' + champion_icon_file_path)
    # get the video frame image file path

    # set the crop coordinates in order to crop a champion icon image from the captured champion frame
    # lolChampionIconCrop will crop a champion icon image from frame.jpg and save it in video folder

    jobs = [gevent.spawn(imageCrop, f, 0.2, 0.85, 0.4, 1,
                         champion_icon_area_file_name) for f in videos]
    gevent.joinall(jobs)

    jobs = [gevent.spawn(imageCrop, f, 422 / 1280, 658 / 720, 457 / 1280, 693 / 720,
                         champion_icon_file_name) for f in videos]
    gevent.joinall(jobs)

    # set initial value of variable championFound as 0 for break a loop when champion detected
    championFound = 0
    # set initial value of champion skin icon index as 0 for counting how many skins for each champion stored in our champion dictionary
    champion_skin_icon_index = 0
    # get the total number of champion skins
    # total_number_of_skins = len(champion_dict)
    # print('===>', champion_dict)
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
    #         if pixel_color_percentage > 2:
    #             # set normal game video store location
    #             # normal_game_mode_destination = 'F:/bambo/Videos/Overwolf/Game Summary/Normal/'
    #             # run function lolDetectChampion
    #             championFound = lolDetectChampion(champion_icon_area_file_path, champion_icon_folder,
    #                                               source, 0.9,
    #                                               'normal', champion_name, skin_name,
    #                                               normal_game_mode_destination, folderName)
    #             # when game mode is aram
    #
    #         elif pixel_color_percentage < 2:
    #             # set normal game video store location
    #             # aram_game_mode_destination = 'F:/bambo/Videos/Overwolf/Game Summary/ARAM/'
    #             # run function lolDetectChampion
    #             championFound = lolDetectChampion(champion_icon_area_file_path, champion_icon_folder,
    #                                               source, 0.9,
    #                                               'aram', champion_name, skin_name,
    #                                               aram_game_mode_destination,
    #                                               folderName)
    #
    #         else:
    #             print('===> Game Mode Undefined')
    #             champion_not_found += 1
    #             break
    #         # todo: these lines might have some issue.
    #         # when all of champion skins have been checked move the undefined champion icon
    #         if champion_name == list(champion_dict.keys())[-1]:
    #             if skin_name == champion_dict[list(champion_dict.keys())[-1]][len(champion_dict[champion_name]) - 1]:
    #                 undefinedChampionIconFolder = sort_folder
    #                 # undefinedChampionIconFolder = champion_icon_folder
    #                 try:
    #                     os.rename(champion_icon_file_path,
    #                               undefinedChampionIconFolder + 'undefinedChampion' + str(
    #                                   undefinedChampionIndex) + '.jpg')
    #                     os.rename(video_frame_file_path,
    #                               undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
    #                                   undefinedChampionIndex) + '.jpg')
    #                     print('===> Undefined champion icon moved to: ', champion_icon_folder)
    #                     print('\n\n------------------------->')
    #
    #                 except WindowsError:
    #                     os.remove(undefinedChampionIconFolder + 'undefinedChampion' + str(
    #                         undefinedChampionIndex) + '.jpg')
    #                     os.remove(undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
    #                         undefinedChampionIndex) + '.jpg')
    #                     os.rename(champion_icon_file_path,
    #                               undefinedChampionIconFolder + 'undefinedChampion' + str(
    #                                   undefinedChampionIndex) + '.jpg')
    #                     os.rename(video_frame_file_path,
    #                               undefinedChampionIconFolder + 'undefinedChampionFrame' + str(
    #                                   undefinedChampionIndex) + '.jpg')
    #                 undefinedChampionIndex += 1
    #                 print('===> Undefined champion icon moved to: ', champion_icon_folder)
    #                 print('\n\n------------------------->')
    #
    #         champion_skin_icon_index += 1
    #
    #     champion_skin_icon_index = 0
    #
    #
    # print('Total number of file moved: ', file_moved)
    # print('Total number of champion icon undefined: ', champion_not_found)

    start = time.time()
    print("花费时间: %s" % (time.time() - start))


if __name__ == "__main__":
    main()

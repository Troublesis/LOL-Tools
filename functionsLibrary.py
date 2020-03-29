
import cv2
import os 
import shutil
import numpy as np
from PIL import Image

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
    #  Pixel RGB tolerence
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
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = frameImage.size 

    # Setting the points for cropped image 
    left = leftPercent*width
    top = topPercent*height
    right = rightPercent*width
    bottom = bottomPercent*height
    # print(left,top,right,bottom)
    
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    croppedImage = frameImage.crop((left, top, right, bottom))
    
    # Shows the image in image viewer 
    # im1.show() 

    return croppedImage.save(sourceFolderPath+resultImageFileName,'JPEG')
############################### FUNCTION END ###############################

'''
===================================================================================================
                                           lolDetectChampion                                                        
                               This function will compare champion icon image with the video frame                                                                    

                                if will return the counter when match found                                                                   
                                                                                                   
                                                              
===================================================================================================
'''

def lolDetectChampion(mainImage,championIconFolder, source, threshold, gameMode, championName, championIconSkinName, gameModeDestination, videoFolderName):

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
        destFolder = gameModeDestination+championName+'/'+videoFolderName 
        dest = shutil.move(source, destFolder)
        print('===> This champion is: ', championName)
        print('===> Folder moved to: ', destFolder)
        print('Done\n\n-------------------------')
        return counter        
    else: 
        return counter
    ##################################################################




import time

from functionsLibrary import lol_call_position
from functionsLibrary import overwolf_lol_videos_sort


def menu():
    print('Description - lol tools. \n')
    while True:
        print('-----------------------------------------------\n1.auto lol video category\n2.call position'
              '\n3.FUnction3\n4.FUnction4\nInput any other number '
              'to EXIT\n')
        choice = int(input('Select a number to choose the function：'))
        if choice == 1:
            overwolf_lol_videos_sort()
            start = time.time()
            print("花费时间: %s" % (time.time() - start))
        elif choice == 2:
            lol_call_position()
        elif choice == 3:
            time.sleep(1)
        elif choice == 4:
            time.sleep(1)
        else:
            print('\n---------------------\nThanks for using the system, bye!')
            break


menu()

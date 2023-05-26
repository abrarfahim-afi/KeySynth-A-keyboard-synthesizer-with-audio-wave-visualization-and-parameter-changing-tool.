# This program is created to set the counter number which are described before audio file name.
# Here the files are saved as 1KeySynth_pian.py where 1 is the counter value 
# The counter value is increased by 1 with each time the main file is played.
# The previous_counter() function is called when the spectrogram of the previously saved composition needs to be played
# When the program is used to create a new composition the update_counter function is utilized. Which updates the counter value by 1

# If the counter.txt file is empty then the program adds a zero to the txt file.   

import os

# if os.path.exists('counter.txt') and os.stat('counter.txt').st_size == 0:  # Sees if the file counter.txt exists and is empty .
#   print('File is empty')
# else:
#     print('x')

def previous_counter():
    if os.stat('counter.txt').st_size == 0:  # Sees if the file counter.txt is empty or not. 
        print('File is empty')
        myfile = open('counter.txt','r+')
        myfile.write(str(0) + '\n')  # If the text file is empty it add a 0 and a new line to it
        myfile.close()
    myfile = open('counter.txt','r+')
    for line in myfile:
                x = line
                #print(x)
    myfile.close()
    return x.strip('\n')

def update_counter(x):
    # print('this is a valid counter:', x)
    myfile = open('counter.txt','a')
    myfile.write(str(x) + '\n')
    myfile.close()



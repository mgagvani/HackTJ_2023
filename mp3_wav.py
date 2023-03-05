# script to convert mp3 to wav

import os
import glob

for file in glob.glob("*.mp3"):
    print(file.split("."))
    # print command before executing
    before_string = '"' + file.split(".")[0] + ".mp3" + '"'
    after_string = '"' + file.split(".")[0] + ".wav" + '"'
    print(before_string, after_string)
    

    # execute command
    os.system("ffmpeg -i " + before_string + " " + after_string)
# Hack TJ code to generate audio files

from gtts import gTTS
  
# This module is imported so that we can 
# play the converted audio
import os
  
# The text that you want to convert to audio
mytext = 'Hi Zani'
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome 
# myobj.save("welcome.mp3")

with open("labels.txt") as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

for i, item in enumerate(lines):
    if i < 60: # sea snake
        continue
    print(x:=item.split(","))
    print(x[0])
    myobj = gTTS(text=x[0], lang=language, slow=False)
    myobj.save(item + ".mp3")
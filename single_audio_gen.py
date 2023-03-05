from gtts import gTTS
import os

mytext = "person"
    
# Language in which you want to convert
language = 'en'
  
myobj = gTTS(text=mytext, lang=language, slow=False)
  
myobj.save("person.mp3")

os.system("ffmpeg -i person.mp3 person.wav") # convert mp3 to wav
 

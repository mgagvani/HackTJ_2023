# AUDVI - AI Arduino Object Detector for the Visually Impaired

### AUDVI is a cost-effective, 100% offline aid for helping the visually impaired see the world around them. By using low-power MCUs, users don't need to recharge the device or plug in it frequently.

![img](/path/to/file)![img](/path/to/file)![1677986646458](image/README/1677986646458.png)![](/path/to/file)![](/path/to/file)

#### Setup

Materials:

1. [Maixduino](https://github.com/sipeed/Maixduino) (Arduino clone w/ AI capabilities, costs around $5)
2. Speaker module
3. A computer
4. A microSD card

Procedure:

* You need the [MaixPy IDE](https://wiki.sipeed.com/soft/maixpy/en/get_started/env_maixpyide.html) to upload code
* Use the kflash_gui tool to flash the **minimal** firmware. Other firmware won't work because there won't be enough space to run the AI model 😀
* Connect the speaker module to the pins on the Maixduino. The board has a power amplifier and DAC built in so an external one is not necessary.
* ![image](https://user-images.githubusercontent.com/37602685/222934944-0c40826c-569d-4967-943b-359f84c0d541.png)
* Download the offical mobilenet.kmodel file and unzip it (use 7-zip or a similar tool). You will see a \*.kmodel file is inside. Clone this repo, and put the files in /audio in a corresponding /audio folder on the SD card. (If you are low on space, you just need the .wav files). Also put the .kmodel file in the root of the SD card along with [labels.txt](https://github.com/sipeed/MaixPy_scripts/blob/master/machine_vision/mobilenet_1000_class/labels.txt).
* Upload any short .wav file (~5 seconds or less) as "small.wav" to the root of the SD card.
* Run boot.py. ou should hear the sound of "small.wav" as it starts up. Wait approximately 10 seconds for the MobileNet model to initialize. Then the speaker will start saying what it recognizes!

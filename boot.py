from fpioa_manager import *
from Maix import I2S, GPIO, utils
import audio
import os

import sensor, image, lcd, time
import KPU as kpu
import gc, sys
import machine

def main(labels = None, model_addr="/sd/m.kmodel", lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    gc.collect()

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        raise Exception("no labels.txt")

    task = kpu.load(model_addr)

    counter = 0

    try:
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            fmap = kpu.forward(task, img)
            t = time.ticks_ms()
            plist=fmap[:]
            pmax=max(plist)
            max_index=plist.index(pmax)
            if counter % 2 == 0:
                img.draw_string(0,0, "%.2f\n%s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
                img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
                lcd.display(img)
                print(labels[max_index].strip())
            # turn on the audio
            player = audio.Audio(path="/sd/audio/"+labels[max_index].strip()+".wav")
            player.volume(99)
            wav_info = player.play_process(wav_dev)
            print("wav file head information: ", wav_info)
            # config i2s according to audio info
            wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                                   cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
            wav_dev.set_sample_rate(wav_info[1])

            while True:
                ret = player.play()
                if ret == None:
                    print("format error")
                    break
                elif ret == 0:
                    print("end of: " + labels[max_index].strip())
                    break
            player.finish()

            # get some memory back
            gc.collect()
    except Exception as e:
        sys.print_exception(e)
    finally:
        kpu.deinit(task)


########### settings ############
WIFI_EN_PIN = 8
# AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
# AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
AUDIO_PA_EN_PIN = 2     # Maixduino


# disable wifi
fm.register(WIFI_EN_PIN, fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

# register i2s(i2s0) pin
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)

# init audio
player = audio.Audio(path="/sd/small.wav")
player.volume(80)

# read audio info
wav_info = player.play_process(wav_dev)
print("wav file head information: ", wav_info)

# config i2s according to audio info
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(wav_info[1])

# list all files in the audio directory
# print(os.listdir("/sd/audio"))

# loop to play audio
while True:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret == 0:
        print("end")
        break
player.finish()

if __name__ == "__main__":
    utils.gc_heap_size(256*1024)
    # machine.reset()

    try:
        with open("/sd/labels.txt.txt") as f:
            labels = f.readlines()
        # main(labels=labels, model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)
        main(labels=labels, model_addr="/sd/m.kmodel")
    except Exception as e:
        sys.print_exception(e)
    finally:
        gc.collect()

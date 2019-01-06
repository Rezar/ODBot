import serial, sys, io
import time as simpletime
from random import *
from threading import Condition
from datetime import *

import pyaudio
from pocketsphinx import *

from StateGraph import *
from XMLParser import *

# for speaker
from subprocess import call
cmd_beg= 'espeak '
cmd_end= ' | aplay ./temp_voice_response.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > temp_voice_response.wav ' # To store the voice file
# end of for speaker

# usb core dev
from tuning import Tuning
import usb.core
import usb.util
from usb_pixel_ring_v2 import PixelRing

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
if dev:
    mic = Tuning(dev)
    pixels = PixelRing(dev)
else:
    mic = None
    pixels = None

last_time_motor_moved = 0


def main():
    model_path = get_model_path()
    config = Decoder.default_config()
    # config.set_string('-hmm', os.path.join(model_path, 'en-us'))
    # config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
    # config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
    config.set_string('-hmm', os.path.join(model_path, 'en-us'))
    config.set_string('-lm', '2823.lm')
    config.set_string('-verbose', 'False')
    config.set_string('-dict', '2823.dic')
    config.set_string('-kws', 'keyphrase.list')
    config.set_string('-logfn', '/dev/null')


    graph = XMLParser(graph_file="basic.xml", debug=True).parse()
    arduino = serial.Serial('/dev/ttyACM0', 57600)
    arduino.timeout = 0.1

    # Check currnet state
    print("Current State: {}".format(graph.get_current_state().name))

    decoder = Decoder(config)

    # while True:
    #     simpletime.sleep(0.1)
    #     try:
    #         # arduino_says = arduino.readline()
    #         # if (len(arduino_says) > 0):
    #         #     print('\nRaw: ' + arduino_says)
    #         # arduino_says = arduino_says.replace('\r', '')
    #         # arduino_says = arduino_says.replace('\n', '')
    #         # if "m:done;" in arduino_says or "e:ready;" in arduino_says:
    #         #     print('Live!')
    #         #     local.arduino_busy = False
    #         # sys.stdout.write(".")
    #         # sys.stdout.flush()
    #     except KeyboardInterrupt:
    #         break

    #src.recursive_stop()


    def on_graph_state_change():
        print("onStateChange()")
        # Runs through state responses
        print("\tNew Current State: {}".format(graph.state))
        print("\tExecuting responses for nextState...")

        if len(graph.state.get_responses()) > 0:
            print('Responses: {}'.format(len(graph.state.get_responses())))
            for response in graph.state.get_responses():
                print('\tRunning Response {}'.format(response))
                # do response action whether it has to do with moving motors, turning led, etc

                if response.typ == ResponseType.GO_TO_STATE:
                    graph.set_current_state(response.value)
                elif response.typ == ResponseType.LED:
                    if pixels is not None:
                        if response.value == 'listening':
                            pixels.think()
                        elif response.value == 'off':
                            pixels.off()
                        elif response.value == 'hello':
                            pixels.speak()
                        elif response.value == 'following':
                            pixels.spin()
                        elif response.value == 'doa':
                            if mic is not None:
                                pixels.wakeup(mic.direction)
                        else:
                            print("Unknown LED value: {} was found.".format(response.value))
                elif response.typ == ResponseType.MOTOR_MOVE:
                    if response.value == 'forward':
                        arduino.write("d:f;")
                    elif response.value == 'stop':
                        arduino.write("d:s;")
                elif response.typ == ResponseType.CAMERA_MOVE:
                    if response.value == 'doa':
                        if mic is not None:
                            voice_direction = mic.direction
                            print "voice from " + str(voice_direction)
                            arduino_command = "m:" + str(voice_direction) + ";"
                            if voice_direction < 180:
                                #voice is coming from behind
                                voice_direction = (voice_direction + 180) % 360
                            else:
                                #voice is coming from in front
                                voice_direction = 90

                        arduino_command = arduino_command + "c:" + str(voice_direction) + ",120;"
                        arduino.write(arduino_command)
                        last_time_motor_moved = simpletime.time()
                        print("@done@")
                elif response.typ == ResponseType.VOICE_RESPONSE:
                    text = response.value.replace(' ', '_')

                    #Calls the Espeak TTS Engine to read aloud a Text
                    call([cmd_beg+cmd_out+text+cmd_end], shell=True)
                else:
                    print("Unused response type: {}.".format(response.typ))
        else:
            print('\tResponding with nothing')

    class local:
        # arduino_busy = True
        voices = {}
        position = None;

    def on_detected(word):
        start = datetime.now()
        if simpletime.time() - last_time_motor_moved > 0.4:
            print("on_detected with word = ")
            graph.apply_action(ActionType.VOICE_COMMAND, word.hypstr)
        else:
            print("on_detected ignored - motor movement")
        print(datetime.now() - start)
        # if 'odd bot' in word.hypstr and 'follow me' in word.hypstr:
        #     pixels.think()
        # else:
        #     print(word.hypstr)
        #     #     print("Arduino is busy. Doing nothing")
        #     #     return
        #     local.position = doa.get_direction()
        #     pixels.wakeup(local.position)
        #     print(datetime.now() - start)
        #     # local.arduino_busy = True
        #     print('\nDirection {}'.format(local.position) + " Sent: " + str(local.position))

        # arduino.write("m:" + str(k) + ";c:" + str(randint(30, 150)) + "," + str(randint(30,150)) + ";")


    graph.set_on_state_change(on_graph_state_change)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    stream.start_stream()

    in_speech_bf = False
    decoder.start_utt()
    while True:
        try:
            buf = stream.read(2048, exception_on_overflow = False)
            if buf:
                decoder.process_raw(buf, False, False)
                if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                        decoder.end_utt()
                        # print 'Result:', decoder.hyp().hypstr
                        on_detected(decoder.hyp())
                        decoder.start_utt()
            else:
                break
        except KeyboardInterrupt:
            break
    decoder.end_utt()




if __name__ == '__main__':
    main()

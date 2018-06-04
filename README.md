# ODBot


## Getting Started
This project uses Seeed Studio's 4 mic hat. For more information on this device, refer to [Seeed studio's wiki page](http://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/) ([Product page](https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi-p-2941.html)).

**Python 2.7** is used for this project and [virtualenv](https://virtualenv.pypa.io/en/stable/) is strongly recommended to isolate python environment.

## Dependencies

 - [Respeaker 4mic hat](https://github.com/respeaker/4mics_hat) - Uses [spidev](https://pypi.python.org/pypi/spidev) and [gpiozero](http://gpiozero.readthedocs.io/). Snowboy and Google Assistant library installation is unnecessary.
 - [Voice-engine](https://github.com/voice-engine/voice-engine) - Used as a voice interface
	 - Voice-engine needs to be modified in order to be used with pocketsphinx in this project. Please refer to instructions below after installation.
 - [Pocketsphinx](https://github.com/cmusphinx/pocketsphinx-python) - Used for STT (Speech-To-Text)
	 - Refer to [CMU Sphinx](https://cmusphinx.github.io/wiki/) for more details



## Driver

 - [seeed-voicecard driver](https://github.com/respeaker/seeed-voicecard) - Drivers for quad AC108 ADC.

## Topology

Voice-engine Audio Feed Flow

```
Source -> ChannelPicker -> PocketSphinx
  |
  V
 DOA
```

Voice Command Flow
```
Human Voice -> Source -> ChannelPicker -> PocketSphinx KWS
                                              /     \
                                            DOA   Serial
```
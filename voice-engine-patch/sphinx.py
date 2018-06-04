# -*- coding: utf-8 -*-

"""
PocketSphinx KWS
"""

import sys
from pocketsphinx import *
from .element import Element
import threading
import time

if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

class Sphinx(Element):
    def __init__(self, config = None):

        super(Sphinx, self).__init__()

        self.queue = queue.Queue()
        self.done = False
        self.on_detected = None

        if config is None:
            model_path = get_model_path()
            config = Decoder.default_config()
            config.set_string('-hmm', os.path.join(model_path, 'en-us'))
            # config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
            config.set_string('-verbose', 'True')
            # config.set_string('-dict', 'dictionary.dict')
            config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
            config.set_string('-kws', 'keyphrase.list')
            # config.set_string('-logfn', '/dev/null')
            # config.set_string('-keyphrase', 'hey there')
            config.set_float('-kws_threshold', 1e-30)

        self.decoder = Decoder(config)
        self.decoder.start_utt()

    def put(self, data):
        super(Sphinx, self).put(data)

        self.queue.put(data)

    def start(self):
        self.done = False
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.decoder.end_utt()
        self.done = True

    def run(self):
        while not self.done:
            buf = self.queue.get()
            self.decoder.process_raw(buf, False, False)
            if self.decoder.hyp() != None:
                print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in self.decoder.seg()])
                print ("Detected keyword, restarting search")
                if callable(self.on_detected):
                    self.on_detected(self.decoder.hyp())
            self.decoder.end_utt()
            self.decoder.start_utt()
            super(Sphinx, self).put(buf)

    def set_callback(self, callback):
        self.on_detected = callback

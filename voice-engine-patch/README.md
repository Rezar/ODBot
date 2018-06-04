# Voice-engine Patch
This is a patch for [voice-engine](https://github.com/voice-engine/voice-engine) intended to be used with [pocketsphinx](https://github.com/cmusphinx/pocketsphinx-python). If you don't have either of these, please install them using the instruction ([here](https://github.com/Rezar/ODBot)) before applying this patch.

## Installation
1. Navigate to `voice-engine` folder generated from git cloning process during voice-engine installation.
2. Navigate to `voice-engine` folder inside `voice-engine`. (`voice-engine/voice-engine`). Make sure the current folder includes files such as `channel_picker.py`, `delay_sum.py`, `element.py`, etc.
3. Copy `sphinx.py` into this folder.
4. Navigate to parent folder
5. Run `python setup.py install` (root may be required)

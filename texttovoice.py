import subprocess
import os
import soundfile
import sys

SPEAK = '/Users/leo/Projects/dankbot/speak'
TEMP = '_temp'
TEMP_FILE = '{}.wav'.format(TEMP)
TMPTXT = '_tmptxt'
PATH = '/Users/leo/Projects/dankbot/'

def tts_to_wav(filename, text):
    f = open(TMPTXT, 'w')
    f.write(text)
    f.close()
    subprocess.run([SPEAK, '-w', '{}.wav'.format(filename), '-f', TMPTXT, text])
    try:
        os.remove(TMPTXT)
    except OSError:
        pass

def tts_to_ogg(filename, text):
    tts_to_wav(TEMP, text)
    sound, samplerate = soundfile.read(TEMP_FILE)
    soundfile.write('{}.ogg'.format(filename), sound, samplerate)
    # remove temp file
    try:
        os.remove(TEMP_FILE)
    except OSError:
        pass


if __name__ == '__main__':
    tts_to_ogg(sys.argv[1], sys.argv[2])

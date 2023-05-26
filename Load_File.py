# This program provides function to the main program to load the previous saved composition and then show its spectrogram.
# The program uses the previous_counter function of string_counter.py program to load the counter value and the concatinate 
# that value with the keywords 'KeySynth_piano.wav' to retrieve the previous saved composition and show its spectrogram.



import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from string_counter import previous_counter



def SPECTROGRAM():
    text = previous_counter()
    if text =='0':
        print('There is no previous file saved')
        return False
    else:
        (Fs, aud) = wavfile.read(text + 'KeySynth_piano.wav')
        aud = aud[:]
        # trim the first 125 seconds
        first = aud[:int(Fs*125)]
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs)
        plt.title('Spectrogram')
        plt.xlabel('Time (Sec)')
        plt.ylabel('Frequency (Hz)')
        plt.show()
        return True
    
        
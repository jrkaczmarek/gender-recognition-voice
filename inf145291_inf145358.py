from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from numpy import *
import sys

def hps(signal, rate, harmony = 3):
    #jezeli dwa kanaly to usredniamy je
    if len(signal.shape) == 2:        
        signal = (signal[:,0]+signal[:,1])/2
    
    #przemnozenie przez funkcje okna
    signal = signal * np.hamming(signal.shape[0])
    
    #obliczenie fft
    spec = np.abs(fft.fft(signal))
    
    #obliczenie czestotliwosc (od 0 do rate)
    freqs = np.arange(0, rate, rate/signal.size)
    
    #dlugosc finalnego spektrum
    length = int(np.ceil(spec.size/harmony))
    
    #wyliczenie nowego spektrum i downsampling
    new_spec = spec[:length].copy()
    for i in range(2, harmony+1):
        new_spec *= spec[::i][:length]
        
    #odfiltrowanie niepotrzebnych czestotliwosci
    for i in range(len(freqs[:length])):
        if freqs[i] < 70:
            new_spec[i] = 0
        
    return (new_spec, freqs[:length])

def plec(file):
    #proba wczytania pliku
    try:
        rate, data = wavfile.read(file)
    except:
        print("nieprawidlowy plik")
        return

    #wyluskanie spektrum z tonem wyodbrebnionym tonem podstawowym
    y, x = hps(data, rate, harmony=3)

    #wyszukanie tonu podstawowego
    freq = x[np.argmax(y[1:])]

    #klasyfikacja
    if freq < 180:
        print("M")
    else:
        print("K")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        plec(filename)
    else:
        print("podano nieprawidlowa ilosc argumentow")
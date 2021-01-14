from os import listdir
import os
from shutil import copyfile
from scipy import signal
from pydub import AudioSegment
import random
import scipy.io.wavfile as wav
from scipy.io.wavfile import read as read_wav


def zamiana_na_wave():
    just_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/test-clean/LibriSpeech/test-clean'
    os.chdir(just_path)
    for i in listdir():
        for j in listdir(str(i)):
            for k in listdir(str(i) + '/' + str(j)):
                flacfiles = [f for f in listdir(str(i) + '/' + str(j)) if f.endswith('.flac')]
            for l in flacfiles:
                pth = str(i) + '/' + str(j) + '/' + str(l)
                os.system('ffmpeg -i '+pth+' '+pth.replace('.flac', '.wav'))


def kopiowanie_wave_w_jedno_miejsce():
    just_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/test-clean/LibriSpeech/test-clean'
    dst_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/wave_wszystkie/'
    os.chdir(just_path)
    for i in listdir():
        for j in listdir(str(i)):
            for k in listdir(str(i) + '/' + str(j)):
                wavfiles = [f for f in listdir(str(i) + '/' + str(j)) if f.endswith('.wav')]
            for l in wavfiles:
                copyfile(str(i) + '/' + str(j) + '/' + str(l), dst_path + str(l))


def transkrypcje():
    just_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/test-clean txt'
    os.chdir(just_path)
    transcription=[]
    for i in listdir():
        for j in listdir(str(i)):
            for k in listdir(str(i) + '/' + str(j)):
                wavfiles = [f for f in listdir(str(i) + '/' + str(j)) if f.endswith('.txt')]
#            print(wavfiles)
            for l in wavfiles:
                pth = str(i) + '/' + str(j) + '/' + str(l)
                with open(pth) as f:
                    for myline in f:
                        transcription.append(myline)
    return transcription


def szukanie_czasow_poszczegolnych_slow():
    transcription = transkrypcje()
    lista_czasow=[]
    for b in range(0, len(transcription)):
        dzielenie = transcription[b].split(' ')

        slowa = dzielenie[1].split(',')
        del slowa[0]
        del slowa[0]
        najdluzsze_slowo = max(slowa, key=len)
        numer_slowa = slowa.index(najdluzsze_slowo)

        czasy = dzielenie[2].split(',')
        del czasy[0]
        czas_slowa = czasy[numer_slowa]
        lista_czasow.append(czas_slowa)
    return lista_czasow


def dopasowanie_czasu_do_nagrania():
    lista_czasow = szukanie_czasow_poszczegolnych_slow()
    #print(lista_czasow)

    wave_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/wave_wszystkie'
    os.chdir(wave_path)
    wavs = [f for f in listdir() if f.endswith('.wav')]

    lista_slow_i_czasow=[]

    for s in range(0, len(lista_czasow)):
        slowo_i_jego_miejsce = []
        slowo_i_jego_miejsce.append(wavs[s])
        slowo_i_jego_miejsce.append(lista_czasow[s])
        lista_slow_i_czasow.append(slowo_i_jego_miejsce)

    return lista_slow_i_czasow


def huki():
    just_path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/huk_wav'
    os.chdir(just_path)
    waves = [f for f in listdir() if f.endswith('.wav')]

    lista_hukow=[]
    for l in waves:
        lista_hukow.append(l)

        sampling_rate, data = read_wav(str(l))  # enter your filename

        x = signal.resample(data, 16000)
        print(x)

    return lista_hukow

huki()

def normalizacja():
    lista_z_danymi = dopasowanie_czasu_do_nagrania()
    lista_hukow = huki()

    for i in range(0, len(lista_z_danymi)):
        path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/'

        fs, nagranie = wav.read(path + 'wave_wszystkie/' + str(lista_z_danymi[i][0]))
        nagranie = nagranie / max(nagranie)
        wav.write((path + 'znormalizowane_nagrania/' + str(lista_z_danymi[i][0])), nagranie)

    for j in range(0, len(lista_hukow)):
        fs, huk = wav.read(path + 'huk_wav/' + str(lista_hukow[j]))
        huk = huk / max(huk)
        wav.write((path + 'znormalizowane_huki/' + str(lista_hukow[j])), huk)


def laczenie_z_odpowiednim_SNR(SNR):
    lista_z_danymi = dopasowanie_czasu_do_nagrania()
    lista_hukow = huki()

    for i in range(0, len(lista_z_danymi)):
        path = 'C:/Users/chyre/Desktop/Studia/V/TM/Projekt2/potrzebne pliki/'
        losowanie_huku = random.randrange(0, len(lista_hukow), 1)

        wave_path = AudioSegment.from_wav(path + 'wave_wszystkie/' + str(lista_z_danymi[i][0]))
        just_path = AudioSegment.from_wav(path + 'huk_wav/' + lista_hukow[losowanie_huku])

        x = SNR + just_path.dBFS - wave_path.dBFS

        just_path = just_path - x

        laczenie_nagran = wave_path.overlay(just_path, position=(float(lista_z_danymi[i][1])*1000))
        laczenie_nagran.export(path + 'polaczone_SNR_' + str(SNR) + '/' + str(lista_z_danymi[i][0]), format="wav")

        print('zdanie:', wave_path.dBFS, 'dBFS')
        print('huk:', just_path.dBFS, 'dBFS')
        print('SNR:', wave_path.dBFS - just_path.dBFS, 'dBFS')


#laczenie_z_odpowiednim_SNR(10)

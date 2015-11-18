#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import audioop
import sys
import websocket

#ws = websocket.create_connection("ws://localhost:8080/ws")

CHUNK  = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SEC = input('REC TIME >')

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")
print("")

for i in range(0, int(RATE / CHUNK * int(RECORD_SEC))):
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)

    print(rms)
    #ws.send(str(rms))
    #sys.stdout.write('\r\033[K' + "Volume: " + "#" * (rms//500))
    #sys.stdout.flush()

print("* done")

stream.stop_stream()
stream.close()
p.terminate()

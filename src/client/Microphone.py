# Source: https://github.com/jasperproject/jasper-client/blob/master/client/mic.py#L171

import tempfile
import wave
import audioop
import pyaudio
import whisper
import re
import os
import requests
import json


class Microphone:
    def __init__(
        self, speaker, model="medium", remote_whisper=False, remote_whisper_url=None
    ):
        self.speaker = speaker
        self._audio = pyaudio.PyAudio()
        self.model = whisper.load_model(model)
        self.remote_whisper = remote_whisper
        self.remote_whisper_url = remote_whisper_url

    def __del__(self):
        self._audio.terminate()

    def getScore(self, data):
        rms = audioop.rms(data, 2)
        score = rms / 3
        return score

    def fetchThreshold(self):
        THRESHOLD_MULTIPLIER = 1.8
        RATE = 16000
        CHUNK = 1024
        THRESHOLD_TIME = 3

        stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        frames = []
        lastN = [i for i in range(20)]

        for i in range(0, int(RATE / CHUNK * THRESHOLD_TIME)):
            data = stream.read(CHUNK)
            frames.append(data)
            lastN.pop(0)
            lastN.append(self.getScore(data))
            average = sum(lastN) / len(lastN)

        stream.stop_stream()
        stream.close()

        THRESHOLD = average * THRESHOLD_MULTIPLIER
        return THRESHOLD

    def transcribe(self, path):
        if self.remote_whisper == False:
            result = self.model.transcribe(path)
            return result["text"]
        else:
            payload = {}
            files = [("file", ("from_client.wav", open(path, "rb"), "audio/wav"))]
            headers = {}
            response = requests.request(
                "POST",
                self.remote_whisper_url,
                headers=headers,
                data=payload,
                files=files,
            )
            return json.loads(response.text)["result"]

    def passiveListen(self, PERSONA):
        print("Im listening carefully")
        THRESHOLD_MULTIPLIER = 1.8
        RATE = 16000
        CHUNK = 1024
        THRESHOLD_TIME = 1
        LISTEN_TIME = 5

        stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        frames = []
        lastN = [i for i in range(30)]

        for i in range(0, int(RATE / CHUNK * THRESHOLD_TIME)):
            data = stream.read(CHUNK)
            frames.append(data)
            lastN.pop(0)
            lastN.append(self.getScore(data))
            average = sum(lastN) / len(lastN)

        THRESHOLD = average * THRESHOLD_MULTIPLIER

        frames = []
        didDetect = False

        for i in range(0, int(RATE / CHUNK * LISTEN_TIME)):
            data = stream.read(CHUNK)
            frames.append(data)
            score = self.getScore(data)

            if score > THRESHOLD:
                didDetect = True
                break

        if not didDetect:
            print("No disturbance detected")
            stream.stop_stream()
            stream.close()
            return (None, None)

        frames = frames[-20:]

        DELAY_MULTIPLIER = 1
        for i in range(0, int(RATE / CHUNK * DELAY_MULTIPLIER)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        with tempfile.NamedTemporaryFile(mode="w+b") as f:
            wav_fp = wave.open(f, "wb")
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(b"".join(frames))
            wav_fp.close()
            f.seek(0)

            print(
                "I do not listen anymore, i'm thinking... looking for wake word: "
                + PERSONA
            )
            transcribed = self.transcribe(f.name)

        if PERSONA.lower() in re.sub("[,.!?]", "", transcribed.lower()):
            return (THRESHOLD, PERSONA)

        return (False, transcribed)

    def activeListen(self, THRESHOLD=None, skip_intro=False):
        RATE = 16000
        CHUNK = 1024
        LISTEN_TIME = 12

        if THRESHOLD is None:
            THRESHOLD = self.fetchThreshold()

        if skip_intro == False:
            self.speaker.play(
                os.path.join(os.path.dirname(__file__), "..", "audio", "yes.wav")
            )
        else:
            self.speaker.play(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "audio",
                    "611503__harrisonlace__perc_checkout.wav",
                )
            )

        stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        frames = []
        lastN = [THRESHOLD * 1.2 for i in range(30)]

        for i in range(0, int(RATE / CHUNK * LISTEN_TIME)):
            data = stream.read(CHUNK)
            frames.append(data)
            score = self.getScore(data)
            lastN.pop(0)
            lastN.append(score)
            average = sum(lastN) / float(len(lastN))

            if average < THRESHOLD * 0.8:
                break

        self.speaker.play(
            os.path.join(os.path.dirname(__file__), "..", "audio", "ok.wav")
        )

        stream.stop_stream()
        stream.close()

        with tempfile.NamedTemporaryFile(mode="w+b") as f:
            wav_fp = wave.open(f, "wb")
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(b"".join(frames))
            wav_fp.close()
            f.seek(0)

            print("I do not listen anymore, i'm thinking...")
            return self.transcribe(f.name)

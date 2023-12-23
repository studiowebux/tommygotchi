import pipes
import tempfile
import subprocess
import wave
from piper.voice import PiperVoice as piper
from os import remove

# Source: https://github.com/rhasspy/piper/issues/232#issuecomment-1751680611


class Mouth:
    model = None
    voice = None

    command = None

    def __init__(self, model_set, command="afplay"):
        self.model_set = model_set
        self.command = command

    def load(self):
        if ".onnx" in self.model_set:
            self.model = self.model_set
        self.voice = piper.load(self.model)

    def say(self, text):
        if self.voice == None:
            self.load()
        with wave.open("talk_to_me.wav", "wb") as wav_file:
            self.voice.synthesize(text, wav_file)
        self.play("talk_to_me.wav", True)

    def play(self, filename, temp=False):
        cmd = [self.command, str(filename)]
        print("Executing %s", " ".join([pipes.quote(arg) for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                print("Output was: '%s'", output)

        if temp == True:
            remove("talk_to_me.wav")

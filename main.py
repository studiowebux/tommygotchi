from Microphone import Microphone
from Mouth import Mouth
from Brain import Brain

def activeListenHandler(mic, brain, mouth, skip_intro=False):
    input = mic.activeListen(skip_intro)

    if input:
        answer = brain.post(input)
        brain.updateContext(answer)
        mouth.say(answer)
        if "?" in answer:
            activeListenHandler(mic, brain, mouth,skip_intro=True)
    else:
        mouth.say("Wut?")
        activeListenHandler(mic, brain, mouth,skip_intro=True)

def handler():
    mouth = Mouth(model_set="./piper-voices/en_US-amy-medium.onnx")
    mic = Microphone(speaker=mouth)
    brain = Brain()

    mouth.say("Hello, I'm listening.")

    while True:
        threshold, transcribed = mic.passiveListen("hey dude")

        if not transcribed or not threshold:
            print("Nothing has been said or transcribed.")
            continue
        print("You said: " + transcribed)
        
        activeListenHandler(mic, brain, mouth)

        mouth.play("audio/220175__gameaudio__pop-click.wav")

if __name__ == "__main__":
    handler()
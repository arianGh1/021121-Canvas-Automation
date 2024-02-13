import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

polly = boto3.client('polly')

try:
    
    text=f"""
        <speak> 
        <prosody rate="80%">
            What is the capital of France?
        </prosody>
        <prosody rate="80%">
            The capital of France is Paris.
        </prosody>
        <prosody rate="80%">
            What is the largest ocean?
        </prosody>
        <prosody rate="80%">
            The largest ocean is the Pacific Ocean.
        </prosody>
        <prosody rate="80%">
             Who wrote Hamlet?
        </prosody>
        <prosody rate="80%">
            Hamlet was written by William Shakespeare.
        </prosody>
    </speak>"""
    response = polly.synthesize_speech(Engine="standard",Text=text,TextType="ssml", OutputFormat="mp3", VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)

# Access the audio stream from the response
if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(os.getcwd(), "Freelancer/021121 Canvas Automation Using GPT/speech.mp3")
            try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
            # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])
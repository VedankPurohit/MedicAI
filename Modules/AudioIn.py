import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" #Temp workaround

from faster_whisper import WhisperModel
import speech_recognition as sr
import torch

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

model_size = "distil-medium.en"
model = WhisperModel(model_size, device=device, compute_type="float16")

WakeUpWords1 = "Hey"
WakeUpWords2 = "Hello"

def Listen():
    # Initialize the recognizer
    r = sr.Recognizer()
    try:
        # Start the microphone and record the audio
        with sr.Microphone() as source:
            print("Please speak now...")
            audio = r.listen(source)
        # Save the audio file
        with open("audio.wav", "wb") as file:
            file.write(audio.get_wav_data())
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except Exception as e:
        print("Error:", e)

def Transcribe():
    print("starting Transcribtion")
    try:
        segments, info = model.transcribe(audio="audio.wav", beam_size=5, 
            language="en", max_new_tokens=128, condition_on_previous_text=False)
        segments = list(segments)
        extracted_texts = [segment.text for segment in segments]
        extracted_texts = "".join(extracted_texts)
        return extracted_texts
    except Exception as e:
        print("Transcription Error:", e)
        return ""

Listen()
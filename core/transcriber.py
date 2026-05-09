import whisper
import os

whisper_model = os.getenv("WHISPER_MODEL", "small")
model = None

def load_model(model_name: str):
    global model
    if model is None:
        print(f"Loading Whisper model: {whisper_model}")
        model = whisper.load_model(whisper_model)
        print("Model loaded successfully.")
    return model

#in this function we will transcribe a single audio chunk using the whisper model and return the transcription as a string
#transcribe is the default task which will transcribe the audio in the original language, while translate will translate the audio to english and then transcribe it
def transcribe_chunk(chunk_path: str,translate: bool=False) -> str:
    model = load_model(whisper_model)
    task = "translate" if translate else "transcribe"

    result = model.transcribe(chunk_path, task=task) 
    return result["text"]


#this function will take a list of audio chunks and transcribe them one by one and concatenate the results into a single string

def transcribe_all(chunks: list, translate: bool=False) -> str:
    full_transcription = ""
    for chunk in chunks:
        transcription = transcribe_chunk(chunk, translate)
        full_transcription += transcription + " "
    return full_transcription





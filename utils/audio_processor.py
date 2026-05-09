
from torch import chunk
import yt_dlp
from pydub import AudioSegment
from dotenv import load_dotenv
import os


DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

#in this function we will download the audio from youtube and save it as mp3 file in the downloads folder
def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],"quiet": True
    }

    # Download the audio and return the file path
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return audio_file
    

def convert_to_wav(input_path: str)-> str:

    output_path = os.path.splitext(input_path)[0] + 'converted.wav' #this will change the extension of the file to wav and add converted at the end of the file name
    audio = AudioSegment.from_file(input_path)#this will read the audio file and convert it to wav format
    audio = audio.set_frame_rate(16000).set_channels(1)#this will set the frame rate to 16000 and the number of channels to 1 (mono) which is required for whisper model
    audio.export(output_path, format='wav')#this will export the audio file in wav format and save it to the output path
    return output_path


# data=download_youtube_audio("https://www.youtube.com/watch?v=HQmm4IJbguI")

# converted_file=convert_to_wav(data)

# print(f"Audio downloaded and converted to wav format: {converted_file}")


def chunk_audio(input_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_file(input_path)
    chunks = []
    chunk_ms = chunk_minutes * 60 * 1000  # Convert minutes to milliseconds
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i + chunk_ms]
        chunk_path = f"{os.path.splitext(input_path)[0]}_chunk_{i // chunk_ms}.wav"
        chunk.export(chunk_path, format='wav')
        chunks.append(chunk_path)
    return chunks

#   chunk_audio(converted_file)


def process_input(source: str) -> list:
    if source.startswith("http") or source.startswith("www"):
        audio_file = download_youtube_audio(source)
    else:
        audio_file = source

    converted_file = convert_to_wav(audio_file)
    chunks = chunk_audio(converted_file)
    return chunks




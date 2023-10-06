import os
import openai
import whisper
import tempfile
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def transcribe_fn_tmp(audio_file):
    s2t_model = whisper.load_model('base.en')
    transcription = s2t_model.transcribe(audio_file)
    
    return (transcription['text'])

def transcribe_fn(audio_file, chunk_size_ms=1.5*60000):
    
    audio = AudioSegment.from_file(audio_file)
    total_duration_ms = len(audio)
    temp_directory = 'data/temp'  # Temporary directory to store audio chunks

    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_directory, exist_ok=True)

    current_time_ms = 0
    transcriptions = []

    while current_time_ms < total_duration_ms:
        start_time_ms = current_time_ms
        end_time_ms = min(current_time_ms + chunk_size_ms, total_duration_ms)

        audio_chunk = audio[start_time_ms:end_time_ms]
        chunk_file = save_audio_chunk(audio_chunk, temp_directory)
        transcription = transcribe_chunk(chunk_file)
        transcriptions.append(transcription)

        current_time_ms += chunk_size_ms

    return ' '.join(transcriptions)

def save_audio_chunk(audio_chunk, temp_directory):
    # Create a temporary mp3 file in the specified directory
    with tempfile.NamedTemporaryFile(suffix=".mp3", dir=temp_directory, delete=False) as temp_mp3:
        audio_chunk.export(temp_mp3, format="mp3")
        return temp_mp3.name

def transcribe_chunk(chunk_file):
    with open(chunk_file, 'rb') as audio:
        transcription = openai.Audio.transcribe(
            model='whisper-1',
            file=audio,
            language='en'
        )
    return transcription['text']


def summarize_fn(text):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': "You are an helpful assistant, specialized in text summarization."},
            {'role': 'user', 'content': f"I will provide you the lyrics of a song, and I want you to summarize the text and tell what the song is about. Note that lyrics may contain errors. Lyrics: <<<{text}>>>. Response:"}
        ],
        max_tokens = 256,
        temperature = 0
    ).choices[0].message.content
    
    return response
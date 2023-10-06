# Whisper2me

## Overview

This is a toy gradio application that expects an audio file (mp3, wav, ...) of a song and is able to extract the lyrics as well as summarize them.

The building blocks are OpenAI `whisper` model for audio transcription and `gpt-3.5-turbo` for text summarization.

## Usage

To utilize the tool, you need to clone the repository, install the requirements and run the application:

```
git clone https://github.com/apiraccini/whisper2me.git
cd whisper2me
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Notes

In order to utilize the tool, you need to create a `.env` file in the root directory and store your OpenAI API Key inside!

The base version uses the standard API call to whisper for transcription. This allows to use the best version of the model with inference optimized for efficiency. 

An alternative is to use the open source package from OpenAI: the model is the same but is downloaded and runs on the user machine, so the default option is to use the smallest model available. It works well with files without instrumental/background noise, not so much for songs with a lot of instruments. To do so, just uncomment line 16 on `app.py` and comment line 17.

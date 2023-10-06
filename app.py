import gradio as gr
from utils.app_utils import transcribe_fn_tmp, transcribe_fn, summarize_fn 

with gr.Blocks(theme=gr.themes.Monochrome()) as demo:

    gr.Markdown('# Whisper2me 🤫\nI am a song lyric generator and summarizer, just load your mp3 file and let me do the rest. 😉')
    
    with gr.Tab(label='Load data'):
        audio_file = gr.Audio(label='Audio', source='upload', type='filepath')
        #audio_file = gr.Audio(label='Audio', source='microphone', type='filepath')
        
    with gr.Tab(label='Lyric generator'):
        transcribe_btn = gr.Button(value = 'Transcribe')
        lyrics = gr.Textbox(label='Lyrics', placeholder='...')
    
        #transcribe_btn.click(fn=transcribe_fn_tmp, inputs=audio_file, outputs=lyrics, api_name="whisper2me_transcribe")
        transcribe_btn.click(fn=transcribe_fn, inputs=audio_file, outputs=lyrics, api_name="whisper2me_transcribe")

    with gr.Tab(label='About the song'):
        summarize_btn = gr.Button(value = 'Summarize')
        summary = gr.Textbox(label='Summary', placeholder='...')
    
        summarize_btn.click(fn=summarize_fn, inputs=lyrics, outputs=summary, api_name="whisper2me_summarize")

if __name__ == '__main__':
    demo.launch()
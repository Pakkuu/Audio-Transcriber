#Setup(macOS)(Python 3.11.0)
#       - setup a python virtual environment
#       - copy this file/code into the venv
#       - activate the venv
#       - install required libraries: streamlit, whisper, ffmpeg, pytorch
#       - run the script with "streamlit run webpage.py" in a terminal
#       - website will run locally in the default browser
import streamlit as st
import whisper
import tempfile #using temp dir so that audio file does not have to be in the same folder as the script
import os

st.title("Audio-To-Text Converter")

#create two column layout
file_column, button_column = st.columns([2,1])

#upload audio file with streamlit
audio_file = st.file_uploader("Upload Audio", type=["wav","mp3","aac"])

model = whisper.load_model("base")
transcription = None #initialize transcription as none

#transcription function
@st.cache_data
def transcribe_audio(audio_file):
        if audio_file is not None:
                #create a temporary directory
                temp_dir = tempfile.TemporaryDirectory()
                temp_audio_path = os.path.join(temp_dir.name, audio_file.name)

                #save uploaded audio file to the temporary directory
                with open(temp_audio_path, "wb") as audio_file_temp:
                        audio_file_temp.write(audio_file.read())

                transcription = model.transcribe(temp_audio_path)

                #close and cleanup temporary directory
                temp_dir.cleanup()
                return transcription
        else:
                st.error("Please upload an audio file")

if st.button("Transcribe Audio"):
        st.success("Transcribing Audio")
        transcription = transcribe_audio(audio_file)
        st.success("Transcription Complete")


#option to edit text
if transcription is not None:
        edit_text = st.text_area("Edit Transcription", value=transcription["text"])
        transcription["edited text"] = edit_text #store edited text

#option to download text
if transcription is not None:
        st.markdown("### Download Options")
        download_format = st.radio("Select Download Format", ["Text","JSON"])
        if st.button("Download Transcription"):
                if download_format == "Text":
                        st.text(transcription["edited_text"])
                elif download_format == "JSON":
                        st.json(transcription)

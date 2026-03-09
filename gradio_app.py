import gradio as gr
import speech_recognition as sr
import tempfile

from brain_of_the_doctor import encode_image, analyze_image_with_query, model
from voice_of_the_doctor import text_to_speech_with_gtts


# -----------------------------
# Speech to Text
# -----------------------------
def speech_to_text(audio_path):

    if audio_path is None:
        return "No audio recorded."

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

    except Exception as e:
        text = "Could not understand the audio."

    return text


# -----------------------------
# Main AI Doctor Function
# -----------------------------
def process_inputs(audio, image):

    # 1️⃣ Convert speech to text
    speech_text = speech_to_text(audio)

    # 2️⃣ Check if image exists
    if image is None:
        return speech_text, "Please upload an image or take a live photo.", audio, None

    # 3️⃣ Encode image
    encoded_image = encode_image(image)

    # 4️⃣ Send query to AI doctor
    query = f"""
    You are an AI doctor assistant.

    Patient symptoms:
    {speech_text}

    Analyze the medical image and provide simple medical guidance.
    If the condition looks serious, suggest consulting a doctor.
    """

    doctor_response = analyze_image_with_query(
        query,
        model,
        encoded_image
    )

    # 5️⃣ Convert doctor response to voice
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    text_to_speech_with_gtts(
        doctor_response,
        temp_audio.name
    )

    return speech_text, doctor_response, audio, temp_audio.name


# -----------------------------
# Gradio Interface
# -----------------------------
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Record Your Voice"
        ),

        gr.Image(
            sources=["upload", "webcam"],   # ✅ Upload + Live Photo
            type="filepath",
            label="Upload Image or Take Live Photo"
        )
    ],

    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(type="filepath", label="Patient's Voice"),
        gr.Audio(type="filepath", label="Doctor's Voice")
    ],

    title="CheckUp AI - Virtual Health Check Partner",
    description="Upload your voice and medical image to get AI health suggestions."
)

iface.launch(server_port=7860)
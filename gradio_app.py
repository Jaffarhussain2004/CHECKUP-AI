iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record Your Voice"),
        gr.Image(type="filepath", label="Upload Image")
    ],   
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(type="filepath", label="Patient's Voice"),
        gr.Audio(type="filepath", label="Doctor's Voice")
    ],
    title="CheckUp AI - Virtual Health Check Partner "
)

iface.launch(server_name="0.0.0.0", server_port=10000)
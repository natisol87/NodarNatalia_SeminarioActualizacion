import gradio as gr


def saludar(nombre):
    nombre = nombre.strip()
    return f"Hola, {nombre or 'mundo'}!"


app = gr.Interface(
    fn=saludar,
    inputs=gr.Textbox(label="Tu nombre"),
    outputs=gr.Textbox(label="Saludo"),
    title="App mínima de Gradio",
)


if __name__ == "__main__":
    app.launch(share=True)

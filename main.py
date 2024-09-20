import os

import ollama
import gradio as gr

from util import get_system_prompt


def get_image_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.png', '.jpg', '.jpeg'))]


image_directory = "/home/humgate/AI/kohya_train/datasets/training_images/Bambolina0"
images = get_image_paths(image_directory)
captioning_prompt = get_system_prompt()
system_prompt = get_system_prompt()


def generate_caption(prompt, system, image):
    result = ollama.generate(
        model='llava',
        prompt=prompt,
        system=system,
        images=[image],
        stream=False
    )['response']
    return result.replace('"', '')

def show_caption(image_path):
    # Generate the initial caption
    return generate_caption(captioning_prompt, system_prompt, image_path)


# Gradio interface
def update_caption(image_path, edited_caption):
    return image_path, edited_caption


with gr.Blocks() as caption_ui:
    with gr.Row():
        with gr.Column(scale=4):
            caption = show_caption(images[0])
            img = gr.Image(images[0], type="filepath", interactive=True)  # Resized image
        with gr.Column(scale=6):
            generated_caption_box = gr.Textbox(caption, lines=3, label="Generated caption")
            submit_button1 = gr.Button("Generate caption")
            edited_caption_box = gr.Textbox(caption, interactive=True, lines=3, label="Edited caption")
            submit_button2 = gr.Button("Save edited caption")
    submit_button1.click(
        fn=show_caption,
        inputs=[img],
        outputs=[generated_caption_box]
    )

if __name__ == '__main__':
    # Launch Gradio app
    caption_ui.launch()

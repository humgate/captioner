import os

import ollama
import gradio as gr

from util import load_prompts, save_prompts

prompts_dir = "prompts"



def get_image_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.png', '.jpg', '.jpeg'))]


def get_next_image(directory, img_number_str):
    images = get_image_paths(directory)
    current_img_number = int(img_number_str)
    if current_img_number < len(images) - 1:
        current_img_number += 1
        current_img_number_text = str(current_img_number)
    else:
        current_img_number_text = img_number_str
    return images[current_img_number], current_img_number_text


def get_prev_image(directory, img_number_str):
    images = get_image_paths(directory)
    current_img_number = int(img_number_str)
    if current_img_number > 0:
        current_img_number -= 1
        current_img_number_text = str(current_img_number)
    else:
        current_img_number_text = img_number_str
    return images[current_img_number], current_img_number_text


def generate_caption(prompt, system, image):
    result = ollama.generate(
        model='llava',
        prompt=prompt,
        system=system,
        images=[image],
        stream=False
    )['response']
    return result.replace('"', '')


def generate_caption_for_image(image_path):
    return generate_caption(captioning_prompt, system_prompt, image_path)


# Gradio UI
with gr.Blocks() as caption_ui:
    with gr.Tab("Captioning"):
        with gr.Row():
            with gr.Column(scale=4):
                img = gr.Image(type="filepath", show_label=True)
            with gr.Column(scale=6):
                images_folder_box = gr.Textbox(interactive=True, label="Images folder", info="Enter images folder path and hit Enter")
                with gr.Row():
                    file_path_box = gr.Textbox(label="Image", scale=9)
                    image_number_box = gr.Textbox(value="-1", scale=1, label="number", max_length=2)
                with gr.Row():
                    prev_button = gr.Button("Previous")
                    next_button = gr.Button("Next")
                generated_caption_box = gr.Textbox(lines=3, label="Generated caption")
                with gr.Row():
                    generate_button = gr.Button("Generate caption", scale=9)
                    copy_button = gr.Button("Copy for editing", scale=1)
                edited_caption_box = gr.Textbox(interactive=True, lines=3, label="Edited caption")
                save_button = gr.Button("Save edited caption")
    with gr.Tab("Prompts"):
        system_prompt, captioning_prompt = load_prompts(prompts_dir)
        system_prompt_box = gr.Textbox(interactive=True, lines=15, label="System prompt", value=system_prompt)
        captioning_prompt_box = gr.Textbox(interactive=True, lines=3, label="Captioning prompt",
                                           value=captioning_prompt)
        save_prompts_button = gr.Button("Save prompts caption")

    # Handlers
    generate_button.click(fn=generate_caption_for_image, inputs=[img], outputs=[generated_caption_box])

    images_folder_box.submit(
        fn=get_next_image,
        inputs=[images_folder_box, image_number_box],
        outputs=[file_path_box, image_number_box]
    )

    file_path_box.change(
        fn=lambda folder, number: get_image_paths(folder)[int(number)],
        inputs=[images_folder_box, image_number_box],
        outputs=img
    )

    next_button.click(
        fn=get_next_image,
        inputs=[images_folder_box, image_number_box],
        outputs=[file_path_box, image_number_box]
    )
    prev_button.click(
        fn=get_prev_image,
        inputs=[images_folder_box, image_number_box],
        outputs=[file_path_box, image_number_box]
    )

    copy_button.click(
        fn=lambda caption: caption,
        inputs=generated_caption_box,
        outputs=edited_caption_box
    )

    save_prompts_button.click(
        fn=lambda sys_prompt, capt_prompt: save_prompts(prompts_dir, sys_prompt, capt_prompt),
        inputs=[system_prompt_box, captioning_prompt_box],
        outputs=None
    )

if __name__ == '__main__':
    caption_ui.launch()

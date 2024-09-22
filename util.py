import os

import gradio as gr
import ollama
import requests


def get_image_paths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.png', '.jpg', '.jpeg'))]


def get_next_image(directory, img_number_str):
    images = get_image_paths(directory)
    if not images:
        return None, img_number_str
    current_img_number = int(img_number_str)
    if current_img_number < len(images) - 1:
        current_img_number += 1
    return images[current_img_number], str(current_img_number)


def get_prev_image(directory, img_number_str):
    images = get_image_paths(directory)
    current_img_number = int(img_number_str)
    if current_img_number > 0:
        current_img_number -= 1
    return images[current_img_number], str(current_img_number)


def load_prompts(prompts_dir):
    with open(f"{prompts_dir}/system_prompt.md", 'r') as file:
        system_prompt = file.read()
    with open(f"{prompts_dir}/captioning_prompt.md", 'r') as file:
        captioning_prompt = file.read()
    return system_prompt, captioning_prompt


def load_caption(image_file):
    caption_file = get_caption_file(image_file)
    if os.path.exists(caption_file):
        with open(caption_file, 'r') as file:
            caption = file.read()
            return caption
    return None


def save_prompts(prompts_dir, system_prompt, captioning_prompt):
    with open(f"{prompts_dir}/system_prompt.md", 'w') as file:
        file.write(system_prompt)
    with open(f"{prompts_dir}/captioning_prompt.md", 'w') as file:
        file.write(captioning_prompt)


def get_caption_file(image_file):
    base_name, _ = os.path.splitext(image_file)
    return f"{base_name}.txt"


def save_caption_for_image(image_file, caption):
    caption_file = get_caption_file(image_file)
    if os.path.exists(caption_file):
        return f"File '{caption_file}' already exists! Please confirm to overwrite.", False
    else:
        with open(caption_file, 'w') as f:
            f.write(caption)
        return f"Caption saved to {caption_file}", True


def check_save(image_file, caption):
    msg, ready = save_caption_for_image(image_file, caption)
    if not ready:
        return msg, gr.update(visible=True), gr.update(visible=True)
    return msg, gr.update(visible=False), gr.update(visible=False)


def confirm_save(image_file, caption, confirm_overwrite):
    caption_file = get_caption_file(image_file)
    if confirm_overwrite:
        with open(caption_file, 'w') as file:
            file.write(caption)
        return f"Caption saved to {caption_file}", gr.update(visible=False), gr.update(visible=False)
    else:
        return f"Operation cancelled. File '{caption_file}' not overwritten.", gr.update(visible=False), gr.update(
            visible=False)


def cancel_save(image_file):
    caption_file = get_caption_file(image_file)
    return (f"Operation cancelled. File '{caption_file}' not overwritten.",
            gr.update(visible=False),
            gr.update(visible=False))


def get_local_models(default_model):
    model_names = [model['name'] for model in ollama.list()['models']]
    resulted_default_model = None
    for name in model_names:
        if name == default_model:
            resulted_default_model = name
            break
    if resulted_default_model is None and model_names:
        resulted_default_model = model_names[0]
    return model_names, resulted_default_model


def translate_with_deep_translator_service(text, target_language):
    flask_url = f"http://localhost:{os.getenv('FLASK_PORT', '5000')}/translate"
    response = requests.post(flask_url, json={'text': text}, params={'dest_lang': target_language})
    return response.json().get('translated_text', 'Translation failed.')

import os

import gradio as gr

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

def load_prompts(prompts_dir):
    with open(f"{prompts_dir}/system_prompt.md", 'r') as file:
        system_prompt = file.read()
    with open(f"{prompts_dir}/captioning_prompt.md", 'r') as file:
        captioning_prompt = file.read()
    return system_prompt, captioning_prompt


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

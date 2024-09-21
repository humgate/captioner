import os


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

def save_caption_for_image(image_file, caption):
    with open(get_caption_file(image_file), 'w') as file:
        file.write(caption)

def get_caption_file(image_file):
    base_name, _ = os.path.splitext(image_file)
    return f"{base_name}.txt"

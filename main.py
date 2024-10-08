import subprocess

from dotenv import load_dotenv

from util import *

prompts_dir = "prompts"
captioning_model = 'llava:13b'
translate_model = 'llama3.1:latest'
system_prompt, captioning_prompt = load_prompts(prompts_dir)
google_translate_destination = 'ru'


def generate_caption_for_image(image_path, model):
    try:
        result = ollama.generate(
            model=model,
            prompt=captioning_prompt,
            system=system_prompt,
            images=[image_path],
            stream=False
        )['response'].replace('"', '').strip()
        if not result:
            return "Error: No caption generated. Check Ollama running correctly with LLaVA model"
        return result
    except Exception as e:
        return f"Error generating caption: {str(e)}"


# Gradio UI
with gr.Blocks() as caption_ui:
    with gr.Tab("Captioning"):
        with gr.Row():
            with gr.Column(scale=4):
                img = gr.Image(type="filepath", show_label=True, interactive=False)
            with gr.Column(scale=6):
                images_folder_box = gr.Textbox(interactive=True, label="Images folder",
                                               info="Enter images folder path and hit Enter")
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
                edited_caption_box = gr.Textbox(
                    interactive=True, lines=3, label="Edited caption", info="Shift + Enter to translate"
                )
                translated_caption_box = gr.Textbox(
                    interactive=True, lines=3, label="Translated caption", info="Shift + Enter to translate back" )
                save_caption_button = gr.Button("Save caption")
                alert_box = gr.Markdown()
                with gr.Row():
                    overwrite_button = gr.Button("Confirm overwrite", visible=False, scale=1)
                    cancel_button = gr.Button("Cancel", visible=False, scale=1)
    with gr.Tab("Prompts"):
        system_prompt_box = gr.Textbox(
            interactive=True, lines=10, label="System prompt", value=system_prompt
        )
        captioning_prompt_box = gr.Textbox(
            interactive=True, lines=10, label="Captioning prompt", value=captioning_prompt
        )
        save_prompts_button = gr.Button("Save prompts")
    with gr.Tab("Settings"):
        model_names, default = get_local_models(captioning_model)
        model_dropdown = gr.Dropdown(
            choices=model_names, label="Captioning model", value=default, interactive=True
        )
        translate_dest_box = gr.Textbox(
            interactive=True,
            label="Translation destination language",
            value=google_translate_destination,
            info="Destination language code, for ex. 'ru'"
        )

    # Handlers
    generate_button.click(
        fn=generate_caption_for_image,
        inputs=[img, model_dropdown],
        outputs=[generated_caption_box]
    )

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

    file_path_box.change(
        fn=lambda image_file: load_caption(image_file),
        inputs=file_path_box,
        outputs=edited_caption_box
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
        fn=lambda system, captioning: save_prompts(prompts_dir, system, captioning),
        inputs=[system_prompt_box, captioning_prompt_box]
    )

    save_caption_button.click(
        fn=check_save,
        inputs=[file_path_box, edited_caption_box],
        outputs=[alert_box, overwrite_button, cancel_button]
    )

    overwrite_button.click(
        fn=confirm_save,
        inputs=[file_path_box, edited_caption_box, gr.State(True)],
        outputs=[alert_box, overwrite_button, cancel_button]
    )

    cancel_button.click(
        fn=cancel_save,
        inputs=file_path_box,
        outputs=[alert_box, overwrite_button, cancel_button]
    )

    edited_caption_box.submit(
        fn=translate_with_deep_translator_service,
        inputs=[edited_caption_box, translate_dest_box],
        outputs=translated_caption_box
    )

    translated_caption_box.submit(
        fn=translate_back_to_en_with_deep_translator_service,
        inputs=translated_caption_box,
        outputs=edited_caption_box
    )

if __name__ == '__main__':
    load_dotenv()
    flask_process = subprocess.Popen(['python', 'flask_translate_service.py'])
    try:
        caption_ui.launch()
    finally:
        flask_process.terminate()
        flask_process.wait()  # O
        print("Flask service terminated")

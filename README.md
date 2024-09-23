# Gradio Image Captioning Tool with LLaVA

Generates image captions using the LLaVA model. Helps organize the process of creating captions for multiple images in a folder, simplifying manual correction for each image.
Useful when creating captions for training datasets where manual correction is required.
## Features
- **Image folder setting**: Set images folder path.
- **Image navigation**: Navigate to next/previous image in the images folder.
- **Image preview**: Preview selected image.
- **Existing caption**: Displays existing caption from caption file if it exists
- **Caption generation**: Generate caption for selected image using the LLaVA model.
- **Manual editing**: Manually edit generated captions directly in the UI.
- **Translate caption**: Translate caption to another language. Set in Settings Tab 
- **Save caption**: Save edited captions as `.txt` files with the same name as the image.
## Requirements
- Python 3.10+
- [Gradio](https://gradio.app/) (for the UI)
- [Ollama](https://ollama.com/) Python client (for LLaVA model integration)
## Install
1. Clone the repository and
2. Create and activate venv
```
cd captioner
python -m venv venv
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt`
```
4. Ensure the LLaVA model is correctly set up using the Ollama Python client. The model should be accessible at the 
correct URL (e.g., http://localhost:11434 or your local instance).
## Run
1. **Start the Gradio UI**:
```
python main.py
```
2. **Navigate the UI**:
- Review captioning prompts on the **Prompts tab**. Modify according to your images specific features
- Set image directory: Enter the path of the folder containing your images in the text box on main tab.
- Generate captions: Click "Generate Caption" to create a caption for the currently displayed image.
- Edit captions: Click "Copy for editing" to copy generated caption into edit field. Modify the generated caption 
if necessary.
- Translate edited caption: Shift + Enter to translate Edited caption.
- Save caption: Click "Save caption" to save the caption as a .txt file in the same folder as the image.
- Image navigation: Use the UI to navigate to the next or previous image in the directory.

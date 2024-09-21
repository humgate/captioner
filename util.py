def get_captioning_prompt():
    return """Please create one caption for image according to guidelines
    """


def get_system_prompt():
    return """##Guidelines
    1. Mention that image is portrait of art doll in caption.
    2. Identify the portrait type and include it in the caption. Use one of the following:
    - full-body portrait: Entire body visible from head to toe.
    - three-quarter body: Body visible from head down to knees.
    - half-body portrait: Body visible from head down to the waist.
    - close-up: Only head and upper chest visible.
    - head-shot: Only head visible.
    - extreme close-up: Only face visible.
    3. Identify lighting style and include "Rembrandt lighting" or "Daylight lighting" into caption where:
    - Rembrandt: lighting creates a clearly visible gradient between the brightly lit one side of the object and the darkened other part.
    - Daylight: background and the subject illuminated evenly from all sides. Lighting does not create high contrasts between dark and light areas.
    4. The caption should have length about 35 words.
    """


def get_lighting_prompt():
    return """##Lighting style identification guide. Use one of the following:
    - Rembrandt light: a photograph in general in dark tones, with a dark, often almost black background and the object 
    illuminated unevenly, but mainly on one side. This type of lighting creates a clearly visible gradient between the 
    brightly lit one side of the object and the darkened other part, thereby creating the illusion of a three-dimensional 
    image for the viewer and at the same time sharply separating the object from the background. 
    This type of lighting is often called "Rembrandt light"
    - Flat light: a photograph in general in light tones, with a light gray or white background and the subject illuminated 
    evenly from all sides. This type of lighting does not create very bright and very dark areas and high contrasts between
     them. This type of lighting creates the illusion of lighting as on a cloudy day outside. This type of lighting is often
      called "Flat light" 
    """


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

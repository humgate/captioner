from openai import OpenAI

openai_client = OpenAI(
    base_url="http://192.168.0.195:11434/v1",
    api_key='ollama'
)

img_url = "https://civitai.com/images/29857139"

if __name__ == '__main__':
    response = openai_client.chat.completions.create(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": f"please create a caption about 40 words in length for the image: {img_url}"
            }
        ],
    )

    print(response.choices[0].message.content)




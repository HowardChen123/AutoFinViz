from openai import OpenAI

def get_api_key():
    try:
        with open("apikey", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % "apikey")

api_key = get_api_key()
gpt_client = OpenAI(
    api_key= api_key
)

def generateLLMResponse(system_prompt, message):
    completion = gpt_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": message},
    ])

    return completion.choices[0].message.content
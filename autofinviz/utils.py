from openai import OpenAI
import re

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

def generateLLMResponse_viz(messages):
    completion = gpt_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages)

    return completion.choices[0].message.content

def preprocess_code(code: str) -> str:
    """Preprocess code to remove any preamble and explanation text"""

    code = code.replace("<imports>", "")
    code = code.replace("<stub>", "")
    code = code.replace("<transforms>", "")

    # remove all text after chart = plot(data)
    if "chart = plot(data)" in code:
        # print(code)
        index = code.find("chart = plot(data)")
        if index != -1:
            code = code[: index + len("chart = plot(data)")]

    if "```" in code:
        pattern = r"```(?:\w+\n)?([\s\S]+?)```"
        matches = re.findall(pattern, code)
        if matches:
            code = matches[0]

    if "import" in code:
        # return only text after the first import statement
        index = code.find("import")
        if index != -1:
            code = code[index:]

    code = code.replace("```", "")
    if "chart = plot(data)" not in code:
        code = code + "\nchart = plot(data)"
    return code
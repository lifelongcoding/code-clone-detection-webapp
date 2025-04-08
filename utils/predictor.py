from openai import OpenAI


def get_predict(code_fragment1, code_fragment2, api_key, base_url, model, prompt):
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"CODE_FRAGMENT1: {code_fragment1}\nCODE_FRAGMENT2: {code_fragment2}"}
        ],
        stream=False,
        temperature=0.1
    )
    prediction = response.choices[0].message.content.lstrip("\n")

    cot = ""
    if hasattr(response.choices[0].message, "reasoning_content"):
        cot = response.choices[0].message.reasoning_content

    return {'prediction': prediction, 'cot': cot}

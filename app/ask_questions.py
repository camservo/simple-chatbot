import json


def get_openai_response_complete(client, question, model="gpt-4-turbo-preview"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Please place every sentence in it's own complete json object.  The key of each sentence should be 'message'",
            },
            {"role": "user", "content": question},
        ],
    )
    return response


def get_openai_responses_in_sentences(client, question, model="gpt-4-turbo-preview"):
    buffer = ""  # Initialize a buffer to accumulate text chunks
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Please place every sentence in it's own complete json object.  The key of each sentence should be 'message'",
            },
            {"role": "user", "content": question},
        ],
        stream=True,
        # max_tokens=5
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            buffer += str(chunk.choices[0].delta.content)
        try:
            obj = json.loads(buffer)
            yield obj["message"]
            buffer = ""

        except json.JSONDecodeError:
            continue

    if buffer.strip():
        yield buffer.strip()

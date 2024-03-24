import json


def get_openai_response_complete(client, question, model="gpt-4-turbo-preview"):
    """
    Retrieves a complete response from the OpenAI API for a given question in a single operation.

    This streamlined function communicates with the OpenAI API by sending a question and
    awaits a full, single-message response. It is designed for scenarios where it's preferable
    to handle the entire response at once, rather than dealing with incremental or partial data.

    Parameters:
    - client (OpenAI API client object): The client instance used to communicate with the OpenAI API.
      Must be properly authenticated and configured prior to making requests.
    - question (str): The question to be sent to the OpenAI API for processing.
    - model (str, optional): The specific OpenAI model to utilize for generating the response.
      Defaults to "gpt-4-turbo-preview", which is tailored for efficient and prompt answers.

    Returns:
    - dict: A dictionary representing the complete response from the OpenAI API. The structure
      and content of this response will vary depending on the question asked and the model used.

    Example:
        >>> client = OpenAI(api_key="your_api_key_here")
        >>> question = "What is the capital of France?"
        >>> response = get_openai_response_complete(client, question)
        >>> print(response)
        {'choices': [{'text': 'Paris'}], ...}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question},
        ],
    )
    return response


def get_openai_responses_in_sentences(client, question, model="gpt-4-turbo-preview"):
    """
    Yields responses from the OpenAI API for a given question, split into individual sentences.

    This function streams the response from the OpenAI API, yielding each sentence
    of the response as soon as it's available. This is particularly useful for
    processing or displaying responses incrementally.

    Parameters:
    - client: An instance of the OpenAI API client, configured with the necessary
      authentication.
    - question: The question string to be sent to the OpenAI API.
    - model: The OpenAI model to use for generating the response. Default is "gpt-4-turbo-preview".

    Yields:
    - Each sentence of the response as a string, one by one.

    Notes:
    - This function uses streaming to receive responses, which can be useful for
      real-time applications.
    - If a partial response cannot be parsed as JSON, it will be buffered until
      a complete JSON object can be formed.
    """
    buffer = ""  # Initialize a buffer to accumulate text chunks
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Please place every sentence in its own complete json object. The key of each sentence should be 'message'",
            },
            {"role": "user", "content": question},
        ],
        stream=True,
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

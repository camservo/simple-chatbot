import json
import logging


class OpenAiQuery:
    def __init__(self, client, default_model="gpt-4-turbo-preview"):
        self.client = client
        self.default_model = default_model

    def get_openai_response_complete(self, question, model=None):
        try:
            model = model or self.default_model
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": question},
                ],
            )
            return response
        except Exception as e:
            logging.error(f"Couldn't make query: {str(e)}")

    def get_openai_responses_in_sentences(self, question, model=None):
        try:
            model = model or self.default_model
            buffer = ""  # Initialize a buffer to accumulate text chunks
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Please place every sentence in its own complete json object. The key of each sentence should be 'message'.  The response should not be formatted at all otherwise.",
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

        except Exception as e:
            logging.error(f"Couldn't make query: {str(e)}")

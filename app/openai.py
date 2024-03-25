import json
import logging
import os

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)


class OpenAiQuery:
    def __init__(self, client, default_model="gpt-4-turbo-preview"):
        self.client = client
        self.default_model = default_model
        self.session_history = []  # Initialize an empty list to store message history

    def add_message_to_history(self, role, content):
        """
        Adds a message to the session history.

        :param role: The role of the message, either 'user' or 'system'.
        :param content: The content of the message.
        """
        self.session_history.append({"role": role, "content": content})

    def get_openai_response_complete(self, question, model=None):
        try:
            model = model or self.default_model
            # Add the user's question to the session history
            self.add_message_to_history("user", question)

            response = self.client.chat.completions.create(
                model=model,
                messages=self.session_history,  # Pass the updated session history
            )

            # Optionally, add the system's response to the session history
            if response.choices and response.choices[0].text.strip():
                self.add_message_to_history("system", response.choices[0].text.strip())

            return response
        except Exception as e:
            logging.error(f"Couldn't make query: {str(e)}")

    def get_openai_responses_in_sentences(self, question, model=None):
        try:
            model = model or self.default_model
            response_text = ""
            # System message for sentence segmentation, if needed
            system_message = {
                "role": "system",
                "content": "Please place every sentence in its own complete json object. The key of each sentence should be 'message'.  The response should not be formatted at all otherwise.",
            }
            query = {"role": "user", "content": question}
            messages = list(self.session_history)
            messages.append(system_message)
            messages.append(query)
            print(messages)
            # logging.info("Sending messages: ", str(messages))
            print(json.dumps(messages))

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )

            buffer = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    buffer += str(chunk.choices[0].delta.content)
                    response_text += str(chunk.choices[0].delta.content)
                try:
                    obj = json.loads(buffer)
                    yield obj["message"]
                    buffer = ""
                except json.JSONDecodeError:
                    continue

            if buffer.strip():
                response_text != str(buffer)
                yield buffer.strip()

            # Add the user's question to the session history
            self.add_message_to_history("assistant", response_text)
            # Optionally, add the system's segmented response to the session history here

        except Exception as e:
            logging.error(f"Couldn't make query: {str(e)}")

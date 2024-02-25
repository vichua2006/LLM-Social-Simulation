# Importing necessary libraries
import numpy as np  # numpy for numerical computations
import os  # os for accessing environment variables
from openai import OpenAI # OpenAI for interacting with the GPT-3 model
from openai.types import Completion

# Setting the OpenAI API key
charles_key="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"
taitienchi_key="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"
jinhan_key = "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"
ericyamnovski_key = "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"
ryan_key = "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"
victor_key = "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"

os.environ["OPENAI"] = jinhan_key
client = OpenAI(
  api_key=os.environ["OPENAI"]
)
# Function to interact with the GPT-3 model and get response

def chat(system, user_assistant,top_prob):
    # Format the conversation
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
        for i in range(len(user_assistant))
    ]

    # Combine the system and user messages
    msgs = system_msg + user_assistant_msgs
    try:
      # Interact with the GPT-3 model
      response = client.chat.completions.create(model="gpt-3.5-turbo", messages=msgs,top_p=top_prob)
      # Check the status of the response
      status_code = response.choices[0].finish_reason
      assert status_code == "stop", f"The status code was {status_code}."
      # Return the content of the response
      return response.choices[0].message.content
    except Exception as e:
      print("An Exception Occur when communicating with ChatGPT:",e)


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    if not text: 
      text = "this is blank"
    return client.embeddings.create(input=[text], model=model).data[0].embedding
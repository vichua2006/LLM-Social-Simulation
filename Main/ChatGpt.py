# Importing necessary libraries
import numpy as np  # numpy for numerical computations
import os  # os for accessing environment variables
import openai  # OpenAI for interacting with the GPT-3 model

# Setting the OpenAI API key
cheops_key='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'# for testing purposes
charles_key="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"

os.environ["OPENAI"] = charles_key

openai.api_key = os.environ["OPENAI"]
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
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs,top_p=top_prob)
      # Check the status of the response
      status_code = response["choices"][0]["finish_reason"]
      assert status_code == "stop", f"The status code was {status_code}."
      # Return the content of the response
      return response["choices"][0]["message"]["content"]
    except Exception as e:
      print("An Exception Occur when communicating with ChatGPT:",e)
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from text2speech import text_to_speech
from speech2text import speech_to_text

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))

# Creating a thread of a conversation with the assistant
thread = client.beta.threads.create()

# Setting up the assistant
assistant = client.beta.assistants.create(
    name="Eve",
    instructions="Your name is Eve. You are a verbal language model inside of a children's toy that helps 3-6 year old "
                 "kids in hospitals to overcome their preoperative anxiety and stress and deal with their emotions. "
                 "Answer each question in a friendly, supportive, caring and hope inspiring way. Try not to give "
                 "overly long responces and try not to exceed 4 sentences. If you are asked to explain something, "
                 "do it very straighforward and simple, so that any child could understand it. If you are asked to "
                 "tell a story, always generate a story with a happy ending that will make the child feel better. "
                 "Always encourage children to share their emotions and concern with you, then address them and help "
                 "to manage them. Help children cope with their emotions in an effective way, using the emotional "
                 "support strategies. Act so that a child could assosiate you with a friend and someone who could "
                 "always listen and support him. Your ultimate goal is to maintain the children's mental wellbeing.",
    model="gpt-3.5-turbo-0125"  # the most cost effitient model so far
)


def generate_response(content):
    global thread

    # create a message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Every 0.5 sec checking if the response from assistant is ready
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    return messages.data[0].content[0].text.value


while True:
    prompt = speech_to_text()
    print("You: " + prompt)
    response = generate_response(prompt)
    print("Eve: " + response)
    text_to_speech(response)

import ollama
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content="Hi, I'm your (virtual) System Dynamics Scientist. I can help you see the future. How can I help you today?"
    ).send()

@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    chat_history.append({"role": "user", "content": query.content})

    response = cl.Message(content="")
    answer = ollama.chat(model="llama3", messages=chat_history, stream=True)

    complete_answer = ""
    for token_dict in answer:
        token = token_dict["message"]["content"]
        complete_answer += token
        await response.stream_token(token)

    chat_history.append({"role": "assistant", "content": complete_answer})
    cl.user_session.set("chat_history", chat_history)

    await response.send()


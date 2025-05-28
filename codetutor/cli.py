import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from agents import Agent, Runner

from codetutor import config
from codetutor.config import get_conversation_dir
from codetutor.core import print_tutor_response


async def tutor(force_model_select=False):
    agent = Agent(
        name="Code Tutor",
        instructions=(
            "You are an expert coding tutor. "
            "You guide students step by step through learning to code. "
            "Use the Socratic method. Do NOT explain the entire concept at once. "
            "Instead, ask one thoughtful, guiding question at a time. "
            "Wait for the student's reply before continuing. "
            "Make the lesson conversational. "
            "Provide concise explanations and usable examples. "
            "If I say 'please give me this answer', confirm before answering directly."
        ),
        model=config.get_model(force_select=force_model_select),
    )

    history = []
    print("\nWhat coding topic are we covering today?\nUse [q] to quit\n")

    while True:
        user_input = await asyncio.to_thread(input, "You: ")
        if user_input.lower() in ["q", "exit"]:
            save_conversation(history, model=agent.model)
            break

        history.append({"role": "user", "content": user_input})
        conversation = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in history
        )
        result = await Runner.run(agent, conversation)
        history.append({"role": "assistant", "content": result.final_output})
        print_tutor_response(result.final_output)


def save_conversation(history, model="unknown"):
    from codetutor.config import get_conversation_dir

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
    output_dir = get_conversation_dir()

    # Try to get topic from first user message
    topic = ""
    for entry in history:
        if entry["role"] == "user":
            topic = entry["content"].strip().split(" ")[0:5]
            break

    slug = "_".join(topic).lower()
    slug = "".join(c for c in slug if c.isalnum() or c in ("_", "-"))

    filename = output_dir / f"{timestamp}_{slug}.md"

    with open(filename, "w") as f:
        f.write(f"# Code Tutor Session - {timestamp}\n")
        f.write(f"**Model:** {model}\n")
        if topic:
            f.write(f"**Topic:** {' '.join(topic)}\n\n")
        for entry in history:
            role = entry["role"].capitalize()
            content = entry["content"]
            f.write(f"### {role}\n{content}\n\n")

    print(f"\n📄 Conversation saved to `{filename}`\n")


def main():
    force_model_select = "--change-model" in sys.argv
    asyncio.run(tutor(force_model_select=force_model_select))


if __name__ == "__main__":
    main()

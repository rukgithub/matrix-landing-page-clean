import os
from openai import OpenAI

# Basis opsætning uden ekstra netværkskonfiguration
client = OpenAI(
    timeout=30.0,
    max_retries=2,
)


def simple_chat():
    try:
        print("Sender anmodning...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Sig hej på dansk"}
            ]
        )

        print("\nSvar modtaget:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Fejl opstod: {type(e).__name__}")
        print(f"Fejlbesked: {str(e)}")


if __name__ == "__main__":
    simple_chat()
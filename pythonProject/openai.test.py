import os
from openai import OpenAI


def simple_chat():
    try:
        print("Starter chat med OpenAI...")

        # Opret client
        client = OpenAI(
            timeout=30.0,
            max_retries=2,
        )

        # Send anmodning
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Sig hej på dansk og forklar kort hvad du er"}
            ]
        )

        # Print svar
        print("\nSvar modtaget:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"\nFejl opstod: {type(e).__name__}")
        print(f"Fejlbesked: {str(e)}")


if __name__ == "__main__":
    simple_chat()
import os
import openai

def main():
    # Hent API-nøglen fra miljøvariabler
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Fejl: OPENAI_API_KEY miljøvariabel er ikke sat.")
        return

    openai.api_key = api_key

    try:
        # Lav API-kaldet til GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Brug "gpt-4" eller den model du har adgang til
            messages=[
                {"role": "system", "content": "Du er en sjov assistent."},
                {"role": "user", "content": "Fortæl mig en sjov vittighed."}
            ],
            max_tokens=100,  # Begræns output for hurtigere respons
            temperature=0.7  # Juster kreativiteten
        )

        # Udskriv svaret
        message = response['choices'][0]['message']['content']
        print("GPT-4 siger:")
        print(message)

    except openai.error.OpenAIError as e:
        print(f"Der opstod en fejl: {e}")

if __name__ == "__main__":
    main()

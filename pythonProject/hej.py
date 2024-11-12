import openai

# Indsæt din OpenAI API-nøgle her
openai.api_key = "din_api_nøgle_here"  # Udskift med din API-nøgle

def main():
    # Skriv en kreativ prompt til GPT-4
    prompt = (
        "Skriv en sjov og absurd historie om, hvordan en robot og en kartoffel "
        "bliver bedste venner på en tur til rummet. Inkluder nogle skøre situationer "
        "og sjove dialoger mellem dem."
    )

    try:
        # Lav API-kaldet til GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du er en sjov og kreativ historiefortæller."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8  # Gør output mere kreativt og uforudsigeligt
        )

        # Udskriv historien
        story = response['choices'][0]['message']['content']
        print("Her er en sjov historie fra GPT-4:")
        print(story)

    except openai.error.OpenAIError as e:
        print(f"Der opstod en fejl: {e}")

if __name__ == "__main__":
    main()

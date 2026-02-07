import openai
import os

def summarize_recon(recon_data):
    api_key = os.getenv("OPENAI_API_KEY")  # make sure this matches your .env
    client = openai.OpenAI(api_key=api_key)

    prompt = f"You're an ethical hacker. Summarize this recon data:\n\n{recon_data}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI error: {e}"

    
    
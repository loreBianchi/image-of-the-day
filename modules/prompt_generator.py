import subprocess
import textwrap

def generate_prompt(titles):
    """
    Use Ollama (e.g. Llama3) to transform news headlines into a high-quality artistic prompt for image generation.
    """
    system_prompt = textwrap.dedent("""
    You are an expert AI art director.
    Your job is to take real news headlines and turn them into imaginative, artistic image prompts
    for a text-to-image AI model (Stable Diffusion).
    
    Rules:
    - Write in English.
    - Describe a single cohesive artistic scene inspired by 5 random headlines combined.
    - Remove any specific names, places, or real-world references.
    - Remove violent, political, or sensitive content.
    - Emphasize creativity and visual impact.                                    
    - Use vivid, creative language to evoke strong imagery.
    - Focus on atmosphere, emotion, lighting, composition, and artistic style.
    - Use detailed visual language (colors, environment, subjects, mood).
    - Avoid mentioning real people, logos, or text.
    - Finish with a cinematic, digital-art tone.
    """)

    joined_titles = "\n".join(f"- {t}" for t in titles)

    user_prompt = f"""
    Create an artistic image prompt inspired by these headlines:
    {joined_titles}
    """

    # Combine system + user prompt for clarity
    full_prompt = f"{system_prompt}\n\n{user_prompt}".strip()

    # Execute Ollama command
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", full_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output

    except subprocess.CalledProcessError as e:
        print("❌ Errore durante l'esecuzione di Ollama:", e)
        print("Output:", e.output)
        return None
    except FileNotFoundError:
        print("❌ Ollama non trovato. Assicurati che sia installato e nel PATH.")
        return None
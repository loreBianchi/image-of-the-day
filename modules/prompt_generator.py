import textwrap
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def generate_prompt_gemini(titles):
    """
    Usa l'API di Gemini (es. Gemini 2.5 Flash) per trasformare i titoli delle notizie 
    in un prompt artistico di alta qualità per la generazione di immagini.
    """
    # 1. Initialize Gemini Client
    # The API key will be automatically read from the GEMINI_API_KEY environment variable
    try:
        client = genai.Client()
    except Exception as e:
        print("❌ Error initializing Gemini client. Make sure the GEMINI_API_KEY environment variable is set correctly.")
        print(f"Details: {e}")
        return None

    # 2. Define the System Prompt (Instructions for the model)
    system_instruction = textwrap.dedent("""
    You are an expert AI art director.
    Your job is to take real news headlines and turn them into imaginative, artistic image prompts
    for a text-to-image AI model (Stable Diffusion).
    
    Rules:
    - Write in English.
    - Describe a single cohesive artistic scene inspired by 5 random headlines combined.
    - Remove violent, or sensitive content.
    - Emphasize creativity and visual impact.                                    
    - Use vivid, creative language to evoke strong imagery.
    - Focus on atmosphere, emotion, lighting, composition, and artistic style.
    - Use detailed visual language (colors, environment, subjects, mood).
    - Finish with a cinematic, digital-art tone.
    """).strip()

    # 3. Define the User Prompt (Specific input)
    joined_titles = "\n".join(f"- {t}" for t in titles)

    user_prompt = f"""
    Create an artistic image prompt inspired by these headlines:
    {joined_titles}
    """

    # 4. Call the Gemini API
    try:
        # Model configuration
        config = types.GenerateContentConfig(
            # Provides high-level instructions to guide the model's behavior
            system_instruction=system_instruction,
            # Sets the temperature to encourage creativity (higher values = more random)
            temperature=0.9, 
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash', # A fast and efficient model, suitable for the free tier
            contents=user_prompt,
            config=config,
        )

        # 5. Returns the generated text
        return response.text.strip()

    except Exception as e:
        print("❌ Error during Gemini API call:", e)
        return None


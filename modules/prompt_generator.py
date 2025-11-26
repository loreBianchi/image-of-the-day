import textwrap
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def generate_prompt(titles):
    """
    Uses the Gemini API (e.g. Gemini 2.5 Flash) to transform news headlines
    into a high-quality artistic prompt for image generation.
    """
    # 1. Initialize Gemini Client
    # The API key will be automatically read from the GEMINI_API_KEY environment variable
    try:
        client = genai.Client()
    except Exception as e:
        print(
            "❌ Error initializing Gemini client. Make sure the GEMINI_API_KEY environment variable is set correctly."
        )
        print(f"Details: {e}")
        return None

    # 2. Define the System Prompt (Instructions for the model)
    system_instruction = textwrap.dedent("""
    You are an expert AI Art Director for a daily digital gallery. Your task is to synthesize 5 diverse news headlines into a single, highly imaginative, and detailed image prompt for a text-to-image AI model (e.g., Stable Diffusion, Midjourney).

    ### INSTRUCTIONS:
    1.  **Language:** Write the final prompt strictly in **English**.
    2.  **Synthesis:** Create one cohesive, narrative scene that weaves together the *mood, themes, or symbolic elements* present in the 5 combined headlines.
    3.  **Avoid Literalism:** Do not simply describe the headlines. Do not mention specific people, political events, brands, or places by name. Remove all sensitive, violent, or explicit content.
    4.  **Focus:** Emphasize abstract ideas, emotion, and dramatic visual tension.

    ### PROMPT STRUCTURE (MUST USE ALL SECTIONS):
    Your output must be a single, flowing string, designed for maximum artistic quality.

    1.  **Subject & Scene:** Start with the main subject and the core narrative (e.g., "A lone astronomer standing on a crystalline shore...").
    2.  **Visual Details:** Integrate key colors, lighting, environment, and textures (e.g., "...bathed in deep, saturated indigo light, reflections shimmer on wet black sand...").
    3.  **Artistic & Technical Style:** Specify the desired final artistic medium and technical quality (e.g., "hyper-detailed, cinematic volumetric lighting, 8k, concept art, trending on ArtStation").

    ### FINISHING TONE:
    The final prompt must be a single, descriptive masterpiece ready for image generation.
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
            model="gemini-2.5-flash",  # A fast and efficient model, suitable for the free tier
            contents=user_prompt,
            config=config,
        )

        # 5. Returns the generated text
        return response.text.strip()

    except Exception as e:
        print("❌ Error during Gemini API call:", e)
        return None

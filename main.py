import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Get API key from secrets
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

model_mapper = {
    "gemini": GeminiModel,
    "openai": OpenAIModel,
}

if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

default_prompt = (
    "Generate a single-line, elegant signature for name <name-here> using a dark blue pen on a clean white background. "
    "The signature should have smooth, continuous lines without breaks, unnecessary flourishes, or extra elements. "
    "Avoid multiple strokes on a single letter and ensure clarity and professionalism."
)

def check_signature(image):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Evaluate this signature image. Is it clear, readable, and does it accurately represent the given name? "
                "Ensure there are no missing or extra letters, and that it looks like a professional signature.",
                "The signature should have smooth, continuous lines without breaks, unnecessary flourishes, or extra elements. "
                "Avoid multiple strokes on a single letter and ensure clarity and professionalism. Your answer should be only YES OR NO",
                image],
            config=types.GenerateContentConfig(response_modalities=['Text'])
        )

        evaluation = response.candidates[0].content.parts[0].text
        if "no" in evaluation.lower().strip():
            st.write("❌ Спроба відхилена. Генеруємо нову...")
            return False
        else:
            st.write("✅ Підпис успішно згенеровано!")
            return True
    except Exception as e:
        st.error(f"Error checking signature: {e}")
        return False

def generate_signature(full_name, custom_prompt):
    image_container = st.container()
    prompt = custom_prompt
    generated_count = 0

    try:
        with image_container:
            cols = st.columns(3)
            for i in range(9):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=prompt,
                    config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
                )

                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        if check_signature(image):
                            st.session_state.generated_images.append(image)
                            with cols[generated_count % 3]:
                                st.image(image, use_container_width=True)
                            generated_count += 1
                        else:
                            i -= 1

                if generated_count >= 9:
                    break

    except Exception as e:
        st.error(f"Error generating signature: {e}")

st.title("SignUs | Signature Generator")
st.write(
    "Enter your name and generate a unique signature. Click 'Generate More' to create additional styles.")

full_name = st.text_input("Enter your full name ### Now don't used, add this into prompt", disabled=True)

custom_prompt = st.text_area("Customize your signature prompt", value=default_prompt)

if st.button("Generate Signature"):
    generate_signature(full_name, custom_prompt)
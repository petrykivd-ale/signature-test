import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Get API key from secrets
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

if 'checking_status' not in st.session_state:
    st.session_state.checking_status = "Waiting for generation..."

default_prompt = (
    "Generate a single-line, elegant signature for name <name-here> using a dark blue pen on a clean white background. "
    "The signature should have smooth, continuous lines without breaks, unnecessary flourishes, or extra elements. "
    "Avoid multiple strokes on a single letter and ensure clarity and professionalism."
)

def check_signature(image):
    st.session_state.checking_status = "Evaluating signature quality..."
    st.progress(50)

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
        print(evaluation)
        if "no" in evaluation.lower().strip():
            st.session_state.checking_status = "Signature rejected. Regenerating..."
            st.progress(100)
            st.text("Trying again... Not acceptable by evaluation agent.\n You can stop it by using the stop button in the upper right corner")
            return False
        else:
            st.session_state.checking_status = "Signature accepted!"
            st.text("Signature accepted! Ready to generate more signatures.")
            st.progress(100)
            return True
    except Exception as e:
        st.error(f"Error checking signature: {e}")
        return False

def generate_signature(full_name, custom_prompt):
    st.session_state.checking_status = "Generating signatures..."
    progress_text = st.empty()  # Create a placeholder for progress text
    progress_bar = st.progress(0)  # Create a progress bar
    image_container = st.container()  # Create a container for images
    
    prompt = custom_prompt
    generated_count = 0

    try:
        with image_container:
            cols = st.columns(3)
            for i in range(9):
                progress_text.text(f"Generating signature {i+1}/9...")
                progress_bar.progress((i + 1) * 11)  # Update progress bar

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
                            # Display the image immediately after generation
                            with cols[generated_count % 3]:
                                st.image(image, use_container_width=True)
                            generated_count += 1
                        else:
                            # If signature is rejected, try again for this position
                            i -= 1

                if generated_count >= 9:  # Stop if we have 9 successful generations
                    break

        progress_text.text("Generation completed!")
        progress_bar.progress(100)

    except Exception as e:
        st.error(f"Error generating signature: {e}")

st.title("SignUs | Signature Generator")
st.write(
    "Enter your name and generate a unique signature. Click 'Generate More' to create additional styles.")

full_name = st.text_input("Enter your full name ### Now don't used, add this into prompt", disabled=True)

custom_prompt = st.text_area("Customize your signature prompt", value=default_prompt)

if st.button("Generate Signature"):
    generate_signature(full_name, custom_prompt)

st.text(st.session_state.checking_status)
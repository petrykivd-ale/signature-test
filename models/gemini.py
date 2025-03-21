import streamlit as st

from PIL import Image
from google import genai
from google.genai import types
from io import BytesIO

from models.base import BaseGenerativeModel


class GeminiModel(BaseGenerativeModel):

    def __init__(self):
        api_key = st.secrets["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, evaluation_prompt: str) -> Image.Image | None:
        image_container = st.container()
        generated_count = 0

        try:
            with image_container:
                cols = st.columns(3)
                for i in range(9):
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash-exp-image-generation",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["Text", "Image"]
                        ),
                    )

                    for part in response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            image = Image.open(BytesIO(part.inline_data.data))
                            if self.evaluate(image, evaluation_prompt):
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

    def evaluate(self, image: Image.Image, evaluation_prompt: str) -> bool:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[evaluation_prompt, image],
                config=types.GenerateContentConfig(response_modalities=["Text"]),
            )

            evaluation = response.candidates[0].content.parts[0].text
            if "no" in evaluation.lower().strip():
                st.write("❌ Signature rejected! Try to resolve conflict...")
                return False
            else:
                st.write("✅ Signature accepted!")
                return True
        except Exception as e:
            st.error(f"Error checking signature: {e}")
            return False


class GeminiModelV3(GeminiModel):

    def generate(self, prompt: str, evaluation_prompt: str) -> Image.Image | None:
        image_container = st.container()
        generated_count = 0

        try:
            with image_container:
                cols = st.columns(3)

                for i in range(3):
                    response = self.client.models.generate_images(
                        model="imagen-3.0-generate-002",
                        prompt=prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=3,
                        ),
                    )

                    for generated_image in response.generated_images:
                        image = Image.open(BytesIO(generated_image.image.image_bytes))
                        if self.evaluate(image, evaluation_prompt):
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

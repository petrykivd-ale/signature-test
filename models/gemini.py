import streamlit as st

from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from models.base import BaseGenerativeModel


class GeminiModel(BaseGenerativeModel):
    model = "gemini-2.0-flash-exp-image-generation"

    def __init__(self):
        api_key = st.secrets["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)

    def _generate_images(
        self,
        prompts: list[dict],
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        image_container = st.container()
        try:
            with image_container:
                cols = st.columns(3)
                for i, prompt in enumerate(prompts):
                    print(i, prompt)
                    for v in prompt.values():
                        prompt_text = v

                    image = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt_text,
                        config=types.GenerateContentConfig(
                            response_modalities=["Text", "Image"]
                        ),
                    )
                    self._process_response(
                        image=image,
                        cols=cols,
                        index=i,
                        prompt=prompt,
                        evaluation_prompt=evaluation_prompt,
                        is_additional=is_additional,
                    )

        except Exception as e:
            st.error(f"Error generating images: {e}")

    def _evaluate(self, image: Image.Image, evaluation_prompt: str) -> bool:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[evaluation_prompt, image],
                config=types.GenerateContentConfig(response_modalities=["Text"]),
            )
            evaluation = response.candidates[0].content.parts[0].text
            if "no" in evaluation.lower().strip():
                st.write("❌ Signature rejected!")
                return False
            else:
                st.write("✅ Signature accepted!")
                return True
        except Exception as e:
            st.error(f"Error evaluating signature: {e}")
            return False

    def _process_response(
        self,
        image: bytes,
        cols: list,
        index: int,
        prompt: dict,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        for part in image.candidates[0].content.parts:
            if part.inline_data is not None:
                img = Image.open(BytesIO(part.inline_data.data))
                self._display_image(
                    image=img,
                    cols=cols,
                    index=index,
                    prompt=prompt,
                    evaluation_prompt=evaluation_prompt,
                    is_additional=is_additional,
                )


class GeminiModelV3(GeminiModel):
    model = "imagen-3.0-generate-002"

    def _generate_images(
        self,
        prompts: list[dict],
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        image_container = st.container()
        try:
            with image_container:
                cols = st.columns(3)
                for i, prompt in enumerate(prompts):
                    for v in prompt.values():
                        prompt_text = v

                    image = self.client.models.generate_images(
                        model=self.model,
                        prompt=prompt_text,
                        config=types.GenerateImagesConfig(number_of_images=1),
                    )
                    self._process_response(
                        image=image,
                        cols=cols,
                        index=i,
                        prompt=prompt,
                        evaluation_prompt=evaluation_prompt,
                        is_additional=is_additional,
                    )
        except Exception as e:
            st.error(f"Error generating images: {e}")

    def _process_response(
        self,
        image: bytes,
        cols: list,
        index: int,
        prompt: dict,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        for generated_image in image.generated_images:
            img = Image.open(BytesIO(generated_image.image.image_bytes))
            self._display_image(
                image=img,
                cols=cols,
                index=index,
                prompt=prompt,
                evaluation_prompt=evaluation_prompt,
                is_additional=is_additional,
            )

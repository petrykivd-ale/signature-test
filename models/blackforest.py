import time
import streamlit as st
import requests

from PIL import Image
from io import BytesIO

from models.gemini import GeminiModel


class BflGenerativeModel(GeminiModel):
    def __init__(self):
        super().__init__()
        self.bfl_api_key = st.secrets["BLF_API_KEY"]

    def generate(
        self, prompt: str, evaluation_prompt: str | None, num_of_images: int = 3
    ) -> Image.Image | None:
        image_container = st.container()

        try:
            with image_container:
                cols = st.columns(3)
                for i in range(num_of_images):
                    response = requests.post(
                        "https://api.us1.bfl.ai/v1/flux-dev",
                        headers={
                            "accept": "application/json",
                            "x-key": self.bfl_api_key,
                            "Content-Type": "application/json",
                        },
                        json={
                            "prompt": prompt,
                        },
                    ).json()

                    generated_image = self._get_image(response["id"])
                    self._process_response(generated_image, cols, i, evaluation_prompt)

        except Exception as e:
            st.error(f"Error generating image: {e}")

    def _process_response(self, response, cols, index, evaluation_prompt):
        image = Image.open(BytesIO(response))
        self._display_image(image, cols, index, evaluation_prompt)

    def _get_image(self, request_id: str) -> bytes:
        while True:
            time.sleep(0.5)
            result = requests.get(
                "https://api.us1.bfl.ai/v1/get_result",
                headers={
                    "accept": "application/json",
                    "x-key": self.bfl_api_key,
                },
                params={"id": request_id},
            ).json()

            if result["status"] == "Ready":
                image = requests.get(result["result"]["sample"])
                return image.content

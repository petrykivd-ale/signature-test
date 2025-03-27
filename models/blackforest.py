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

    def _generate_images(
        self,
        prompts: list[dict],
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        image_container = st.container()
        try:
            with image_container:
                cols = st.columns(5)
                for i, prompt in enumerate(prompts):
                    for v in prompt.values():
                        prompt_text = v

                    response = requests.post(
                        "https://api.us1.bfl.ai/v1/flux-dev",
                        headers={
                            "accept": "application/json",
                            "x-key": self.bfl_api_key,
                            "Content-Type": "application/json",
                        },
                        json={"prompt": prompt_text},
                    )
                    if response.status_code == 402:
                        st.error("Insufficient credits to generate images.")
                        return

                    generated_image = self._get_image(response.json()["id"])
                    self._process_response(
                        image=generated_image,
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
        evaluation_prompt: str,
        is_additional: bool = True,
    ):
        img = Image.open(BytesIO(image))
        self._display_image(
            image=img,
            cols=cols,
            index=index,
            prompt=prompt,
            evaluation_prompt=evaluation_prompt,
            is_additional=is_additional,
        )

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

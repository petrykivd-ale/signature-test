import time
import streamlit as st
import requests

from PIL import Image
# from io import BytesIO

from models.base import BaseGenerativeModel


class BflGenerativeModel(BaseGenerativeModel):
    def __init__(self):
        self.api_key = st.secrets["BFL_API_KEY"]

    def generate(self, prompt: str, evaluation_prompt: str) -> Image.Image | None:
        image_container = st.container()
        # generated_count = 0

        with image_container:
            try:
                response = requests.post(
                    "https://api.us1.bfl.ai/v1/flux-pro-1.1",
                    headers={
                        "accept": "application/json",
                        "x-key": self.api_key,
                        "Content-Type": "application/json",
                    },
                    json={
                        "prompt": prompt,
                        "width": 1024,
                        "height": 768,
                    },
                ).json()

                # cols = st.columns(3)

                # for generated_image in response.generated_images:
                #     image = Image.open(BytesIO(generated_image.image.image_bytes))
                #     if self.evaluate(image, evaluation_prompt):
                #         st.session_state.generated_images.append(image)
                #         with cols[generated_count % 3]:
                #             st.image(image, use_container_width=True)
                #         generated_count += 1
                #     else:
                #         i -= 1

                #     if generated_count >= 9:
                #         break

                # image = Image.open(BytesIO(response["image"]))
                # st.image(image, use_container_width=True)

            except Exception as e:
                st.error(f"Error generating image: {e}")

    def get_response(self, request_id):
        time.sleep(1)
        result = requests.get(
            "https://api.us1.bfl.ai/v1/get_result",
            headers={
                "accept": "application/json",
                "x-key": self.api_key,
            },
            params={
                "id": request_id,
            },
        ).json()
        if result["status"] == "Ready":
            print(f"Result: {result['result']['sample']}")
        else:
            print(f"Status: {result['status']}")

import streamlit as st

from abc import ABC, abstractmethod
from PIL import Image


class IBaseGenerativeModel(ABC):
    model = None

    @abstractmethod
    def __init__(self):
        """Initialize model with its specific API key from st.secrets"""
        pass

    @abstractmethod
    def generate(
        self,
        prompts: list,
        evaluation_prompt: str | None = None,
    ):
        """Generate image based on prompt"""
        pass

    @abstractmethod
    def generate_more(
        self,
        prompt: str,
        evaluation_prompt: str | None = None,
        is_additional: bool = False,
    ):
        """Generate more images based on prompt"""
        pass

    @abstractmethod
    def _generate_images(
        self,
        prompts: list,
        num_of_images: int,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        """Generate images based on prompts"""
        pass

    @abstractmethod
    def _evaluate(self, image: Image.Image, evaluation_prompt: str) -> bool:
        """Evaluate generated image"""
        pass

    @abstractmethod
    def _process_response(
        self,
        image: bytes,
        cols: list,
        index: int,
        prompt: str,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        """Process response from model"""
        pass

    @abstractmethod
    def _display_image(
        self,
        image: Image.Image,
        cols: list,
        index: int,
        prompt: str,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        """Display generated image"""
        pass


class BaseGenerativeModel(IBaseGenerativeModel):

    def generate(
        self,
        prompts: list[dict],
        evaluation_prompt: str | None = None,
    ):
        self._generate_images(prompts, evaluation_prompt)

    def generate_more(
        self,
        prompt: dict,
        evaluation_prompt: str | None = None,
        is_additional: bool = False,
    ):
        self._generate_images(
            [prompt] * 9, evaluation_prompt, is_additional
        )

    def _display_image(
        self,
        image: Image.Image,
        cols: list,
        index: int,
        prompt: dict,
        evaluation_prompt: str | None = None,
        is_additional: bool = True,
    ):
        def on_click():
            st.session_state.trigger_generate_more = True
            st.session_state.generate_more_prompt = prompt

        if evaluation_prompt is not None:
            if self._evaluate(image, evaluation_prompt):
                st.session_state.generated_images.append(image)
                with cols[index % 3]:
                    st.image(image, use_container_width=True)
                    if is_additional:
                        st.button("Show more like this", on_click=on_click, key=index)
        else:
            st.session_state.generated_images.append(image)
            with cols[index % 5]:
                st.image(image, use_container_width=True)
                if is_additional:
                    st.button("Show more like this", on_click=on_click, key=index)

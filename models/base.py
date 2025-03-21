import streamlit as st

from abc import ABC, abstractmethod
from PIL import Image
from typing import Optional


class IBaseGenerativeModel(ABC):
    model = None

    @abstractmethod
    def __init__(self):
        """Initialize model with its specific API key from st.secrets"""
        pass

    @abstractmethod
    def generate(self, prompt: str, evaluation_prompt: str) -> Optional[Image.Image]:
        """Generate image based on prompt"""
        pass

    @abstractmethod
    def _evaluate(self, image: Image.Image, evaluation_prompt: str) -> bool:
        """Evaluate generated image"""
        pass

    @abstractmethod
    def _display_image(self, image, cols, index, evaluation_prompt):
        """Display generated image"""
        pass

    @abstractmethod
    def _process_response(self, response, cols, index, evaluation_prompt):
        """Process response from model"""
        pass


class BaseGenerativeModel(IBaseGenerativeModel):
    def __init__(self):
        pass

    def generate(self, prompt: str, evaluation_prompt: str) -> Optional[Image.Image]:
        pass

    def _evaluate(self, image: Image.Image, evaluation_prompt: str) -> bool:
        pass

    def _display_image(self, image, cols, index, evaluation_prompt):
        if evaluation_prompt is not None:
            if self._evaluate(image, evaluation_prompt):
                st.session_state.generated_images.append(image)
                with cols[index % 3]:
                    st.image(image, use_container_width=True)
        else:
            st.session_state.generated_images.append(image)
            with cols[index % 3]:
                st.image(image, use_container_width=True)

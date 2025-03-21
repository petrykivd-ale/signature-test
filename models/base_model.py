from abc import ABC, abstractmethod
from PIL import Image
import streamlit as st
from typing import Optional

class BaseGenerativeModel(ABC):
    @abstractmethod
    def __init__(self):
        """Initialize model with its specific API key from st.secrets"""
        pass

    @abstractmethod
    def generate(self, prompt: str) -> Optional[Image.Image]:
        """Generate image based on prompt"""
        pass

    @abstractmethod
    def evaluate(self, image: Image.Image) -> bool:
        """Evaluate generated image"""
        pass 
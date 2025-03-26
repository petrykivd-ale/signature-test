
import streamlit as st
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class FontSignatureService:
    """Service for generating font-based signatures."""

    def generate(self, name: str):
        fonts_dir = Path("fonts/")
        if not fonts_dir.exists() or not fonts_dir.is_dir():
            st.error("Error generating signatures")
            return

        image_container = st.container()

        with image_container:
            cols = st.columns(3)

            for i, file in enumerate(fonts_dir.iterdir()):
                if file.is_file():
                    img = self.create(name, file)
                    self._display_image(file.stem, img, cols, i)

    @staticmethod
    def create(text: str, font_path: Path):
        # Create image with white background
        img = Image.new("RGB", (512, 256), color="white")
        d = ImageDraw.Draw(img)

        # Load the font
        font = ImageFont.truetype(str(font_path), 40)

        bbox = d.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2

        # Draw text
        d.text((x, y), text, font=font, fill="darkblue")

        # Save image to buffer
        with io.BytesIO() as buffer:
            img.save(buffer, format="JPEG")
            buffer.seek(0)

            img = Image.open(io.BytesIO(buffer.getvalue()))
            return img

    def _display_image(
        self,
        font_name: str,
        image: Image.Image,
        cols: list,
        index: int,
    ):
        st.session_state.generated_images.append(image)
        with cols[index % 3]:
            st.text(font_name)
            st.image(image, use_container_width=True)

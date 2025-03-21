import streamlit as st

from models.gemini import GeminiModel, GeminiModelV3
from prompts import DEFAULT_PROMPT, EVALUATION_PROMPT


model_mapper = {
    "gemini": GeminiModel,
    "gemini_v3": GeminiModelV3,
}


if "generated_images" not in st.session_state:
    st.session_state.generated_images = []


st.title("SignUs | Signature Generator")
st.write(
    "Generate a unique signature. Click 'Generate More' to create additional styles."
)

option = st.selectbox(
    "Choose model for generation:",
    ("gemini", "gemini_v3"),
)


with st.expander("Signature Prompt"):
    signature_prompt = st.text_area(
        "Customize your signature prompt", value=DEFAULT_PROMPT
    )


with st.expander("Evaluation Prompt"):
    evaluation_prompt = st.text_area(
        "Customize your signature evaluation prompt", value=EVALUATION_PROMPT
    )


if st.button("Generate Signature"):
    model: GeminiModel | GeminiModelV3 = model_mapper[option]()
    model.generate(signature_prompt, evaluation_prompt)

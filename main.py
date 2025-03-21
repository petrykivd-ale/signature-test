import streamlit as st

from models.blackforest import BflGenerativeModel
from models.gemini import GeminiModel, GeminiModelV3
from prompts import DEFAULT_PROMPT, EVALUATION_PROMPT


model_mapper = {
    "gemini": GeminiModel,
    "gemini_v3": GeminiModelV3,
    "blackforest": BflGenerativeModel,
}


if "generated_images" not in st.session_state:
    st.session_state.generated_images = []


st.title("SignUs | Signature Generator")
st.write(
    "Generate a unique signature."
)

option = st.selectbox(
    "Choose model for generation:",
    ("gemini", "gemini_v3", "blackforest"),
)


with st.expander("Signature Prompt"):
    signature_prompt = st.text_area(
        "Customize your signature prompt", value=DEFAULT_PROMPT
    )


agree = st.checkbox("Turn evaluation prompt")

evaluation_prompt = None
if agree:
    evaluation_prompt = st.text_area(
        "Customize your signature evaluation prompt", value=EVALUATION_PROMPT
    )


if st.button("Generate Signature"):
    model = model_mapper[option]()
    model.generate(signature_prompt, evaluation_prompt)

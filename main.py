import streamlit as st

from models.blackforest import BflGenerativeModel
from models.gemini import GeminiModel, GeminiModelV3
from prompts import (
    DEFAULT_SIGNATURE_PROMPT,
    CHAOTIC_SIGNATURE_PROMPT,
    ELEGANT_SIGNATURE_PROMPT,
    FEMININE_HEART_SIGNATURE_PROMPT,
    CORPORATE_SIGNATURE_PROMPT,
    OLD_HOLLYWOOD_SIGNATURE_PROMPT,
    GRAFFITI_SIGNATURE_PROMPT,
    MIN_SHARP_SIGNATURE_PROMPT,
    CHILDLIKE_SIGNATURE_PROMPT,
    FLAMBOYANT_SIGNATURE_PROMPT,
    MASCULINE_SIGNATURE_PROMPT,
    FLAMBOYANT_FEMININE_PROMPT,
    EVALUATION_PROMPT,
    FEMININE_GEOMETRY_PROMPT,
    FEMININE_STAR_SIGNATURE_PROMPT,
)


model_mapper = {
    "gemini": GeminiModel,
    "gemini_v3": GeminiModelV3,
    "blackforest": BflGenerativeModel,
}


if "generated_images" not in st.session_state:
    st.session_state.generated_images = []


st.title("SignUs | Signature Generator")
st.write("Generate a unique signature.")

option = st.selectbox(
    "Choose model for generation:",
    ("gemini", "gemini_v3", "blackforest"),
)


with st.expander("Customize Signature Prompts"):
    default_signature_prompt = st.text_area(
        "Default Signature Prompt", value=DEFAULT_SIGNATURE_PROMPT
    )
    chaotic_signature_prompt = st.text_area(
        "Chaotic Signature Prompt", value=CHAOTIC_SIGNATURE_PROMPT
    )
    elegant_signature_prompt = st.text_area(
        "Elegant Signature Prompt", value=ELEGANT_SIGNATURE_PROMPT
    )
    feminine_heart_signature_prompt = st.text_area(
        "Feminine Heart Signature Prompt", value=FEMININE_HEART_SIGNATURE_PROMPT
    )
    feminine_star_signature_prompt = st.text_area(
        "Feminine Star Signature Prompt", value=FEMININE_STAR_SIGNATURE_PROMPT
    )
    feminine_geometry_signature_prompt = st.text_area(
        "Feminine Geometry Signature Prompt", value=FEMININE_GEOMETRY_PROMPT
    )
    corporate_signature_prompt = st.text_area(
        "Corporate Signature Prompt", value=CORPORATE_SIGNATURE_PROMPT
    )
    old_hollywood_signature_prompt = st.text_area(
        "Old Hollywood Signature Prompt", value=OLD_HOLLYWOOD_SIGNATURE_PROMPT
    )
    graffiti_signature_prompt = st.text_area(
        "Graffiti Signature Prompt", value=GRAFFITI_SIGNATURE_PROMPT
    )
    min_sharp_signature_prompt = st.text_area(
        "Minimalist Sharp Signature Prompt", value=MIN_SHARP_SIGNATURE_PROMPT
    )
    childlike_signature_prompt = st.text_area(
        "Childlike Signature Prompt", value=CHILDLIKE_SIGNATURE_PROMPT
    )
    flamboyant_signature_prompt = st.text_area(
        "Flamboyant Signature Prompt", value=FLAMBOYANT_SIGNATURE_PROMPT
    )
    masculine_signature_prompt = st.text_area(
        "Masculine Signature Prompt", value=MASCULINE_SIGNATURE_PROMPT
    )
    flamboyant_feminine_signature_prompt = st.text_area(
        "Flamboyant Feminine Signature Prompt", value=FLAMBOYANT_FEMININE_PROMPT
    )


agree = st.checkbox("Turn on evaluation prompt")

evaluation_prompt = None
if agree:
    evaluation_prompt = st.text_area(
        "Customize your signature evaluation prompt", value=EVALUATION_PROMPT
    )


model = model_mapper[option]()

prompts = [
    {"Standard & Clean": default_signature_prompt},
    {"Messy & Fast Scribble": chaotic_signature_prompt},
    {"Elegant Calligraphy": elegant_signature_prompt},
    {"Feminine & Bubbly (Heart Flourishes)": feminine_heart_signature_prompt},
    {"Feminine & Bubbly (Star Flourishes)": feminine_star_signature_prompt},
    {"Feminine & Bubbly (Geometric Flourishes)": feminine_geometry_signature_prompt},
    {"Corporate & Precise": corporate_signature_prompt},
    {"Old Hollywood Glam": old_hollywood_signature_prompt},
    {"Graffiti-Inspired": graffiti_signature_prompt},
    {"Minimalist Sharp": min_sharp_signature_prompt},
    {"Childlike & Naive": childlike_signature_prompt},
    {"Flamboyant Artistic": flamboyant_signature_prompt},
    {"Masculine": masculine_signature_prompt},
    {"Flamboyant Flourish – Feminine Signature Style": flamboyant_feminine_signature_prompt},
]

prompts_names = [list(prompt.keys())[0] for prompt in prompts]

options = st.multiselect(
    "What styles would you like?",
    prompts_names,
    prompts_names,
)

if st.button("Generate Signature"):
    selected_prompts = [prompt for prompt in prompts if list(prompt.keys())[0] in options]
    model.generate(selected_prompts, evaluation_prompt)


if st.session_state.get("trigger_generate_more"):
    st.write(f"More like: {list(st.session_state.generate_more_prompt)[0]}")
    model.generate_more(st.session_state.generate_more_prompt, evaluation_prompt)
    st.session_state.trigger_generate_more = False
    st.session_state.generate_more_prompt = ""

import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import json

from dotenv import load_dotenv

load_dotenv()
st.write("API Key Connected Successfully")
# Configuration

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Page Settings

st.set_page_config(
    page_title="AI Caption Generator",
    page_icon="🖼️",
    layout="centered"
)

# Header

st.title("🖼️ AI Image Caption & Alt-Text Generator")

st.markdown(
    """
Upload an image and generate:

- Formal Caption
- Casual Caption
- SEO Caption
- Accessibility Alt-Text
"""
)

st.divider()

# Upload Image

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

# Process Image


if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    st.write("")

    if st.button("Generate Captions"):

        with st.spinner("Analyzing image with Gemini AI..."):

            prompt = """
Analyze the image carefully.

Return ONLY valid JSON.

{
  "formal":"",
  "casual":"",
  "seo":"",
  "alt_text":""
}

Requirements:

formal:
Professional and objective.
2-3 sentences.

casual:
Friendly and conversational.

seo:
15-25 words.
Keyword rich.

alt_text:
Under 125 characters.
Accessibility friendly.
WCAG compliant.

Return JSON only.
"""

            try:

                response = model.generate_content(
                    [prompt, image]
                )

                result = response.text

                result = result.replace(
                    "```json",
                    ""
                )

                result = result.replace(
                    "```",
                    ""
                )

                captions = json.loads(result)

                st.success(
                    "Captions Generated Successfully!"
                )
                
                # Formal
                
                st.subheader("📌 Formal Caption")

                st.info(
                    captions["formal"]
                )
                
                # Casual
                
                st.subheader("😊 Casual Caption")

                st.success(
                    captions["casual"]
                )
                
                # SEO
                
                st.subheader("🚀 SEO Caption")

                st.warning(
                    captions["seo"]
                )
                
                # Alt Text
                
                st.subheader("♿ Alt Text")

                st.code(
                    captions["alt_text"]
                )
                
                # Download
                
                text_output = f"""
FORMAL CAPTION
--------------
{captions['formal']}

CASUAL CAPTION
--------------
{captions['casual']}

SEO CAPTION
-----------
{captions['seo']}

ALT TEXT
--------
{captions['alt_text']}
"""

                st.download_button(
                    label="📥 Download Captions",
                    data=text_output,
                    file_name="captions.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )
                 
                 

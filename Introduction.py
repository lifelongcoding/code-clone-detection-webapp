import streamlit as st

# Set page configuration for the introduction page
st.set_page_config(
    page_title="Welcome - LLM-based Code Clone Detector",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Main Page Content ---
st.title("👋 Welcome to the LLM-based Code Clone Detector!")

st.markdown("""
This application leverages Large Language Models (LLMs) to analyze and predict the similarity between two provided code snippets. It follows a simple two-step process:

1.  **Configuration:** Set up the analysis parameters.
2.  **Prediction:** Input code and get the similarity assessment.
""")

st.divider()

# --- Explanation of Pages ---
st.header("🧭 How to Use This Application")
st.markdown("""
Navigate through the pages in the sidebar to use the tool:
""")

# Explain Config Setup page
with st.container(border=True):
    st.subheader("1️⃣ Config Setup")
    st.markdown("""
    * **Purpose:** Configure the prompt and the LLM used for the similarity analysis.
    * **Steps:**
        * **Upload Prompt File:** Use the sidebar to upload a text file (`.txt`, `.md`, `.json`) containing the specific instructions (prompt) you want the LLM to follow when assessing code similarity. This file defines *how* similarity should be judged. (Uploading is optional if a prompt is already confirmed in the session).
        * **Select Model:** Choose the desired LLM (e.g., `deepseek-v3-241226`, `deepseek-r1-250120`) from the dropdown menu in the sidebar.
        * **Confirm Selection:** Click the "Confirm Selection" button in the sidebar. This saves your chosen prompt and model for the current session.
    * **Output:** The main page displays the content of the confirmed prompt file and the selected model.
    * **❗ Important:** You **must** confirm your settings on this page before proceeding to the prediction step.
    """)

# Explain Similarity Prediction page
with st.container(border=True):
    st.subheader("2️⃣ Similarity Prediction")
    st.markdown("""
    * **Purpose:** Input two code snippets and get a similarity prediction based on the settings configured in the previous step.
    * **Prerequisites:** You must have confirmed a prompt and model on the 'Config Setup' page.
    * **Steps:**
        * **Input Code:** Enter the two code snippets you want to compare into the text areas provided in the sidebar.
        * **Predict:** Click the "Predict Now" button in the sidebar.
    * **Output:**
        * The main page displays the **latest prediction result**, including a conclusion and the reasoning process (Chain of Thought) provided by the LLM.
        * The **input code snippets** for the latest prediction are also shown.
        * A **prediction history** for the current session is maintained and can be viewed in an expandable section.
    """)

st.divider()

st.info("🚀 **Get Started:** Navigate to the **Config Setup** page using the sidebar to begin!")

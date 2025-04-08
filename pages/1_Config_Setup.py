import streamlit as st

# --- Constants ---
MODEL_OPTIONS = ["deepseek-v3-241226", "deepseek-r1-250120"]  # Available models

st.set_page_config(page_title="Prompt Upload and Model Selection", layout="wide")

# --- Initialize Session State ---
if "confirmed_prompt" not in st.session_state:
    st.session_state.confirmed_prompt = None
if "confirmed_model" not in st.session_state:
    st.session_state.confirmed_model = None

# --- Sidebar Input ---
# Upload section
st.sidebar.header("📄 Upload Prompt File")
uploaded_file = st.sidebar.file_uploader("Select a text file", type=["txt", "md", "json"], key="prompt_uploader")

# Model selection section
st.sidebar.header("🤖 Select Model")
selected_model = st.sidebar.selectbox("Choose a model", MODEL_OPTIONS, key="model_selector")

confirm_button = st.sidebar.button("✅ Confirm")

# --- Main Page Output ---
st.title("📄 View Prompt and Confirm Model")

# --- Handle Confirm Button Click ---
if confirm_button:
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state["confirmed_prompt"] = file_content
            st.session_state["confirmed_model"] = selected_model
            st.sidebar.success(f"Prompt from '{uploaded_file.name}' and model '{selected_model}' confirmed!")
        except UnicodeDecodeError:
            st.sidebar.error(f"Error: Could not decode the file '{uploaded_file.name}'. Please ensure it is UTF-8 encoded.")
        except Exception as e:
            st.sidebar.error(f"An error occurred while reading the file: {e}")
    else:
        st.sidebar.warning("Please upload a prompt file before confirming.")

# --- Display confirmed info if available in session state ---
if st.session_state.confirmed_prompt is not None and st.session_state.confirmed_model is not None:
    with st.container(border=True):
        st.subheader("✅ Selected Model")
        st.markdown("---")
        st.info(f"The selected model is: `{st.session_state['confirmed_model']}`")

    with st.container(border=True):
        st.subheader("📄 Confirmed Prompt File Content")
        st.markdown("---")
        content = st.session_state.confirmed_prompt
        st.markdown(content)
else:
    # Show instruction if nothing is confirmed yet
    st.warning("⚠️ Please upload a prompt file, select a model, and click 'Confirm' in the sidebar.")

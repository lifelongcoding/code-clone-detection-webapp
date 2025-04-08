import streamlit as st

# --- Constants ---
MODEL_OPTIONS = ["deepseek-v3-241226", "deepseek-r1-250120"]  # Available models

st.set_page_config(page_title="Prompt Upload and Model Selection", layout="wide")

# --- Initialize Session State ---
if "confirmed_prompt" not in st.session_state:
    st.session_state.confirmed_prompt = None
if "confirmed_model" not in st.session_state:
    st.session_state.confirmed_model = None
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None  # Keep track of the confirmed prompt's filename

# --- Sidebar Input ---
# Prompt upload section
st.sidebar.header("📄 Upload Prompt File")
uploaded_file = st.sidebar.file_uploader(
    "Select a text file (Optional after first confirmation)",
    type=["txt", "md", "json"],
    key="prompt_uploader"
)

# Model selection section
st.sidebar.header("🤖 Select Model")
# Set the default selection based on the confirmed model if available
current_model_index = 0
if st.session_state.confirmed_model in MODEL_OPTIONS:
    try:
        current_model_index = MODEL_OPTIONS.index(st.session_state.confirmed_model)
    except ValueError:
        # Handle case where the saved model is no longer in options
        current_model_index = 0

selected_model = st.sidebar.selectbox(
    "Choose a model",
    MODEL_OPTIONS,
    index=current_model_index,  # Set initial selection based on session state
    key="model_selector"
)

confirm_button = st.sidebar.button("✅ Confirm Selection")

# --- Main Page Output ---
st.title("📄 View Prompt and Confirm Model")

# --- Handle Confirm Button Click ---
if confirm_button:
    # Scenario 1: A new file is uploaded (or it's the first upload)
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state["confirmed_prompt"] = file_content
            st.session_state["confirmed_model"] = selected_model
            st.session_state["last_uploaded_filename"] = uploaded_file.name
            st.sidebar.success(f"Prompt from '{uploaded_file.name}' and model '{selected_model}' confirmed!")
        except UnicodeDecodeError:
            st.sidebar.error(f"Error: Could not decode the file '{uploaded_file.name}'. Please ensure it is UTF-8 encoded.")
        except Exception as e:
            st.sidebar.error(f"An error occurred while reading the file: {e}")

    # Scenario 2: No new file is uploaded, BUT a prompt is already confirmed
    # This means the user might only want to update the model
    elif st.session_state.confirmed_prompt is not None:
        # Check if the selected model is different from the confirmed one
        if st.session_state.confirmed_model != selected_model:
            st.session_state["confirmed_model"] = selected_model
            st.sidebar.success(f"Model updated to '{selected_model}'. Prompt remains unchanged.")
        else:
            # Provide feedback if nothing changed
            st.sidebar.info("Selection confirmed. No changes detected.")

    # Scenario 3: No file uploaded and no prompt confirmed yet
    else:
        st.sidebar.warning("Please upload a prompt file before confirming.")

# --- Display confirmed info if available in session state ---
if st.session_state.confirmed_prompt is not None:
    # Display Confirmed Model (should always be available if prompt is confirmed)
    with st.container(border=True):
        st.subheader("✅ Confirmed Model")
        st.markdown("---")
        # Ensure we display the model stored in session state
        confirmed_model_display = st.session_state.get('confirmed_model', 'Not selected yet')
        st.info(f"The confirmed model is: `{confirmed_model_display}`")

    # Display Confirmed Prompt Content
    with st.container(border=True):
        st.subheader("📄 Confirmed Prompt File Content")
        if st.session_state.last_uploaded_filename:
            st.caption(f"From file: {st.session_state.last_uploaded_filename}")
        st.markdown("---")
        content = st.session_state.confirmed_prompt
        st.markdown(content)

# Show instruction if nothing is confirmed yet
else:
    st.warning("⚠️ Please upload a prompt file, select a model, and click 'Confirm Selection' in the sidebar.")

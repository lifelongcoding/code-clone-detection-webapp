import streamlit as st

st.set_page_config(page_title="Prompt Upload and Model Selection", layout="wide")

# ========================
# 🔧 Sidebar Input Section
# ========================
# Upload section
st.sidebar.header("📄 Upload Prompt File")
uploaded_file = st.sidebar.file_uploader("Select a text file", type=["txt", "md", "json"])

# Model selection section
st.sidebar.header("🤖 Select Model")
model_options = ["deepseek-v3-241226", "deepseek-r1-250120"]
selected_model = st.sidebar.selectbox("Choose a model", model_options)

confirm_button = st.sidebar.button("✅ Confirm")

# ========================
# 📤 Main Output Section
# ========================
if confirm_button:
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state["confirmed_prompt"] = file_content
        st.session_state["confirmed_model"] = selected_model
        st.sidebar.success("Content confirmed!")
    else:
        st.sidebar.warning("Please upload a prompt file before confirming.")

# Main page content display
st.title("📄 View Prompt and Confirm Model")

if "confirmed_prompt" in st.session_state and "confirmed_model" in st.session_state:
    model_info_container = st.container(border=True)

    model_info_container.subheader("✅ Selected Model")
    model_info_container.markdown("---")
    model_info_container.info(f"The selected model is: `{st.session_state['confirmed_model']}`")

    prompt_info_container = st.container(border=True)
    prompt_info_container.subheader("📄 Confirmed Prompt File Content")
    prompt_info_container.markdown("---")
    content = st.session_state.confirmed_prompt
    prompt_info_container.markdown(content)
else:
    st.warning("⚠️ Please upload a prompt file and confirm it from the sidebar.")


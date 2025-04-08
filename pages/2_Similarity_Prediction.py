import streamlit as st
from utils import get_predict

st.set_page_config(page_title="Code Similarity Prediction", layout="wide")

# 🚨 Ensure prompt and model are confirmed
if "confirmed_prompt" not in st.session_state or "confirmed_model" not in st.session_state:
    st.warning("⚠️ Please go to the home page to upload the prompt and confirm the model.")
    st.stop()

if "code_input_1" not in st.session_state:
    st.session_state.code_input_1 = ""

# ========================
# 🔧 Sidebar Input Section
# ========================
st.sidebar.header("📥 Input & Prediction")
st.sidebar.markdown("Please fill in the following information and click the button to predict.")

code1 = st.sidebar.text_area("✍️ Code Snippet 1", height=150, key="code_input_1")
code2 = st.sidebar.text_area("✍️ Code Snippet 2", height=150, key="code_input_2")

predict_button = st.sidebar.button("🚀 Predict Now")

# Model and prompt information
model = st.session_state["confirmed_model"]
prompt = st.session_state["confirmed_prompt"]
base_url = st.secrets["BASE_URL"]
api_key = st.secrets["API_KEY"]

# ========================
# 📤 Main Output Section
# ========================
st.title("🧠 Code Similarity Prediction")

if predict_button:
    if not code1.strip() or not code2.strip():
        st.warning("⚠️ Please enter both code snippets before predicting.")
    else:
        st.info(f"Predicting using model `{model}`...")

        try:
            with st.spinner("Thinking..."):
                result = get_predict(code1, code2, api_key, base_url, model, prompt)

            st.success("✅ Prediction complete!")
            st.subheader("🧾 Prediction Result")
            st.markdown(f"**Conclusion:**\n\n> {result['prediction']}")

            if result["cot"]:
                st.markdown("---")
                st.markdown("**🧩 Reasoning Process:**")
                st.markdown(result["cot"])

            st.markdown("---")
            st.subheader("📄 Your Input Code Snippets")
            st.code(code1, language="java")
            st.code(code2, language="java")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

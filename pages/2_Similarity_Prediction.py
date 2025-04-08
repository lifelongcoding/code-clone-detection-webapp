import streamlit as st
from utils import get_predict
from datetime import datetime  # Used to add timestamp (optional)

st.set_page_config(page_title="Code Similarity Prediction", layout="wide")

# --- Initialize Session State ---
# Check if the required configuration has been set
if "confirmed_prompt" not in st.session_state or "confirmed_model" not in st.session_state:
    st.warning("⚠️ Please go to the home page to upload the prompt and confirm the model.")
    st.stop()

# Initialize session state for code input (if not exists)
if "code_input_1" not in st.session_state:
    st.session_state.code_input_1 = ""
if "code_input_2" not in st.session_state:
    st.session_state.code_input_2 = ""
# Initialize prediction history list (if not exists)
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []  # Use a list to store history

# --- Sidebar Input ---
st.sidebar.header("📥 Input & Prediction")
st.sidebar.markdown("Please fill in the following information and click the button to predict.")

# Use the value in session state as the default for text_area
code1_input = st.sidebar.text_area("✍️ Code Snippet 1", value=st.session_state.code_input_1, height=150, key="code_input_widget_1")
code2_input = st.sidebar.text_area("✍️ Code Snippet 2", value=st.session_state.code_input_2, height=150, key="code_input_widget_2")

# Update code in session state to retain text input across page switches
st.session_state.code_input_1 = code1_input
st.session_state.code_input_2 = code2_input

predict_button = st.sidebar.button("🚀 Predict Now")

# Get config info
model = st.session_state["confirmed_model"]
prompt = st.session_state["confirmed_prompt"]
base_url = st.secrets["BASE_URL"]
api_key = st.secrets["API_KEY"]

# --- Main Page Output ---
st.title("🧠 Code Similarity Prediction")

# --- Handle Prediction Button Click ---
if predict_button:
    # Use latest input code from session state
    code1 = st.session_state.code_input_1
    code2 = st.session_state.code_input_2

    if not code1.strip() or not code2.strip():
        st.warning("⚠️ Please enter both code snippets before predicting.")
    else:
        st.info(f"Predicting using model `{model}`...")
        try:
            with st.spinner("Thinking..."):
                result = get_predict(code1, code2, api_key, base_url, model, prompt)

            st.success("✅ Prediction complete! Result added to history.")

            # Create a history record
            history_entry = {
                "code1": code1,
                "code2": code2,
                "prediction": result.get("prediction", "N/A"),  # Use get to prevent KeyError
                "cot": result.get("cot"),  # Use get to prevent KeyError
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Add the new result to the *beginning* of the history list (latest first)
            st.session_state.prediction_history.insert(0, history_entry)
        except Exception as e:
            st.error(f"❌ An error occurred during prediction: {e}")

# --- Display the Latest Prediction Result ---
if st.session_state.prediction_history:
    # Get the latest prediction record
    latest_result = st.session_state.prediction_history[0]

    st.subheader("📜 Latest Prediction Result")
    st.markdown(f"**Conclusion:**\n\n> {latest_result['prediction']}")

    if latest_result["cot"]:
        st.markdown("---")
        st.markdown("**🧩 Reasoning Process:**")
        st.markdown(latest_result["cot"])

    st.markdown("---")
    st.subheader("📄 Input Code Snippets for Latest Prediction")
    st.code(latest_result['code1'], language="java")
    st.code(latest_result['code2'], language="java")
    st.caption(f"Predicted at: {latest_result['timestamp']}")
    st.markdown("---")
else:
    # If no history, show a message
    st.info("📊 No predictions made yet in this session. Use the sidebar to input code and predict.")

# --- Display Full History ---
if len(st.session_state.prediction_history) > 1:  # If there's more than one record
    with st.expander("📜 View Full Prediction History (Newest First)"):
        for i, entry in enumerate(st.session_state.prediction_history):
            with st.container(border=True):
                st.markdown(f"**Prediction #{len(st.session_state.prediction_history) - i}** (Timestamp: {entry['timestamp']})")
                st.markdown(f"**Conclusion:** {entry.get('prediction', 'N/A')}")
                if entry.get('cot'):
                    st.markdown(f"**Reasoning:** {entry.get('cot')}")
                st.code(entry.get('code1',''), language="java")
                st.code(entry.get('code2',''), language="java")
            st.divider()

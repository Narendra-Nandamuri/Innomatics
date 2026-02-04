import streamlit as st
import joblib

# Load the trained model
@st.cache_resource
def load_model():
    model = joblib.load('sentiment_model.pkl')
    return model

model = load_model()

st.title("Badminton Product Sentiment Analyzer")
st.markdown("Enter a product review below to check if it's **Positive** or **Negative**.")

# Text Input
user_input = st.text_area("Review Text:", height=150, placeholder="Example: The quality is not good, very disappointed.")

if st.button("Analyze Sentiment"):
    if model is None:
        st.error("Model file 'sentiment_model.pkl' not found. Please run 'train_model.py' first.")
    elif user_input.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        # Predict
        prediction = model.predict([user_input])[0]
        probability = model.predict_proba([user_input])[0]
        
        # Display Results
        if prediction == 1:
            confidence = probability[1] * 100
            st.success(f"**Positive Review** (Confidence: {confidence:.2f}%)")
            st.balloons()
        else:
            confidence = probability[0] * 100
            st.error(f"**Negative Review** (Confidence: {confidence:.2f}%)")
            st.markdown("### Potential Issues:")
            st.write("This review likely contains complaints about quality, damage, or authenticity.")

# Sidebar
st.sidebar.header("About Project")
st.sidebar.info("This model detects sentiment in Flipkart reviews, specifically trained to handle negations (e.g., 'not good').")
import streamlit as st
import json
from pipeline import process_email

st.set_page_config(page_title="Mumzworld AI Triage", page_icon="👶")

st.title("🤖 Mumzworld AI Customer Support Triage")
st.markdown("AI-powered email classification for multilingual customer support")

# Input section
st.header("📧 Customer Email Input")
email_input = st.text_area(
    "Paste the customer email here:",
    height=150,
    placeholder="Enter customer email text here..."
)

if st.button("🔍 Analyze Email", type="primary"):
    if email_input.strip():
        with st.spinner("Analyzing email..."):
            try:
                result = process_email(email_input)

                # Display results
                st.success("✅ Analysis Complete!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Intent", result.intent.upper())
                    st.metric("Urgency", result.urgency.upper())
                    st.metric("Confidence", f"{result.confidence_score:.0%}")

                with col2:
                    st.subheader("📝 Reasoning")
                    st.write(result.reasoning)

                st.header("💬 Suggested Replies")

                tab1, tab2 = st.tabs(["🇺🇸 English", "🇸🇦 Arabic"])

                with tab1:
                    st.subheader("English Reply")
                    st.write(result.suggested_reply_english)

                with tab2:
                    st.subheader("Arabic Reply")
                    st.write(result.suggested_reply_arabic)

                # Raw JSON output
                with st.expander("🔧 Raw JSON Output"):
                    st.code(json.dumps(result.model_dump(), indent=2, ensure_ascii=False), language="json")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter an email text to analyze.")

# Footer
st.markdown("---")
st.markdown("*Built with OpenRouter API & GPT-3.5-turbo*")
st.markdown("*Supports English and Arabic customer communications*")
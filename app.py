import streamlit as st
from email_generator import generate_email,generate_email_with_hf
from hf_pipelines import sentiment_hf
from utlis import detect_language, named_entity_recognition


def main():
    st.title("📧 Smart Email Assistant")
    st.markdown("Generate professional replies, subject lines, summaries, and insights from email threads.")

    # Store user API key
    if 'OPENAI_API_KEY' not in st.session_state:
        st.session_state.OPENAI_API_KEY = None

    # Sidebar
    with st.sidebar:
        st.subheader("🔧 Settings")
        key_input = st.text_input("OpenAI API Key (optional)", type="password")
        if key_input:
            st.session_state.OPENAI_API_KEY = key_input
            st.success("API key set successfully!")
        st.markdown("---")
        st.markdown("**Features**")
        st.markdown("- OpenAI + Hugging Face fallback\n- Auto tone detection\n- NER insights\n- Download responses")

    # Email input
    st.subheader("📝 Email Thread Input")
    email_thread = st.text_area("Paste the email thread here:", height=200)
    additional_context = st.text_area("Additional context (optional):", height=100)

    # Language & Tone Detection
    if email_thread:
        lang = detect_language(email_thread)
        if lang != 'en':
            st.warning(f"Detected language: {lang.upper()}. Responses will still be generated in English.")
        tone_detected = sentiment_hf(email_thread)[0]
        st.info(f"Detected sentiment: {tone_detected['label']} (Confidence: {tone_detected['score']:.2f})")

    selected_tone = st.selectbox("✒️ Select tone", ["Professional", "Casual", "Friendly", "Formal"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Response"):
            if not email_thread:
                st.error("Enter an email thread.")
            else:
                prompt = f"Email Thread:\n{email_thread}\n\nContext:\n{additional_context}"  
                st.session_state.last_prompt = prompt
                st.session_state.last_tone = selected_tone
                with st.spinner("Generating..."):
                    if st.session_state.OPENAI_API_KEY:
                        result = generate_email(st.session_state.OPENAI_API_KEY, prompt, selected_tone)
                    else:
                        st.warning("No OpenAI key; using Hugging Face models.")
                        result = generate_email_with_hf(prompt)
                    if result["error"]:
                        st.error(result["error"])
                    else:
                        st.session_state.generated = result  # Save the result to `generated`
                        st.success("Generated successfully!")

    with col2:
        if st.button("Regenerate Last Response"):
            if st.session_state.last_prompt:
                with st.spinner("Regenerating..."):
                    if st.session_state.OPENAI_API_KEY:
                        result = generate_email(st.session_state.OPENAI_API_KEY, st.session_state.last_prompt, st.session_state.last_tone)
                    else:
                        result = (st.session_state.last_prompt)
                    if result["error"]:
                        st.error(result["error"])
                    else:
                        st.session_state.generated = result  # Save the regenerated result
                        st.success("Regenerated successfully!")

    # Display the generated output if it exists
    if 'generated' in st.session_state:
        output = st.session_state.generated

        st.markdown("---")
        st.subheader("📬 Generated Email")

        st.markdown("**Subject Line**")
        st.code(output['subject'], language=None)

        st.markdown("**Response**")
        st.code(output['response'], language=None)

        st.markdown("**Summary**")
        st.code(output['summary'], language=None)

        # NER
        with st.expander("🔍 NER on Input"):
            st.dataframe(named_entity_recognition(email_thread))
        with st.expander("🔍 NER on Response"):
            st.dataframe(named_entity_recognition(output['response']))

        # Downloads
        st.download_button("Download Reply", output['response'], file_name="email_reply.txt")
        st.download_button("Download Summary", output['summary'], file_name="email_summary.txt")

if __name__ == "__main__":
    main()


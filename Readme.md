# 📧 **Smart Email Assistant**

An interactive **Streamlit** app that automatically summarizes email threads, generates professional replies, drafts concise subject lines, and extracts insights—all powered by **OpenAI** (with **Hugging Face** fallback), tone detection, and Named Entity Recognition (NER). ✨

---

## 🚀 **Features**

- **📝 Email Summarization**: Condense long email threads into 2–3 sentence summaries
- **💬 Reply Generation**: Auto-generate professional replies in various tones (Professional, Casual, Friendly, Formal)
- **✉️ Subject Line Drafting**: Create concise, context-appropriate subject lines
- **⚡ OpenAI + HF Fallback**: Uses **OpenAI GPT-4/3.5** when API key is provided, otherwise falls back to **Hugging Face** models
- **🎯 Tone Detection**: Auto-detect the input thread’s sentiment and suggest tone
- **🔍 Named Entity Recognition (NER)**: Highlight people, organizations, dates, etc. in both the input and the generated reply
- **📥 Downloadable Outputs**: Download reply and summary as `.txt` files
- **🔄 “Regenerate” Button**: Quickly re-run the last prompt with the same settings

---


## ⚙️ **Tech Stack**

- **💻 Backend**: Python, [OpenAI Python SDK](https://github.com/openai/openai-python)
- **🔄 Fallback NLP**: [Hugging Face Transformers](https://github.com/huggingface/transformers)
- **🌍 Language Detection**: [`langdetect`](https://pypi.org/project/langdetect/)
- **🧠 NER**: Hugging Face “ner” pipeline or **spaCy** models
- **🌐 UI**: [Streamlit](https://streamlit.io/)
- **🐋 Containerization**: Docker


## 📋 **Usage**

1. **Run locally with Streamlit**

   streamlit run app.py
3. **Open the app**

   Navigate to [http://localhost:8501](http://localhost:8501) in your browser.
4. **Interact with the UI**

   * Paste an email thread
   * (Optional) Enter extra context
   * Select your desired tone
   * Click **Generate Response**
   * View & download the generated subject, reply, and summary

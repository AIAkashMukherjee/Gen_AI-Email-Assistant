from openai import OpenAI
from transformers import pipeline
from hf_pipelines import summarizer_hf,generator_hf

def generate_email(api_key,prompt,tone,model='gpt-4'):
    if not api_key:
        return {"error": "Please enter your OpenAI API key.", "response": None}
    try:
        llm=OpenAI(api_key=api_key)

        # email response
        messages=[
            {"role": "system", "content": f"You are a professional email assistant. Generate a {tone} tone response."},
            {"role": "user", "content": prompt}
        ]

        response=llm.chat.completions.create(model=model,messages=messages,temperature=.8)
        email_response=response.choices[0].message.content

        # Subject line
        subj_msgs = [
            {"role": "system", "content": "Generate a concise subject line for this email."},
            {"role": "user", "content": email_response}
        ]
        subject=llm.chat.completions.create(model=model, messages=subj_msgs, temperature=0.7)
        subject_response=subject.choices[0].message.content

        # thread summrary
        sum_msgs = [
            {"role": "system", "content": "Provide a concise summary of the email thread."},
            {"role": "user", "content": f"Thread:\n{prompt}\n\nResponse:\n{email_response}"}
        ]
        summary=llm.chat.completions.create(model=model, messages=sum_msgs, temperature=0.7)
        thread_summary = summary.choices[0].message.content

        return {"error": None, "response": email_response, "subject": subject_response, "summary": thread_summary}

    except Exception as e:
        return {
            "error": str(e),
            "response": None
        }


def generate_email_with_hf(prompt):
    try:
        thread_summary = summarizer_hf(prompt, max_length=80, min_length=30, do_sample=False)[0]["summary_text"]
        reply_output = generator_hf(f"Reply to the email: {prompt}", max_length=256, do_sample=True)[0]["generated_text"]
        subject_line = generator_hf(f"Generate a short subject line for: {reply_output}", max_length=20)[0]["generated_text"]
        return {"error": None, "response": reply_output, "subject": subject_line, "summary": thread_summary}
    except Exception as e:
        return {"error": str(e), "response": None}
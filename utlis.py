from langdetect import detect
import spacy
import subprocess
import importlib.util

def ensure_spacy_model(model_name="en_core_web_sm"):
    if importlib.util.find_spec(model_name) is None:
        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)

ensure_spacy_model()


# Load SpaCy's small English model
nlp = spacy.load("en_core_web_sm")

def detect_language(text):
    """Detect the language of the input text"""
    try:
        return detect(text)
    except:
        return 'en'

def named_entity_recognition(text):
    """Extract named entities from the text using SpaCy"""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities
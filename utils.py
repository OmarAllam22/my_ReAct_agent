import os, yaml
from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_gemini(api_config_path):
    with open(api_config_path, 'r') as f:
        data = yaml.safe_load(f)
    
    os.environ["GOOGLE_API_KEY"] = data.get("GOOGLE_API_KEY",None) 
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    return model
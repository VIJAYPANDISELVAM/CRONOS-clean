from google import genai
genai.Client(...)
models = gemini_client.models.list()
for m in models:
    print(m.name, m.supported_generation_methods)

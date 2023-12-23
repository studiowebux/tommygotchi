import requests
import json

class Brain:
    def __init__(self, 
                 url="http://localhost:3000/api/chat", 
                 brain_path="./brain.json", 
                 prompt="You are a helpful and friendly AI assistant. Respond very concisely.",
                 model="./models/llama-2-7b-chat.bin",
                 model_name="Llama 2 7B",
                 temperature=1,
                 max_length=12000,
                 token_limit=4000):
        self.URL = url
        
        try:
            f = open(brain_path, "r")
            self.context=json.loads(f.read())
            f.close()
        except:
            print("Failed to load existing brain... will start a new one.")
            self.context = {
                'model': {
                    'id': model,
                    'name': model_name,
                    'maxLength': max_length,
                    'tokenLimit': token_limit
                },
                'messages': [],
                'key': "",
                'prompt': prompt,
                'temperature': temperature
            }

    def updateContext(self, answer):
        self.context["messages"].append({'role': "assistant", 'content': answer})
        f = open("brain.json", "w")
        f.write(json.dumps(self.context, indent=4))
        f.close()
    
    def post(self, prompt):
        self.context["messages"].append({'role': "user", 'content': prompt})
        r = requests.post(url=self.URL, json=self.context)
        response = r.text
        print("Response from LlamaGPT: %s" % response)
        return response
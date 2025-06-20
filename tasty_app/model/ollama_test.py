import ollama


response = ollama.chat(model='deepseek-coder', messages=[{'role': 'user', 'content': 'Hello!'}])
print(response['message'])
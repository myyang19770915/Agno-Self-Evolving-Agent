import requests

try:
    url = 'http://localhost:7777/agents/self-evolving-agent-gpt-5-mini/runs'
    files = {
        'message': (None, 'hello 1+1='),
        'stream': (None, 'true'),
        'session_id': (None, 'ba825121-654d-4876-8051-5facbb70cae4')
    }
    with requests.post(url, files=files, stream=True) as r:
        with open('debug_stream.txt', 'w', encoding='utf-8') as f:
            for line in r.iter_lines():
                if line:
                    f.write(line.decode('utf-8') + '\n')
except Exception as e:
    print("Error:", e)

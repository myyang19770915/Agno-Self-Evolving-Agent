import requests
import json

try:
    with open('debug_output2.txt', 'w', encoding='utf-8') as f:
        res = requests.get('http://localhost:7777/sessions')
        sessions = res.json()
        if isinstance(sessions, dict) and 'data' in sessions:
            sessions = sessions['data']
        
        if sessions:
            for s in sessions[:2]:
                sid = s['session_id']
                res2 = requests.get(f'http://localhost:7777/sessions/{sid}')
                session_data = res2.json()
                chat_hist = session_data.get('chat_history', [])
                for i, msg in enumerate(chat_hist):
                    role = msg.get('role', 'N/A')
                    content = msg.get('content')
                    f.write(f"  {i:02d} [{role}] content type: {type(content)} \n")
                    f.write(f"   value: {repr(content)[:100]}\n")
                    if 'tool_calls' in msg:
                        f.write(f"   has tool_calls: {len(msg['tool_calls'])} calls\n")
                f.write("-" * 40 + "\n")
except Exception as e:
    print('Error:', e)

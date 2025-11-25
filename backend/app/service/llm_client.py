import requests

API_KEY = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImUzNDRlZjExLTQ0NzItNDFjMS1iOTA5LWQyMjlkMzZkN2Q0MCIsImV4cCI6NDkxNzM2MTUyOH0.a31bOPKDAjLEGmqCJtCEqOq8m4sEo35vrP7bVAN23pnzSi0UF8_jiS4AYfAT5lh9YrGflqvRMmVr27AwH-Yr1w"
AI_MODEL = "mistralai/Mistral-Nemo-Instruct-2407"

def ask_llm(message_text: str) -> str:
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "Ты универсальный агент"},
            {"role": "user", "content": message_text},
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]

    return "Ошибка: LLM не вернул корректного ответа"


import openai
import json
import numpy as np

amostra = {
    "Colesterol": {"valor": np.random.uniform(110, 260)},
    "Glicose": {"valor": np.random.uniform(80, 220)},
    "T3": {"valor": np.random.uniform(0.2, 4.5)},
    "T4": {"valor": np.random.uniform(3.0, 18.0)},
    "TSH": {"valor": np.random.uniform(0.3, 14.0)},
    "Triglicerídeos": {"valor": np.random.uniform(80, 700)},
}
# print(json.dumps(amostra, indent=4, ensure_ascii=False))

# Conexão no lm studio
client = openai.OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# setup das menssagens para o modelo
messages = [
    {"role": "system", "content": "Você é um nutricionista. Faça uma rotina de dieta com os dados referente de amostras de sangue."},
    {"role": "user", "content":  json.dumps(amostra, indent=4, ensure_ascii=False)}
]

#Setup do formato da saida
character_schema = {
    "type": "json_schema",
    "name": "diet",
    "schema": {
    "type": "object",
        "properties": {
            "days": {
            "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "time": { "type": "string" },
                        "food": { "type": "string" }
                    },
                    "required": ["time", "food"],
                }
            }
        },
        "required": ["days"],
    }
}

# Resposta do LM
response = client.chat.completions.create(
    model="meta-llama-3.1-8b-instruct",
    messages=messages,
    temperature=0.7,
    max_tokens=10000,
    response_format= {
    "type" : "json_schema",
    "json_schema": {
        "type": "json_schema",
        "name": "diet",
        "schema": {
            "type": "object",
            "properties": {
            "diet": {
            "type": "array",
            "items": {
            "type": "object",
            "properties": {
            "day": { "type": "string" },
            "routine": { "type": "array", "items": {"type":"object","properties":{"time": { "type": "string" },
            "food": { "type": "string" }}} }
            },
            "required": ["time", "food"],
            }
            }
            },
            "required": ["days"],
        }
    }
    }
        
)
print(response.choices[0].message.content)

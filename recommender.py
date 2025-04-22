
import openai
import json
import numpy as np

client = openai.OpenAI(base_url="http://192.168.143.122:1234/v1", api_key="not-needed")
amostra = {
    "Colesterol": {"valor": np.random.uniform(110, 260)},
    "Glicose": {"valor": np.random.uniform(80, 220)},
    "T3": {"valor": np.random.uniform(0.2, 4.5)},
    "T4": {"valor": np.random.uniform(3.0, 18.0)},
    "TSH": {"valor": np.random.uniform(0.3, 14.0)},
    "Triglicerídeos": {"valor": np.random.uniform(80, 700)},
}
diet = client.responses.create(
    model="local-model",
    input=[
        {"role": "system", "content": "You are a helpful nutricionist. With the follow blood sample make a diet schedule."},
        {"role": "user", "content":  json.dumps(amostra, indent=4, ensure_ascii=False)}
    ],
    text={
        "format": {
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
                            "additionalProperties": False
						}
					},
					"final_answer": { "type": "string" }
				},
                "required": ["days"],
				 "additionalProperties": False
			},
			"strict": True
		}
	}
)
event = json.loads(diet.output_text)

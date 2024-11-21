import openai

class APIOpenAI:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.system_prompt = config["system_prompt"]
        self.json_schema = config["json_schema"]
        self.parameters = config["parameters"]

    def analyze_text(self, user_input):
        response = openai.ChatCompletion.create(
            model=self.parameters["model"],
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            functions=[self.json_schema],
            function_call={"name": "sleutelfiguren_schema"}
        )
        return response.choices[0].message["function_call"]["arguments"]
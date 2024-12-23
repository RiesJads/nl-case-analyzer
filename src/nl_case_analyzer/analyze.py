import time
from openai import OpenAI


class AnalyzeGPT:
    def __init__(self, config):
        self.client = config["client"]

        self.api_key = config["api_key"]
        self.system_prompt = config["system_prompt"]
        self.json_schema = config["json_schema"]
        self.parameters = config["parameters"]

    def analyze_text(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model=self.parameters["model"],
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=self.parameters["temperature"],
                max_tokens=self.parameters["max_tokens"],
                top_p = self.parameters["top_p"],
                frequency_penalty = self.parameters["frequency_penalty"],
                presence_penalty = self.parameters["presence_penalty"],

                
                response_format={
                    "type": "json_schema",
                    "json_schema": self.json_schema
                }
            )


            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return None
    
    def analyze_snippets(self, snippets, timeout=5):
        """
        Analyze a list of text snippets and return the results.

        Args:
            snippets (list): List of text snippets to process.

        Returns:
            list: List of responses from the OpenAI API.
        """
        results = []
        for i, snippet in enumerate(snippets):
            print(f"Processing snippet {i + 1}/{len(snippets)}...")
            result = self.analyze_text(snippet)
            if result:
                print(f"Snippet {i + 1} processed successfully.")
                results.append(result)
            else:
                print(f"Snippet {i + 1} failed to process.")
            
            time.sleep(timeout)
        return results
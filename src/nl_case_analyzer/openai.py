# Class to configure API + Response JSON SCHEMA

import os
import openai


class ConfigGPT:

    """
    Class includes:
        - user prompt
        - system prompt
        - required response format
        - parameter settings for gpt
    """
    def __init__(self):
        # init api key
        self.api_key = os.getenv("OPENAI_API")
        if not self.api_key:
            raise ValueError("API key is not set in the environment variable 'OPENAI_API'.")
        openai.api_key = self.api_key

        ## system prompt
        self.system_prompt = """
        Je bent een taalmodel dat gespecialiseerd is in het analyseren van samenvattingen van gerechtelijke uitspraken. Je taak is om de tekstfragmenten te analyseren en de correcte sleutelfiguren te identificeren. Deze sleutelfiguren zijn:

        - **Sleutelfiguur 1**: 'rechter', 'het hof' of 'de rechtbank'
        - **Sleutelfiguur 2**: 'officier van justitie' of 'advocaat-generaal'
        - **Sleutelfiguur 3**: 'verdediging'

        Voor elke sleutelfiguur moet je:

        1. De zin(nen) uit het fragment extraheren die het standpunt van de sleutelfiguur over het gebruikte bewijsmateriaal weergeven. **Als er bewijsmateriaal gebaseerd op gedecrypteerde chatberichten (crypto-data) aanwezig is, focus dan in het bijzonder op dit type bewijs.**

        2. **Geef een korte uitleg (reden) van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs. Deze uitleg moet specifiek zijn en gebaseerd op informatie uit de tekst.**

        3. Vijf specifieke tags creëren die de redenen weergeven waarom de sleutelfiguur zo denkt over het crypto-data bewijs. Deze tags moeten direct gerelateerd zijn aan de argumenten of overwegingen van de sleutelfiguur.

        4. Een label creëren dat de kern van de redenen achter het standpunt van de sleutelfiguur over het crypto-data bewijs samenvat.

        Je moet altijd output produceren die strikt voldoet aan het volgende JSON-schema:

        [Voeg het bijgewerkte JSON-schema hier in]

        **Belangrijk:**

        - **Als een sleutelfiguur niet voorkomt in de tekst, stel dan de waarde in op `null`.**
        - **Zorg ervoor dat alle output strikt voldoet aan het JSON-schema.**
        - **Gebruik specifieke en relevante informatie uit de tekst voor alle velden, met nadruk op de redenen achter het standpunt over het crypto-data bewijs.**
        - **Vermijd algemene of vage termen; wees zo specifiek mogelijk.**
        """

        # JSON SCHEMA
        self.json_schema  = {
        "name": "sleutelfiguren_schema",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
            "sleutelfiguur_1": {
                "type": [
                "object",
                "null"
                ],
                "properties": {
                "rol": {
                    "type": "string",
                    "enum": [
                    "rechter",
                    "het hof",
                    "de rechtbank"
                    ],
                    "description": "De rol van sleutelfiguur 1."
                },
                "zin": {
                    "type": "string",
                    "description": "De zin die het standpunt van sleutelfiguur 1 over het bewijsmateriaal weergeeft."
                },
                "crypto_relevant": {
                    "type": "boolean",
                    "description": "Geeft aan of de zin gerelateerd is aan crypto-data (waar of niet waar)."
                },
                "reden": {
                    "type": "string",
                    "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
                },
                "tags": {
                    "type": "array",
                    "description": "Een lijst met 5 specifieke tags die de redenen weergeven waarom de sleutelfiguur zo denkt over het crypto-data bewijs.",
                    "items": {
                    "type": "string"
                    }
                },
                "label": {
                    "type": "string",
                    "description": "Een label dat de kern van de redenen achter het standpunt van de sleutelfiguur over het crypto-data bewijs samenvat."
                }
                },
                "required": [
                "rol",
                "zin",
                "crypto_relevant",
                "reden",
                "tags",
                "label"
                ],
                "additionalProperties": False
            },
            "sleutelfiguur_2": {
                "type": [
                "object",
                "null"
                ],
                "properties": {
                "rol": {
                    "type": "string",
                    "enum": [
                    "officier van justitie",
                    "advocaat-generaal"
                    ],
                    "description": "De rol van sleutelfiguur 2."
                },
                "zin": {
                    "type": "string",
                    "description": "De zin die het standpunt van sleutelfiguur 2 over het bewijsmateriaal weergeeft."
                },
                "crypto_relevant": {
                    "type": "boolean",
                    "description": "Geeft aan of de zin gerelateerd is aan crypto-data (waar of niet waar)."
                },
                "reden": {
                    "type": "string",
                    "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
                },
                "tags": {
                    "type": "array",
                    "description": "Een lijst met 5 specifieke tags die de redenen weergeven waarom de sleutelfiguur zo denkt over het crypto-data bewijs.",
                    "items": {
                    "type": "string"
                    }
                },
                "label": {
                    "type": "string",
                    "description": "Een label dat de kern van de redenen achter het standpunt van de sleutelfiguur over het crypto-data bewijs samenvat."
                }
                },
                "required": [
                "rol",
                "zin",
                "crypto_relevant",
                "reden",
                "tags",
                "label"
                ],
                "additionalProperties": False
            },
            "sleutelfiguur_3": {
                "type": [
                "object",
                "null"
                ],
                "properties": {
                "rol": {
                    "type": "string",
                    "enum": [
                    "verdediging"
                    ],
                    "description": "De rol van sleutelfiguur 3."
                },
                "zin": {
                    "type": "string",
                    "description": "De zin die het standpunt van sleutelfiguur 3 over het bewijsmateriaal weergeeft."
                },
                "crypto_relevant": {
                    "type": "boolean",
                    "description": "Geeft aan of de zin gerelateerd is aan crypto-data (waar of niet waar)."
                },
                "reden": {
                    "type": "string",
                    "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
                },
                "tags": {
                    "type": "array",
                    "description": "Een lijst met 5 specifieke tags die de redenen weergeven waarom de sleutelfiguur zo denkt over het crypto-data bewijs.",
                    "items": {
                    "type": "string"
                    }
                },
                "label": {
                    "type": "string",
                    "description": "Een label dat de kern van de redenen achter het standpunt van de sleutelfiguur over het crypto-data bewijs samenvat."
                }
                },
                "required": [
                "rol",
                "zin",
                "crypto_relevant",
                "reden",
                "tags",
                "label"
                ],
                "additionalProperties": False
            }
            },
            "required": [
            "sleutelfiguur_1",
            "sleutelfiguur_2",
            "sleutelfiguur_3"
            ],
            "additionalProperties": False
        }
        }
        self.parameters = {
            "model": "gpt-4o",
            "temperature": 0.2,
            "max_tokens": 3000
        }
    def get_configuration(self):
        """
        Fetches the configuration for the API.
        Returns:
            dict: A dictionary containing system prompt, parameters, and JSON schema.
        """
        return {
            "api_key": self.api_key,
            "system_prompt": self.system_prompt,
            "json_schema": self.json_schema,
            "parameters": self.parameters
        }

        
    
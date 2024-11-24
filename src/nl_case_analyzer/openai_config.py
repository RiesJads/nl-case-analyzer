# Class to configure API + Response JSON SCHEMA

import os
from openai import OpenAI

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
        

        self.client = OpenAI(api_key=self.api_key)
        ## system prompt
        self.system_prompt = """
Je bent een taalmodel dat gespecialiseerd is in het analyseren van samenvattingen van gerechtelijke uitspraken. Je taak is om de tekstfragmenten te analyseren en de correcte sleutelfiguren te identificeren. Deze sleutelfiguren zijn:

- **Sleutelfiguur 1**: 'rechter', 'het hof', 'de rechtbank', of andere termen die verwijzen naar de rechtsprekende instantie, zoals 'magistraat', 'voorzitter', 'rechtsprekende instantie'.
- **Sleutelfiguur 2**: 'officier van justitie', 'advocaat-generaal', of andere termen die verwijzen naar de aanklager, zoals 'aanklager', 'het Openbaar Ministerie', 'OM'.
- **Sleutelfiguur 3**: 'verdediging', of andere termen die verwijzen naar de advocaat van de verdachte, zoals 'raadsman', 'raadsvrouw', 'advocaat van de verdachte'.

**Voorbeelden van hoe sleutelfiguren kunnen worden genoemd:**

- **Sleutelfiguur 1 (rechter):**
  - "De rechtbank oordeelt dat..."
  - "Volgens het hof is..."
  - "De magistraat stelde vast dat..."

- **Sleutelfiguur 2 (aanklager):**
  - "De officier van justitie betoogt dat..."
  - "Het Openbaar Ministerie stelt dat..."
  - "De aanklager is van mening dat..."

- **Sleutelfiguur 3 (verdediging):**
  - "De verdediging voert aan dat..."
  - "Volgens de raadsman van de verdachte..."
  - "De advocaat stelt dat..."

Voor elke sleutelfiguur moet je:

1. **Identificeren en Extraheren van Zinnen:**
   - Zoek de zin(nen) uit het fragment die het standpunt van de sleutelfiguur over het **bewijsmateriaal gerelateerd aan berichten van versleutelde communicatiesystemen** weergeven.
   - Let op zowel expliciete termen als contextuele aanwijzingen die kunnen duiden op een sleutelfiguur.

2. **Controleer op Crypto-Relevantie:**
   - Bepaal of het standpunt betrekking heeft op bewijsmateriaal afkomstig van versleutelde communicatie (crypto-data).
   - Stel het veld `crypto_relevant` in op `true` als dat zo is, anders op `false`.

3. **Creëer Vijf Specifieke Tags:**
   - Maak een lijst van 5 specifieke tags die weergeven hoe en waarom de sleutelfiguur denkt over het crypto-data bewijsmateriaal.
   - Deze tags moeten direct gerelateerd zijn aan de argumenten of overwegingen van de sleutelfiguur.

4. **Labels Evalueren:**
   - Beoordeel voor elk van de drie labels **'betrouwbaarheid'**, **'rechtmatigheid'**, **'overtuigend'** of deze van toepassing zijn op basis van de rationale van de sleutelfiguur.
   - Gebruik de opties **'ja'**, **'nee'**, of **'NVT'** (Niet Van Toepassing).
     - **'ja'**: Het label is van toepassing; de sleutelfiguur vindt dat het bewijs aan dit criterium voldoet.
     - **'nee'**: Het label is niet van toepassing; de sleutelfiguur vindt dat het bewijs niet aan dit criterium voldoet.
     - **'NVT'**: Er is onvoldoende informatie om te bepalen of het label van toepassing is.

**Definities van de labels:**

- **Betrouwbaarheid**: De mate waarin erop vertrouwd kan worden dat het bewijs feitelijk waar en relevant is.
- **Rechtmatigheid**: Of het bewijs is verkregen op een wijze die in lijn is met het recht.
- **Overtuigend**: Of het bewijs voldoende overtuigend is; de sleutelfiguur is persoonlijk overtuigd dat de verdachte inderdaad datgene heeft gedaan waarvan hij of zij beschuldigd wordt.

Je moet altijd output produceren die strikt voldoet aan het volgende JSON-schema:

{self.json_schema}

**Belangrijk:**

- **Identificatie van Sleutelfiguren:**
  - Zoek niet alleen naar de expliciete termen, maar let ook op synoniemen, titels en contextuele aanwijzingen die kunnen duiden op een sleutelfiguur.
  - Als je een rol tegenkomt die waarschijnlijk een sleutelfiguur is, neem deze dan op, zelfs als de term niet expliciet in de lijst staat.

- **Als een sleutelfiguur niet voorkomt in de tekst, of geen standpunt heeft over het bewijsmateriaal, stel dan de waarde in op `null`.**

- **Zorg ervoor dat alle output strikt voldoet aan het JSON-schema.**

- **Gebruik specifieke en relevante informatie uit de tekst voor alle velden.**

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
              "de rechtbank",
              "magistraat",
              "voorzitter",
              "rechtsprekende instantie"
            ],
            "description": "De rol van sleutelfiguur 1."
          },
          "zin": {
            "type": "string",
            "description": "De zin(nen) die het standpunt van sleutelfiguur 1 over het bewijsmateriaal weergeven."
          },
          "crypto_relevant": {
            "type": "boolean",
            "description": "Geeft aan of het standpunt betrekking heeft op crypto-data (waar of niet waar)."
          },
          "reden": {
            "type": "string",
            "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
          },
          "tags": {
            "type": "array",
            "description": "Een lijst met 5 specifieke tags die weergeven hoe en waarom de sleutelfiguur denkt over het crypto-data bewijsmateriaal.",
            "items": {
              "type": "string"
            }
          },
          "labels": {
            "type": "object",
            "description": "Een object met de drie labels 'betrouwbaarheid', 'rechtmatigheid', 'overtuigend', gebaseerd op de rationale.",
            "properties": {
              "betrouwbaarheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als betrouwbaar gezien. Nee: het bewijs wordt niet als betrouwbaar gezien. NVT: onvoldoende informatie om betrouwbaarheid te beoordelen."
              },
              "rechtmatigheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als rechtmatig verkregen beschouwd. Nee: het bewijs wordt niet als rechtmatig verkregen beschouwd. NVT: onvoldoende informatie om rechtmatigheid te beoordelen."
              },
              "overtuigend": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als overtuigend beschouwd. Nee: het bewijs wordt niet als overtuigend beschouwd. NVT: onvoldoende informatie om overtuigingskracht te beoordelen."
              }
            },
            "required": [
              "betrouwbaarheid",
              "rechtmatigheid",
              "overtuigend"
            ],
            "additionalProperties": False
          }
        },
        "required": [
          "rol",
          "zin",
          "crypto_relevant",
          "reden",
          "tags",
          "labels"
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
              "advocaat-generaal",
              "aanklager",
              "het Openbaar Ministerie",
              "OM"
            ],
            "description": "De rol van sleutelfiguur 2."
          },
          "zin": {
            "type": "string",
            "description": "De zin(nen) die het standpunt van sleutelfiguur 2 over het bewijsmateriaal weergeven."
          },
          "crypto_relevant": {
            "type": "boolean",
            "description": "Geeft aan of het standpunt betrekking heeft op crypto-data (waar of niet waar)."
          },
          "reden": {
            "type": "string",
            "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
          },
          "tags": {
            "type": "array",
            "description": "Een lijst met 5 specifieke tags die weergeven hoe en waarom de sleutelfiguur denkt over het crypto-data bewijsmateriaal.",
            "items": {
              "type": "string"
            }
          },
          "labels": {
            "type": "object",
            "description": "Een object met de drie labels 'betrouwbaarheid', 'rechtmatigheid', 'overtuigend', gebaseerd op de rationale.",
            "properties": {
              "betrouwbaarheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als betrouwbaar gezien. Nee: het bewijs wordt niet als betrouwbaar gezien. NVT: onvoldoende informatie om betrouwbaarheid te beoordelen."
              },
              "rechtmatigheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als rechtmatig verkregen beschouwd. Nee: het bewijs wordt niet als rechtmatig verkregen beschouwd. NVT: onvoldoende informatie om rechtmatigheid te beoordelen."
              },
              "overtuigend": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als overtuigend beschouwd. Nee: het bewijs wordt niet als overtuigend beschouwd. NVT: onvoldoende informatie om overtuigingskracht te beoordelen."
              }
            },
            "required": [
              "betrouwbaarheid",
              "rechtmatigheid",
              "overtuigend"
            ],
            "additionalProperties": False
          }
        },
        "required": [
          "rol",
          "zin",
          "crypto_relevant",
          "reden",
          "tags",
          "labels"
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
              "verdediging",
              "raadsman",
              "raadsvrouw",
              "advocaat van de verdachte"
            ],
            "description": "De rol van sleutelfiguur 3."
          },
          "zin": {
            "type": "string",
            "description": "De zin(nen) die het standpunt van sleutelfiguur 3 over het bewijsmateriaal weergeven."
          },
          "crypto_relevant": {
            "type": "boolean",
            "description": "Geeft aan of het standpunt betrekking heeft op crypto-data (waar of niet waar)."
          },
          "reden": {
            "type": "string",
            "description": "Een korte uitleg van waarom de sleutelfiguur dit standpunt heeft over het crypto-data bewijs."
          },
          "tags": {
            "type": "array",
            "description": "Een lijst met 5 specifieke tags die weergeven hoe en waarom de sleutelfiguur denkt over het crypto-data bewijsmateriaal.",
            "items": {
              "type": "string"
            }
          },
          "labels": {
            "type": "object",
            "description": "Een object met de drie labels 'betrouwbaarheid', 'rechtmatigheid', 'overtuigend', gebaseerd op de rationale.",
            "properties": {
              "betrouwbaarheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als betrouwbaar gezien. Nee: het bewijs wordt niet als betrouwbaar gezien. NVT: onvoldoende informatie om betrouwbaarheid te beoordelen."
              },
              "rechtmatigheid": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als rechtmatig verkregen beschouwd. Nee: het bewijs wordt niet als rechtmatig verkregen beschouwd. NVT: onvoldoende informatie om rechtmatigheid te beoordelen."
              },
              "overtuigend": {
                "type": "string",
                "enum": [
                  "ja",
                  "nee",
                  "NVT"
                ],
                "description": "Ja: het bewijs wordt als overtuigend beschouwd. Nee: het bewijs wordt niet als overtuigend beschouwd. NVT: onvoldoende informatie om overtuigingskracht te beoordelen."
              }
            },
            "required": [
              "betrouwbaarheid",
              "rechtmatigheid",
              "overtuigend"
            ],
            "additionalProperties": False
          }
        },
        "required": [
          "rol",
          "zin",
          "crypto_relevant",
          "reden",
          "tags",
          "labels"
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
            "max_tokens": 3000,
            "top_p": 0.74,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
    def get_configuration(self):
        """
        Fetches the configuration for the API.
        Returns:
            dict: A dictionary containing system prompt, parameters, and JSON schema.
        """
        return {
            "client": self.client,

            "api_key": self.api_key,
            "system_prompt": self.system_prompt,
            "json_schema": self.json_schema,
            "parameters": self.parameters
        }

        
    
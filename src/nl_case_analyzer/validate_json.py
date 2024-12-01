import json
from jsonschema import validate, Draft7Validator, exceptions

class ResponseValidator:
    def __init__(self, schema):
        self.schema = schema
        # Pre-compile the schema for better performance
        self.validator = Draft7Validator(self.schema['schema'])

    def is_valid(self, response_json):
        """
        Validates the response JSON against the schema.

        Parameters:
            response_json (str or dict): The JSON response from the API.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            # If the response is a string, parse it into a dictionary
            if isinstance(response_json, str):
                response_data = json.loads(response_json)
            else:
                response_data = response_json

            # Perform the validation
            self.validator.validate(response_data)
            return True
        except exceptions.ValidationError as ve:
            print(f"Validation Error: {ve.message}")
            return False
        except json.JSONDecodeError as je:
            print(f"JSON Decode Error: {je.msg}")
            return False

    def get_validation_errors(self, response_json):
        """
        Returns a list of validation errors.

        Parameters:
            response_json (str or dict): The JSON response from the API.

        Returns:
            list: A list of error messages.
        """
        errors = []
        try:
            if isinstance(response_json, str):
                response_data = json.loads(response_json)
            else:
                response_data = response_json

            for error in sorted(self.validator.iter_errors(response_data), key=str):
                errors.append(error.message)
        except json.JSONDecodeError as je:
            errors.append(f"JSON Decode Error: {je.msg}")
        return errors
# 
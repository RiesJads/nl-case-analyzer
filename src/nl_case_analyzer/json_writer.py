import os
import json


class JSONWriter:
    """
    A utility class to write JSON data to a specified folder.
    """

    def __init__(self, output_dir: str):
        """
        Initializes the JSONWriter.

        Args:
            output_dir (str): The directory where the JSON files will be saved.
        """
        self.output_dir = output_dir
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """
        Ensures the output directory exists. Creates it if it does not exist.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created directory: {self.output_dir}")
        else:
            print(f"Directory already exists: {self.output_dir}")

    def write_json(self, data, file_name: str):
        """
        Writes JSON data to a file in the output directory.

        Args:
            data (dict or list): The JSON-serializable data to save.
            file_name (str): The name of the output JSON file.

        Returns:
            str: The full path to the saved JSON file.
        """
        file_path = os.path.join(self.output_dir, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to: {file_path}")
            return file_path
        except Exception as e:
            print(f"Failed to save JSON data: {e}")
            return None

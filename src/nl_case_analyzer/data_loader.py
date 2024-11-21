import pandas as pd


class CSV_Loader:
    """
    Class that loads the data needed for the analysis of Dutch court cases
    """
    def __init__(self, path: str):
        """
        Initliaze CSV_Loader 
        """
        self.path = path

    def load_dataset(self, 
                     cols_to_filter: str,
                     model_name: str) -> pd.DataFrame():
        
        """
        Reads data from csv and selects analysis data based on selected model 
        Options for model_name:
            Llama 3 8B
            GPT-3.5-Turbo
        """
        try:
            # Load dataset
            data = pd.read_csv(self.path, sep = ";")

            # filtering condition model name
            if cols_to_filter in list(data.columns) and model_name in ("Llama 3 8B", "GPT-3.5-Turbo"):
                data = data[data[cols_to_filter] == model_name]

            # return empty df when filtering conditions is not met
            else:
                print(f"Column '{cols_to_filter}' or model '{model_name}' not present in dataset")
                print(f"Current columns {list(data.columns)}")
                return pd.DataFrame() 

            return data
        
        # returns empty df when file not found
        except FileNotFoundError:
            print(f"File not found at path: {self.path}")
            return pd.DataFrame()

    def generate_txt_snippets(self, df: pd.DataFrame, column_name: str) -> list:
        """
        Prepares snippets of text from a DataFrame column to be inputted in API call.

        Args:
            df (pd.DataFrame): Input DataFrame containing the text data.
            column_name (str): Name of the column containing the text snippets.

        Returns:
            list: A list of text snippets.
        """
        if column_name in df.columns:
            # Extract non-null snippets from the specified column
            snippets = df[column_name].dropna().tolist()
            return snippets
        else:
            # Return an empty list with a message if the column is not found
            print(f"Column '{column_name}' not found in DataFrame.")
            return []
        
    def validate_txt(self, df: pd.DataFrame, column_name: str) -> list:
        """
        Validates if the DataFrame is not empty, previews its content, and generates snippets.

        Args:
            df (pd.DataFrame): Input DataFrame to validate.
            column_name (str): Name of the column to generate text snippets from.

        Returns:
            list: A list of text snippets if DataFrame is valid; otherwise, an empty list.
        """
        if not df.empty:
            print("Data loaded successfully. Here's a preview:")
            print(df.head())

            # Generate text snippets from the specified column
            snippets = self.generate_txt_snippets(df, column_name=column_name)
            print(f"Generated {len(snippets)} snippets.")

            # Preview the first 2 snippets
            for i, snippet in enumerate(snippets[:2]): 
                print(f"Snippet {i + 1}: {snippet}")

            return snippets
        else:
            print("No data available for the specified filter criteria.")
            return []   
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

    def generate_txt_snippets(self, df):
        """
        Prepares snippets of text from df to be inputted in API call
        """

        return list
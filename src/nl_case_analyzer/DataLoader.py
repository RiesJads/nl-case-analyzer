import pandas as pd


class Load_Data():
    """
    Class that loads the data needed for the analysis of Dutch court cases
    """

    def load_dataset(cols_to_filter: str,
                     model_name: str,
                     path: str) -> pd.DataFrame():
        
        """
        Reads data from csv and selects analysis data based on selected model 
        Options for model_name:
            Llama 3 8B
            GPT-3.5-Turbo
        """
        if cols_to_filter in data.columns AND model_name in ("Llama 3 8B", "GPT-3.5-Turbo"):
            data = pd.read_csv(f"{path}")

            data = data[data[cols_to_filter] == model_name]

        else:
            print(f"Column {cols_to_filter} not present in dataset")
        return data



import os
from nl_case_analyzer.openai_api import XXX
from nl_case_analyzer.data_loader import CSV_Loader



def main():

    # root directory of project
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # build path to data folder
    path = os.path.join(project_root, "data", "Analyses_Dataset.csv")

    print(path)
    loader = CSV_Loader(path)
    df = loader.load_dataset(
        cols_to_filter = "Model",
        model_name = "GPT-3.5-Turbo"
        )
    print(df.head())

if __name__ == "__main__":
    main()
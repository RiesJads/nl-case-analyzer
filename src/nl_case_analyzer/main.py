
import os
import json
import glob
from nl_case_analyzer.data_loader import CSV_Loader
from nl_case_analyzer.openai_config import ConfigGPT
from nl_case_analyzer.analyze import AnalyzeGPT
from nl_case_analyzer.validate_json import ResponseValidator
from nl_case_analyzer.json_writer import JSONWriter
from nl_case_analyzer.visualizer import Visualizer


def main():

    # root directory of project
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # build path to data folder

    path = os.path.join(project_root, "data", "Analyses_Dataset.csv")
    output_dir = os.path.join(project_root, "results")


    # Loading data
    print(f"Loading data from: {path}")
    loader = CSV_Loader(path)
    df = loader.load_dataset(
        cols_to_filter = "Model",
        model_name = "GPT-3.5-Turbo"
        )
    
    # Validate
    snippets = loader.validate_txt(df, column_name="Answer")


    if snippets:
        # Initialize API configurations
        config_gpt = ConfigGPT()
        config = config_gpt.get_configuration()

        schema = config['json_schema']

        # Initialize the OpenAI API handler
        openai_api = AnalyzeGPT(config)

        # Initialize the validation function 
        validator = ResponseValidator(schema=schema)

        

        # Analyze snippts
        print("Starting API calls for text snippets...")
        results = openai_api.analyze_snippets(snippets[600:], timeout=1)

        # Validate
        invalid_snippets = []
        for idx, response in enumerate(results):
            print(f"\n Validating Snippet {idx}")
            if not validator.is_valid(response):
                 print(f"Snippet {idx + 1} is invalid.")
                 # append to list 
                 invalid_snippets.append(idx)
            else:
                print(f"Snippet {idx + 1} is valid.")

        print("\nSummary of Validation:")
        if invalid_snippets:
            print(f"The following snippets are invalid: {invalid_snippets}")
        else:
            print("All snippets are valid.")


        # write JSON (list of jsons)s
        json_writer = JSONWriter(output_dir)
        result_file = json_writer.write_json(results, "Results_3.json")

    
        # Loading in Results 
        results_file_path = glob.glob(os.path.join(output_dir, "*.json"))
        result_list = []

        for file in results_file_path:

            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                result_list.extend(data)
        # Visualization

        visualizer = Visualizer(result_list, output_dir)
        visualizer.generate_wordcloud()
        visualizer.plot_label_distributions()

        print("chepoint mate")
    
    else:
        print("Loading snippets went down the drain")
    
    
if __name__ == "__main__":
    main()
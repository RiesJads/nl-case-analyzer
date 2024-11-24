
import os
from nl_case_analyzer.data_loader import CSV_Loader
from nl_case_analyzer.openai_config import ConfigGPT
from nl_case_analyzer.analyze import AnalyzeGPT
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

        # Initialize the OpenAI API handler
        openai_api = AnalyzeGPT(config)

        # Analyze snippts
        print("Starting API calls for text snippets...")
        results = openai_api.analyze_snippets(snippets[:200], timeout=2)

        # write JSON (list of jsons)s
        json_writer = JSONWriter(output_dir)
        result_file = json_writer.write_json(results, "Results.json")
    
        # Visualization
        # results_file_path = os.path.join(output_dir, "Results.json")
        visualizer = Visualizer(results, output_dir)
        visualizer.generate_wordcloud()
        visualizer.plot_label_distributions()
    
    else:
        print("Loading snippets went down the drain")
    
    
if __name__ == "__main__":
    main()
import os
import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
from IPython.display import display

class Visualizer:
    def __init__(self, json_list, output_dir):
        self.json_list = json_list
        self.output_dir = output_dir
        self.visuals_dir = os.path.join(self.output_dir, 'vizuals')
        os.makedirs(self.visuals_dir, exist_ok=True)
        self.sleutelfiguren_mapping = {
                        'sleutelfiguur_1': 'Rechter',
                        'sleutelfiguur_2': 'Aanklager',
                        'sleutelfiguur_3': 'Verdediging'
                        }
        self.sleutelfiguren = list(self.sleutelfiguren_mapping.keys())

        self.df = self._prepare_data_viz()

    def _prepare_data_viz(self):
        """
        Process the JSON data and prepare a pandas DataFrame.
        """
        records = []
        for json_str in self.json_list:
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON string skipped: {e}")
                continue
            
            for figuur in self.sleutelfiguren:
                fig_data = data.get(figuur)

                if fig_data:
                    labels = fig_data.get('labels', {})
                    crypto_relevant = fig_data.get('crypto_relevant', "false")
                    for label_name, label_value in labels.items():
                        records.append({
                            'sleutelfiguur': self.sleutelfiguren_mapping.get(figuur),
                            'label': label_name,
                            'value': label_value.lower(), 
                            'crypto_relevant': 'Ja' if crypto_relevant else 'Nee'
                        })
        df = pd.DataFrame(records)
        if df.empty:
            print("Warning: The prepared DataFrame is empty.")
        return df 
                      
    
    def _prepare_data_full_conversion(self):
        """
        Process the JSON data and prepare a pandas DataFrame.
        """
        records = []
        for json_str in self.json_list:
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON string skipped: {e}")
                continue
            for idx, json_str in enumerate(self.json_list, start=1):
                for figuur in self.sleutelfiguren:
                    fig_data = data.get(figuur)

                    if fig_data:
                        rol = fig_data.get('rol', None)
                        zin = fig_data.get('zin', None)
                        crypto_relevant = fig_data.get('crypto_relevant', False)
                        reden = fig_data.get('reden', None)
                        tags = fig_data.get('tags', [])
                        labels = fig_data.get('labels', {})
                        
                        # Extract individual label values, defaulting to 'NVT' if not present
                        betrouwbaarheid = labels.get('betrouwbaarheid', 'NVT')
                        rechtmatigheid = labels.get('rechtmatigheid', 'NVT')
                        overtuigend = labels.get('overtuigend', 'NVT')
                        
                        # Convert tags list to a comma-separated string
                        tags_str = ", ".join(tags)
                        
                        records.append({
                            'json_index': idx,  # To track which JSON string the data came from
                            'sleutelfiguur': figuur,
                            'rol': rol,
                            'zin': zin,
                            'crypto_relevant': 'Ja' if crypto_relevant else 'Nee',
                            'reden': reden,
                            'tags': tags_str,
                            'betrouwbaarheid': betrouwbaarheid.lower(),  # Convert to lowercase for consistency
                            'rechtmatigheid': rechtmatigheid.lower(),
                            'overtuigend': overtuigend.lower()
                        })
                    
        
        df = pd.DataFrame(records)
        if df.empty:
            print("Warning: The prepared DataFrame is empty.")
        else:
            print(f"Data preparation complete. {len(df)} records added to the DataFrame.")
        return df

    def generate_plot(self, figuur):
        """
        Generate a seaborn count plot for a given sleutelfiguur.
        
        Parameters:
            figuur (str): The sleutelfiguur to plot.
        
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        fig_df = self.df[self.df['sleutelfiguur'] == figuur]
        if fig_df.empty:
            print(f"No data available for sleutelfiguur: {figuur}")
            return None
        plt.figure(figsize=(16, 10))
        ax = sns.countplot(
            data=fig_df,
            x='label',
            hue='value',
            palette='Set2',
            order=['betrouwbaarheid', 'rechtmatigheid', 'overtuigend'],
            hue_order=['ja', 'nee', 'nvt']
            )

        plt.suptitle(f"De {figuur}", fontsize=20)
        plt.title("Verdeling van de standpunten volgens de criteria", fontsize=14, x=.55)

        plt.xlabel('Criterium', fontsize= 16)
        plt.ylabel('Aantal', fontsize = 16)
        plt.xticks(fontsize=14)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='Voldoet aan criterium:', loc='upper right', bbox_to_anchor=(1.15,1),
                  fontsize=14)
        plt.tight_layout()

        for p in ax.patches:
            height = round(p.get_height())
            if height > 0:
                ax.annotate(
                    f'{height}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center',  # Horizontal alignment
                    va='bottom',  # Vertical alignment
                    fontsize=14,
                    color='black',
                    xytext=(0, 2),  # Offset text by 5 points above the bar
                    textcoords='offset points'
                )
        
        # Capture the current figure
        fig = ax.get_figure()
        plt.close(fig)  # Prevents the figure from displaying automatically
        return fig
    
    def display_plots(self):
        """
        Display all generated plots inline within the Jupyter notebook.
        """
        for figuur in self.sleutelfiguren:
            fig = self.generate_plot(self.sleutelfiguren_mapping.get(figuur))
            if fig:
                display(fig)
                print(f"Displayed plot for {figuur}")

    def save_plots(self):
        """
        Save all generated plots to the specified directory.
        """
        if not os.path.exists(self.visuals_dir):
            os.makedirs(self.visuals_dir)
            print(f"Created directory: {self.visuals_dir}")

        for figuur in self.sleutelfiguren:
            fig = self.generate_plot(self.sleutelfiguren_mapping.get(figuur))
            if fig:
                plot_path = os.path.join(self.visuals_dir, f"{figuur}_label_distribution.png")
                fig.savefig(plot_path)
                print(f"Label distribution plot saved to {plot_path}")



    def generate_wordcloud(self):
        # Extract tags from all sleutelfiguren
        tags = []
        for json_str in self.json_list:
            data = json.loads(json_str)
            for figuur in self.sleutelfiguren:
                if data.get(figuur) and data[figuur].get('tags'):
                    tags.extend(data[figuur]['tags'])
        # Calculate word frequencies
        word_counts = Counter(tags)
        # Select top 50% most frequent words
        most_common_words = word_counts.most_common()
        top_50_percent_index = len(most_common_words) // 2
        top_words = dict(most_common_words[:top_50_percent_index])
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_words)
        # Save the word cloud
        plt.figure(figsize=(15, 7.5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        wordcloud_path = os.path.join(self.visuals_dir, 'wordcloud.png')
        plt.savefig(wordcloud_path)
        plt.close()
        print(f"Word cloud saved to {wordcloud_path}")

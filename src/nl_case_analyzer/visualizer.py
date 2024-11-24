import os
import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, json_list, output_dir):
        self.json_list = json_list
        self.output_dir = output_dir
        self.visuals_dir = os.path.join(self.output_dir, 'vizuals')
        os.makedirs(self.visuals_dir, exist_ok=True)
        self.sleutelfiguren = ['sleutelfiguur_1', 'sleutelfiguur_2', 'sleutelfiguur_3']

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

    def plot_label_distributions(self):
        # Prepare data
        records = []
        for json_str in self.json_list:
            data = json.loads(json_str)
            for figuur in self.sleutelfiguren:
                fig_data = data.get(figuur)
                if fig_data:
                    labels = fig_data.get('labels', {})
                    crypto_relevant = fig_data.get('crypto_relevant', "false")
                    for label_name, label_value in labels.items():
                        records.append({
                            'sleutelfiguur': figuur,
                            'label': label_name,
                            'value': label_value,
                            'crypto_relevant': 'Ja' if crypto_relevant else 'Nee'
                        })
        df = pd.DataFrame(records)
        # Plotting for each sleutelfiguur
        for figuur in self.sleutelfiguren:
            fig_df = df[df['sleutelfiguur'] == figuur]
            plt.figure(figsize=(10, 6))
            sns.countplot(
                data=fig_df,
                x='label',
                hue='value',
                palette='Set2',
                order=['betrouwbaarheid', 'rechtmatigheid', 'overtuigend'],
                hue_order=['ja', 'nee', 'NVT']
            )
            plt.title(f"Label Distribution for {figuur}")
            plt.xlabel('Label')
            plt.ylabel('Count')
            plt.legend(title='Value')
            plt.tight_layout()
            plot_path = os.path.join(self.visuals_dir, f"{figuur}_label_distribution.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"Label distribution plot saved to {plot_path}")


# src/data_visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Setting a clean statistical aesthetic for plots
        sns.set_theme(style="whitegrid")

    def plot_popularity_distribution(self, output_name="1_popularity_distribution.png"):
        """Plot 1: Histogram of Popularity Score to show the general spread."""
        plt.figure(figsize=(9, 5))
        sns.histplot(data=self.df, x='popularity', bins=30, kde=True, color='skyblue')
        plt.title('Distribution of Track Popularity on Spotify', fontsize=14, pad=15)
        plt.xlabel('Popularity Score (0-100)')
        plt.ylabel('Count / Frequency')
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close()

    def plot_danceability_vs_energy(self, output_name="2_danceability_vs_energy.png"):
        """Plot 2: Scatter plot to examine relationship between Danceability and Energy."""
        plt.figure(figsize=(9, 6))
        # Sampling 1000 rows for faster and cleaner plotting on dense datasets
        sample_df = self.df.sample(n=min(1000, len(self.df)), random_state=42)
        sns.scatterplot(data=sample_df, x='danceability', y='energy', alpha=0.6, color='purple')
        plt.title('Danceability vs. Energy (Sample of 1,000 Tracks)', fontsize=14, pad=15)
        plt.xlabel('Danceability Factor')
        plt.ylabel('Energy Level')
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close()

    def plot_correlation_matrix(self, correlation_matrix, output_name="3_correlation_matrix.png"):
        """Plot 3: Heatmap of numerical audio attributes correlation."""
        if correlation_matrix is None:
            return
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, linewidths=.5)
        plt.title('Audio Feature Correlation Heatmap', fontsize=14, pad=15)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close()

    def plot_popularity_boxplot(self, output_name="4_popularity_boxplot.png"):
        """Plot 4: Box Plot of Popularity to visual check for outliers."""
        plt.figure(figsize=(6, 5))
        sns.boxplot(data=self.df, y='popularity', color='lightgreen')
        plt.title('Box Plot of Track Popularity (Outlier Analysis)', fontsize=14, pad=15)
        plt.ylabel('Popularity Score')
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close()
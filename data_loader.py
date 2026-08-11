# src/data_loader.py
import os
import pandas as pd
from src.song import Song  # Importing our validated Song model

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_dataset(self):
        """Loads the Spotify dataset from disk safely with error handling."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Dataset file not found at: {self.file_path}")
        
        # Low_memory=False prevents warnings with large student datasets
        self.df = pd.read_csv(self.file_path, low_memory=False)
        return self.df

    def get_missing_report(self):
        """Generates a simple dictionary report of missing values per column."""
        if self.df is None:
            return "Dataset is not loaded yet."
        
        # Count missing values for each column
        missing_counts = self.df.isnull().sum()
        report = {col: int(count) for col, count in missing_counts.items() if count > 0}
        
        if not report:
            return "No missing values detected in the current dataset!"
        return report

    def append_song(self, song: Song):
        """Appends a single Song object directly to the CSV file and updates RAM."""
        if self.df is None:
            raise ValueError("Cannot append song. Dataset is not loaded in memory.")

        # Convert the Song object into a standard dictionary format
        new_song_dict = song.to_dict()
        
        # Create a tiny DataFrame for the single new row
        new_row_df = pd.DataFrame([new_song_dict])
        
        # 1. Update the physical file on disk using Append Mode ('a')
        # header=False prevents re-writing column names into the middle of the file
        new_row_df.to_csv(self.file_path, mode='a', index=False, header=False)
        
        # 2. Update the active RAM data using pandas concatenation
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)
        return True
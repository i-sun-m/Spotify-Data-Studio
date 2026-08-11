# src/data_analyzer.py
import pandas as pd

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_genre_insights(self):
        """Calculates average popularity, danceability, and energy per genre."""
        if self.df is None or self.df.empty:
            return None
        
        # Group by genre and calculate the mean for key metrics
        grouped = self.df.groupby('track_genre')[['popularity', 'danceability', 'energy']].mean()
        # Sort by popularity to show the top trending genres
        return grouped.sort_values(by='popularity', ascending=False)

    def get_correlation_matrix(self):
        """Calculates the correlation matrix for the specified numerical audio features."""
        if self.df is None or self.df.empty:
            return None
        
        features = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness']
        # Select only existing numerical features to avoid potential KeyError
        valid_features = [f for f in features if f in self.df.columns]
        return self.df[valid_features].corr()

    def generate_mood_playlist(self, mood: str):
        """
        [BONUS FEATURE] Generates a 7-song playlist tailored to the user's emotional mood.
        Uses exact logic based on audio features like valence, energy, and tempo.
        """
        if self.df is None or self.df.empty:
            return None

        mood = mood.lower().strip()
        filtered_df = self.df.copy()

        # Filtering logic based on real psychoacoustic properties in Spotify Data
        if mood == 'happy':
            # Happy: High valence (positivity) and good energy
            filtered_df = filtered_df[(filtered_df['valence'] > 0.6) & (filtered_df['energy'] > 0.5)]
        elif mood == 'sad':
            # Sad: Low valence and low energy
            filtered_df = filtered_df[(filtered_df['valence'] < 0.3) & (filtered_df['energy'] < 0.4)]
        elif mood == 'energetic':
            # Energetic: High energy and fast tempo
            filtered_df = filtered_df[(filtered_df['energy'] > 0.75) & (filtered_df['tempo'] > 120)]
        elif mood == 'relaxed':
            # Relaxed: Low energy, lower tempo, and higher acoustic quality
            filtered_df = filtered_df[(filtered_df['energy'] < 0.4) & (filtered_df['acousticness'] > 0.5)]
        else:
            # Fallback if an unknown mood is passed
            return None

        # Check if we have enough tracks after filtering
        if len(filtered_df) == 0:
            return pd.DataFrame()  # Empty fallback

        # Naturally sample exactly 7 songs randomly without replacement
        sample_size = min(7, len(filtered_df))
        playlist = filtered_df.sample(n=sample_size, random_state=None)
        
        return playlist[['track_name', 'artists', 'album_name', 'track_genre', 'popularity']]
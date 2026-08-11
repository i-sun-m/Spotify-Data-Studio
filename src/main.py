# src/main.py
import os
import sys

# Standard way for students to ensure local src package can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
from src.data_cleaner import MeanImputer, MedianImputer, KNNImputer, IQROutlierHandler, ZScoreOutlierHandler
from src.data_analyzer import DataAnalyzer
from src.data_visualizer import DataVisualizer
from src.song import Song

def display_menu():
    print("\n" + "="*50)
    print("         SPOTIFY DATA STUDIO - MAIN MENU")
    print("="*50)
    print("1. Load Dataset & Show Missing Values Report")
    print("2. Handle Missing Values (Imputation)")
    print("3. Handle Outliers (Capping)")
    print("4. Add a New Track (Append Mode)")
    print("5. Generate Statistical Insights (Genres & Correlations)")
    print("6. Generate and Save Analytical Charts")
    print("7. [BONUS] Generate Mood Playlist (7 Special Tracks)")
    print("8. Exit Application")
    print("="*50)

def main():
    # Define default path for the dataset
    # Change this if your dataset filename is different
    dataset_path = os.path.join("data", "spotify_tracks.csv")
    
    # Check if the data folder exists, if not create it to prevent crashes
    if not os.path.exists("data"):
        os.makedirs("data")

    loader = DataLoader(dataset_path)
    print("Welcome to Spotify Data Studio!")
    print(f"Target dataset file location set to: {dataset_path}")

    while True:
        display_menu()
        choice = input("Please select an option (1-8): ").strip()

        try:
            if choice == '1':
                print("\n[Action] Loading dataset...")
                df = loader.load_dataset()
                print(f"Successfully loaded! Dataset contains {len(df)} rows and {len(df.columns)} columns.")
                
                print("\n--- Missing Values Report ---")
                report = loader.get_missing_report()
                if isinstance(report, dict):
                    for col, count in report.items():
                        print(f"-> Column '{col}': {count} missing values")
                else:
                    print(report)

            elif choice == '2':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                print("\n--- Missing Value Imputation Methods ---")
                print("1. Mean Imputer")
                print("2. Median Imputer")
                print("3. KNN Imputer (Smart Neighbor Estimation)")
                imp_choice = input("Select imputation strategy: ").strip()
                
                col_to_impute = input("Enter the column name to clean: ").strip()
                if col_to_impute not in loader.df.columns:
                    print(f"Error: Column '{col_to_impute}' does not exist.")
                    continue

                if imp_choice == '1':
                    imputer = MeanImputer()
                elif imp_choice == '2':
                    imputer = MedianImputer()
                elif imp_choice == '3':
                    imputer = KNNImputer(n_neighbors=5)
                else:
                    print("Invalid selection. Returning to main menu.")
                    continue

                print(f"Applying imputation on '{col_to_impute}'...")
                loader.df = imputer.impute(loader.df, col_to_impute)
                print("Imputation completed successfully!")

            elif choice == '3':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                print("\n--- Outlier Handling Methods ---")
                print("1. IQR Method (Interquartile Range Capping)")
                print("2. Z-Score Method (Standard Deviations Capping)")
                out_choice = input("Select outlier strategy: ").strip()
                
                col_to_clean = input("Enter the numerical column name: ").strip()
                if col_to_clean not in loader.df.columns:
                    print(f"Error: Column '{col_to_clean}' does not exist.")
                    continue

                if out_choice == '1':
                    handler = IQROutlierHandler()
                elif out_choice == '2':
                    handler = ZScoreOutlierHandler(threshold=3.0)
                else:
                    print("Invalid selection. Returning to main menu.")
                    continue

                print(f"Handling outliers on '{col_to_clean}'...")
                loader.df = handler.handle(loader.df, col_to_clean)
                print("Outlier processing completed successfully!")

            elif choice == '4':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                print("\n--- Add a New Track to Dataset ---")
                print("Please provide track information:")
                
                # Gathering inputs for a valid Song object
                t_id = input("Track ID (e.g., 5Y95x...): ").strip()
                artists = input("Artists (e.g., Taylor Swift): ").strip()
                album = input("Album Name: ").strip()
                name = input("Track Name: ").strip()
                
                # Numeric inputs wrapped in try-except for safe conversion
                try:
                    pop = int(input("Popularity (0-100): "))
                    duration = int(input("Duration (in ms): "))
                    explicit = input("Explicit? (true/false): ").lower() == 'true'
                    dance = float(input("Danceability (0.0-1.0): "))
                    energy = float(input("Energy (0.0-1.0): "))
                    genre = input("Track Genre (e.g., pop, rock): ").strip()
                except ValueError:
                    print("Validation Error: Invalid number format entered. Track insertion aborted.")
                    continue

                # Constructing the Song object (This automatically fires property validation setters!)
                try:
                    new_song = Song(
                        track_id=t_id, artists=artists, album_name=album, track_name=name,
                        popularity=pop, duration_ms=duration, explicit=explicit,
                        danceability=dance, energy=energy, key=0, loudness=-5.0, mode=1,
                        speechiness=0.0, acousticness=0.0, instrumentalness=0.0,
                        liveness=0.0, valence=0.5, tempo=120.0, time_signature=4, track_genre=genre
                    )
                except ValueError as ve:
                    print(f"Validation Error: {ve} Track insertion aborted.")
                    continue

                print("Appending track to database file and memory...")
                loader.append_song(new_song)
                print(f"Success! '{new_song}' added. Total tracks in memory: {len(loader.df)}")

            elif choice == '5':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                analyzer = DataAnalyzer(loader.df)
                print("\n--- Top 10 Most Popular Genres (Averages) ---")
                genre_insights = analyzer.get_genre_insights()
                if genre_insights is not None:
                    print(genre_insights.head(10))
                
                print("\n--- Audio Features Correlation Matrix ---")
                corr_matrix = analyzer.get_correlation_matrix()
                if corr_matrix is not None:
                    print(corr_matrix)

            elif choice == '6':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                print("\n[Action] Generating analytical plots...")
                visualizer = DataVisualizer(loader.df)
                analyzer = DataAnalyzer(loader.df)
                
                visualizer.plot_popularity_distribution()
                visualizer.plot_danceability_vs_energy()
                visualizer.plot_correlation_matrix(analyzer.get_correlation_matrix())
                visualizer.plot_popularity_boxplot()
                
                print("All 4 charts have been generated and saved to the project directory!")
                print("Files generated: ")
                print(" - 1_popularity_distribution.png\n - 2_danceability_vs_energy.png")
                print(" - 3_correlation_matrix.png\n - 4_popularity_boxplot.png")

            elif choice == '7':
                if loader.df is None:
                    print("Error: Please load the dataset first (Option 1).")
                    continue
                
                print("\n--- Creative Feature: Mood Playlist Generator ---")
                print("Choose your current emotional mood:")
                print("Options: happy, sad, energetic, relaxed")
                selected_mood = input("Enter mood: ").strip()
                
                analyzer = DataAnalyzer(loader.df)
                playlist = analyzer.generate_mood_playlist(selected_mood)
                
                if playlist is None:
                    print("Error: Unknown mood selection.")
                elif playlist.empty:
                    print("No songs found matching this criteria in the current dataset slice.")
                else:
                    print(f"\n>>>> YOUR CUSTOM 7-SONG '{selected_mood.upper()}' PLAYLIST <<<<")
                    print("="*75)
                    # Simple clean counter presentation for the CLI
                    for idx, row in playlist.iterrows():
                        print(f"Track: {row['track_name']} | Artist: {row['artists']} | Genre: {row['track_genre']} (Pop: {row['popularity']})")
                    print("="*75)

            elif choice == '8':
                print("\nThank you for using Spotify Data Studio. Exiting application. Goodbye!")
                break
            else:
                print("Invalid menu choice. Please select a valid number between 1 and 8.")

        except Exception as e:
            print(f"\nAn unexpected runtime error occurred: {e}")
            print("The system recovered safely. Please try again.")

if __name__ == "__main__":
    main()

# src/song.py

class Song:
    def __init__(self, track_id, artists, album_name, track_name, popularity, 
                 duration_ms, explicit, danceability, energy, key, loudness, 
                 mode, speechiness, acousticness, instrumentalness, liveness, 
                 valence, tempo, time_signature, track_genre):
        
        # Identity attributes
        self.track_id = str(track_id)
        self.artists = str(artists)
        self.album_name = str(album_name)
        self.track_name = str(track_name)
        
        # Validated attributes via setters
        self.popularity = popularity
        self.danceability = danceability
        self.energy = energy
        
        # Technical & Audio features
        self.duration_ms = int(duration_ms)
        self.explicit = bool(explicit)
        self.key = int(key)
        self.loudness = float(loudness)
        self.mode = int(mode)
        self.speechiness = float(speechiness)
        self.acousticness = float(acousticness)
        self.instrumentalness = float(instrumentalness)
        self.liveness = float(liveness)
        self.valence = float(valence)
        self.tempo = float(tempo)
        self.time_signature = int(time_signature)
        self.track_genre = str(track_genre)

    # Property for popularity (Constraint: 0 to 100)
    @property
    def popularity(self):
        return self._popularity

    @popularity.setter
    def popularity(self, value):
        val = int(value)
        if not (0 <= val <= 100):
            raise ValueError("Popularity must be between 0 and 100.")
        self._popularity = val

    # Property for danceability (Constraint: 0.0 to 1.0)
    @property
    def danceability(self):
        return self._danceability

    @danceability.setter
    def danceability(self, value):
        val = float(value)
        if not (0.0 <= val <= 1.0):
            raise ValueError("Danceability must be between 0.0 and 1.0.")
        self._danceability = val

    # Property for energy (Constraint: 0.0 to 1.0)
    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        val = float(value)
        if not (0.0 <= val <= 1.0):
            raise ValueError("Energy must be between 0.0 and 1.0.")
        self._energy = val

    def to_dict(self):
        """Converts the song object data into a dictionary for pandas integration."""
        return {
            'track_id': self.track_id, 'artists': self.artists, 
            'album_name': self.album_name, 'track_name': self.track_name,
            'popularity': self.popularity, 'duration_ms': self.duration_ms, 
            'explicit': self.explicit, 'danceability': self.danceability, 
            'energy': self.energy, 'key': self.key, 'loudness': self.loudness, 
            'mode': self.mode, 'speechiness': self.speechiness, 
            'acousticness': self.acousticness, 'instrumentalness': self.instrumentalness, 
            'liveness': self.liveness, 'valence': self.valence, 
            'tempo': self.tempo, 'time_signature': self.time_signature, 
            'track_genre': self.track_genre
        }

    def __str__(self):
        return f"{self.track_name} by {self.artists} [{self.track_genre}]"

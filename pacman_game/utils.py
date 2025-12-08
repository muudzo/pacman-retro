import json
import os

class HighScoreManager:
    def __init__(self, filename="highscore.json"):
        self.filename = filename
        self.high_score = 0
        self.load_high_score()
    
    def load_high_score(self):
        """Load high score from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or can't be read, start fresh
                self.high_score = 0
    
    def save_high_score(self):
        """Save high score to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except IOError:
            # If we can't save, just continue (high score will be lost)
            pass
    
    def update_high_score(self, score):
        """Update high score if current score is higher."""
        if score > self.high_score:
            self.high_score = score
            self.save_high_score()
            return True  # New high score!
        return False
    
    def get_high_score(self):
        """Get the current high score."""
        return self.high_score

#general tools used in app.py
import re

def extract(response):
    pattern = r'(acousticness|danceability|tempo|valence|energy):?\s*(\d+(\.\d+)?)'
    matches = re.findall(pattern, response)
    matches_dict = {}
    for match in matches:
        keyword, value, _ = match
        matches_dict[keyword] = float(value)
    return matches_dict


# Test the function with your input string

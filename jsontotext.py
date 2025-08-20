import requests
import json

# Fetch data from Football-Data.org API
API_KEY = "56f38217075b4148a26a89c7494ac1eb"  
BASE_URL = "https://api.football-data.org/v4/competitions/CL/matches"

# Headers for the API request
headers = {
    "X-Auth-Token": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Make the GET request with headers
response = requests.get(BASE_URL, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Write the JSON data to a file (convert to string first)
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)  # Use json.dump instead of .write for correct formatting

    matches = data.get('matches', [])
    print("Data fetched successfully")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    matches = []

# Function to format the JSON data into a readable .txt file
def format_json_to_txt(json_data, file_name="formatted_matches.txt"):
    if not json_data:
        print("No match data available to write.")
        return
    
    try:
        with open(file_name, "w") as file:
            for match in json_data:
                # Debugging the structure of match
                print(f"Match data: {match}")  # Check the structure of the match
                
                # Ensure the match data contains the required keys
                try:
                    home_team = match['homeTeam']['name']
                    away_team = match['awayTeam']['name']
                    home_goals = match['score']['fullTime']['home']
                    away_goals = match['score']['fullTime']['away']
                    status = match['status']
                    match_date = match['utcDate']
                    
                    # Write match details to the file
                    file.write(f"Home Team: {home_team}\n")
                    file.write(f"Away Team: {away_team}\n")
                    file.write(f"Home Goals: {home_goals}\n")
                    file.write(f"Away Goals: {away_goals}\n")
                    if home_goals > away_goals:
                        file.write(f"Home Wins\n")
                    elif away_goals > home_goals:
                        file.write(f"Away Wins\n")
                    else:
                        file.write(f"Draw\n")
                    file.write(f"Status: {status}\n")
                    file.write(f"Match Date: {match_date}\n\n")
                except KeyError as e:
                    print(f"Missing key {e} in match data. Skipping match.")
        
        print(f"Data has been written to {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Call the function to save formatted data into the txt file
format_json_to_txt(matches)

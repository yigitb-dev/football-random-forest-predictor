import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Function to create a DataFrame from the formatted .txt file
def create_dataframe_from_txt(file_name="formatted_matches.txt"):
    rows = []
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

            # Initialize a dictionary to hold match data for each match
            match_data = {}
            
            # Iterate over the lines in the file
            for line in lines:
                line = line.strip()  # Clean up extra spaces and newlines
                
                # Extract and store relevant match information
                if line.startswith("Home Team"):
                    match_data['home_team'] = line.split(": ")[1]
                elif line.startswith("Away Team"):
                    match_data['away_team'] = line.split(": ")[1]
                elif line.startswith("Home Goals"):
                    match_data['home_goals'] = int(line.split(": ")[1])
                elif line.startswith("Away Goals"):
                    match_data['away_goals'] = int(line.split(": ")[1])
                elif line.startswith("Status"):
                    match_data['status'] = line.split(": ")[1]
                elif line.startswith("Match Date"):
                    match_data['match_date'] = line.split(": ")[1]
                    # Once all fields for a match are gathered, add it to rows and reset match_data
                    rows.append(match_data)
                    match_data = {}  # Reset for the next match

        # Convert the list of rows into a DataFrame
        df = pd.DataFrame(rows)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return pd.DataFrame()  # Return empty DataFrame if error occurs

# Create DataFrame from the formatted .txt file
df = create_dataframe_from_txt()


# Check if data was successfully read into the DataFrame
if not df.empty:
    print("First few rows of the DataFrame:")
    print(df.head())

    # Encode categorical team names
    label_encoder = LabelEncoder()
    df['home_team'] = label_encoder.fit_transform(df['home_team'])
    df['away_team'] = label_encoder.transform(df['away_team'])

    # Define features X and target y
    X = df.drop(['home_team_win'], axis=1, errors='ignore')
    y = df['home_team_win'] if 'home_team_win' in df.columns else None

    # Ensure target variable exists
    if y is not None:
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Random Forest
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate model
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        # Feature importance
        importances = model.feature_importances_
        feature_names = X.columns
        feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
        print(feature_importance_df.sort_values(by='importance', ascending=False))

        # User input for prediction
        user_home_team = input("\nHome Team: ")
        user_away_team = input("\nAway Team: ")

        # Predict a new match (example placeholder values for goals)
        new_match = pd.DataFrame({
            'home_team': [label_encoder.transform([user_home_team])[0]],
            'away_team': [label_encoder.transform([user_away_team])[0]],
            'home_goals': [2.0],  # Placeholder value
            'away_goals': [1.5],  # Placeholder value
        })

        prediction = model.predict(new_match)
        print(f"Prediction for the match: {'Home Team Win' if prediction[0] == 1 else 'Home Team Lose'}")
    else:
        print("Target variable 'home_team_win' not found in the data. Please ensure the .txt file has this field.")
else:
    print("No data to train the model.")

class Analysis:
    def __init__(self, predictions1, predictions2, predictions3):
        self.predictions1 = predictions1
        self.predictions2 = predictions2
        self.predictions3 = predictions3

    def normalize_team_names(self, team_name):
        team_map = {
            "newcastle united": "newcastle", "arsenal": "arsenal", "ipswich town": "ipswich", "leicester city": "leicester",
            "liverpool": "liverpool", "brighton": "brighton", "nottingham forest": "nott’m forest", "west ham": "west ham",
            "southampton": "southampton", "everton": "everton", "bournemouth": "bournemouth", "manchester city": "man city",
            "wolverhampton": "wolves", "crystal palace": "crystal palace", "tottenham": "tottenham",
            "aston villa": "aston villa", "manchester united": "man united", "chelsea": "chelsea",
            "fulham": "fulham", "brentford": "brentford"
        }
        return team_map.get(team_name.lower(), team_name.lower())

    def merge_predictions(self):
        merged_predictions = {}

        def add_predictions(predictions):
            for match in predictions:
                teams = list(match.keys())
                for team in teams:
                    normalized_team = self.normalize_team_names(team)
                    if normalized_team in merged_predictions:
                        merged_predictions[normalized_team].append(match[team])
                    else:
                        merged_predictions[normalized_team] = [match[team]]

        # Add all predictions to merged_predictions
        add_predictions(self.predictions1)
        add_predictions(self.predictions2)
        add_predictions(self.predictions3)

        averaged_predictions = {}
        for team, values in merged_predictions.items():
            averaged_predictions[team] = sum(values) / len(values)

        return averaged_predictions

    def print(self):
        averaged_predictions = self.merge_predictions()
        
        print(f"{'Team 1':<15} | {'Percentage':<10} | - | {'Percentage':<10} | {'Team 2'}")
        print("-" * 55)

        for prediction in self.predictions1:
            teams = list(prediction.keys())
            if len(teams) == 2:
                team1, team2 = self.normalize_team_names(teams[0]), self.normalize_team_names(teams[1])
                percentage1 = averaged_predictions.get(team1, 0)
                percentage2 = averaged_predictions.get(team2, 0)
                print(f"{team1.capitalize():<15} | {percentage1:.2%} | - | {percentage2:.2%} | {team2.capitalize()}")


import json
import requests
import pandas as pd

list_teams = ['Boston College', 'Clemson', 'Duke', 'Florida State', 'Georgia Tech', 'Louisville', 'Miami', 'NC State', 'North Carolina', 'Pittsburgh', 'Syracuse', 'Virginia', 'Virginia Tech', 'Wake Forest', 'Baylor', 'Iowa State', 'Kansas', 'Kansas State', 'Oklahoma', 'Oklahoma State', 'TCU', 'Texas', 'Texas Tech', 'West Virginia', 'Illinois', 'Indiana', 'Iowa', 'Maryland', 'Michigan', 'Michigan State', 'Minnesota', 'Nebraska', 'Northwestern', 'Ohio State', 'Penn State', 'Purdue', 'Rutgers', 'Wisconsin', 'Alabama', 'Arkansas', 'Auburn', 'Florida', 'Georgia', 'Kentucky', 'LSU', 'Mississippi State', 'Missouri', 'Ole Miss', 'South Carolina', 'Tennessee', 'Texas A&M', 'Vanderbilt', 'Arizona', 'Arizona State', 'California', 'Colorado', 'Oregon', 'Oregon State', 'Stanford', 'UCLA', 'USC', 'Utah', 'Washington', 'Washington State', 'Charlotte', 'Florida Atlantic', 'Florida International', 'Louisiana Tech', 'Marshall', 'Middle Tennessee', 'North Texas', 'Old Dominion', 'Rice', 'Southern Mississippi', 'UAB', 'UTEP', 'UT San Antonio', 'Western Kentucky', 'Akron', 'Ball State', 'Bowling Green', 'Buffalo', 'Central Michigan', 'Eastern Michigan', 'Kent State', 'Miami (OH)', 'Northern Illinois', 'Ohio', 'Toledo', 'Western Michigan', 'Air Force', 'Boise State', 'Colorado State', 'Fresno State', "Hawai'i", 'Nevada', 'New Mexico', 'San Diego State', 'San José State', 'UNLV', 'Utah State', 'Wyoming', 'Army', 'BYU', 'Liberty', 'New Mexico State', 'Notre Dame', 'UMass', 'Appalachian State', 'Arkansas State', 'Coastal Carolina', 'Georgia Southern', 'Georgia State', 'Louisiana', 'Louisiana Monroe', 'South Alabama', 'Texas State', 'Troy', 'Cincinnati', 'Connecticut', 'East Carolina', 'Houston', 'Memphis', 'Navy', 'SMU', 'South Florida', 'Temple', 'Tulane', 'Tulsa', 'UCF']
play_types = ["Rush", "Pass Completion", "Pass Incompletion", "Pass Reception", "Passing Touchdown", "Rushing Touchdown"]
success_cols = ["Rushes", "Passes", "Rush Successes", "Pass Successes", "1st Downs", "1st Successes", "2nd Downs", "2nd Successes", "3rd Downs", "3rd Successes"]

success = pd.Panel(0, items=list_teams, major_axis=success_cols, minor_axis=[a for a in range(14)])
defense_success = pd.Panel(0, items=list_teams, major_axis=success_cols, minor_axis=[a for a in range(14)])
try:
	for team in list_teams:
		for week in [a for a in range(14)]:
			response = requests.get("https://api.collegefootballdata.com/plays", params={"seasonType": "regular", "year": 2018, "defense": team, "week": week})
			print(team + " week " + str(week) + " " + str(response.status_code) + response.url)
			if response.status_code == 200:
				for play in response.json():
					if play["play_type"] in play_types:
						if play["distance"] != 0:
							if play["play_type"] == "Rush":
								success[team][week]["Rushes"] += 1
								if play["down"] == 1:
									success[team][week]["1st Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < .5:
										success[team][week]["1st Successes"] += 1
										success[team][week]["Rush Successes"] += 1
								if play["down"] == 2:
									success[team][week]["2nd Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < .7:
										success[team][week]["2nd Successes"] += 1
										success[team][week]["Rush Successes"] += 1
								if play["down"] == 3:
									success[team][week]["3rd Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < 1:
										success[team][week]["3rd Successes"] += 1
										success[team][week]["Rush Successes"] += 1

							elif play["play_type"] == "Rushing Touchdown":
								success[team][week]["Rushes"] += 1
								success[team][week]["Rush Successes"] += 1
								if play["down"] == 1:
									success[team][week]["1st Downs"] += 1
									success[team][week]["1st Successes"] += 1
								elif play["down"] == 2:
									success[team][week]["2nd Downs"] += 1
									success[team][week]["2nd Successes"] += 1
								else:
									success[team][week]["3rd Downs"] += 1
									success[team][week]["3rd Successes"] += 1

							elif play["play_type"] == "Passing Touchdown":
								success[team][week]["Passes"] += 1
								success[team][week]["Pass Successes"] += 1
								if play["down"] == 1:
									success[team][week]["1st Downs"] += 1
									success[team][week]["1st Successes"] += 1
								elif play["down"] == 2:
									success[team][week]["2nd Downs"] += 1
									success[team][week]["2nd Successes"] += 1
								else:
									success[team][week]["3rd Downs"] += 1
									success[team][week]["3rd Successes"] += 1
							else:
								success[team][week]["Passes"] += 1
								if play["down"] == 1:
									success[team][week]["1st Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < .5:
										success[team][week]["1st Successes"] += 1
										success[team][week]["Pass Successes"] += 1
								if play["down"] == 2:
									success[team][week]["2nd Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < .7:
										success[team][week]["2nd Successes"] += 1
										success[team][week]["Pass Successes"] += 1
								if play["down"] == 3:
									success[team][week]["3rd Downs"] += 1
									if (play["yards_gained"] / play["distance"]) < 1:
										success[team][week]["3rd Successes"] += 1
										success[team][week]["Pass Successes"] += 1
	success.to_excel("C:\\users\\jva12\\Documents\\CFB Poll\\Defense.xlsx")
except Exception as e:
	print(e)
	success.to_excel("C:\\users\\jva12\\Documents\\CFB Poll\\Defense.xlsx")

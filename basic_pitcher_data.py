import statsapi
from pybaseball import team_game_logs
from pybaseball import team_ids
from pybaseball import schedule_and_record
import csv


def get_batter_names(game_array):
    # Extract batter data from the game array
    line_counter = 0
    team1_batter_names = []
    team2_batter_names = []

    for i in range(len(game_array)-1):
        line = game_array[i]
        if line[0] == "-":
            line_counter += 1
            continue
            
        if line_counter == 2: # Get the batter data
            starting_num = line[0]
            halfway_index = line.find("|")
            try:  # gets batter from team 1
                starting_num = int(starting_num) # Make sure the starting number is an integer
                batter_name = line.split(' ')[1] # Get the batter name from the line
                if batter_name[-1] == ",": # Remove the comma at the end of the batter name (if there is one)
                    batter_name = batter_name[:-1]
                
                team1_batter_names.append(batter_name) # Add the batter name to the list
                # print(f"batter name = {batter_name}")
            except ValueError:
                continue

            try:  # gets batter from team 2
                half_line = line[halfway_index+2:] # Reset the line to the second half of the line
                starting_num = half_line[0]
                starting_num = int(starting_num) # Make sure the starting number is an integer
                batter_name = half_line.split(' ')[1] # Get the batter name from the line
                if batter_name[-1] == ",": # Remove the comma at the end of the batter name (if there is one)
                    batter_name = batter_name[:-1]
                
                team2_batter_names.append(batter_name) # Add the batter name to the list
                # print(f"batter name = {batter_name}")
            except ValueError:
                continue

    return [team1_batter_names, team2_batter_names] #  NEED TO GET THE BATTER NAMES FROM THE BOTH TEAMS, AM ONLY GETTING NAMES FROM ONE TEAM RIGHT NOW

            


def get_pitcher_data(game_array):
    # Extract pitcher data from the game array
    # Extract batter data from the game array
    line_counter = 0
    total_pitcher_data = []

    for i in range(len(game_array)-1):
        line = game_array[i]
        if line[0] == "-":
            line_counter += 1
            continue
            
        if line_counter == 7: # Get the pitcher data
            halfway_index = line.find("|")

            pitcher_1_name = line.split(' ')[0] # Get the 1st pitcher's name from the line
            # print(f"pitcher_1_name = {pitcher_1_name}")
            if pitcher_1_name == "":
                continue
            if pitcher_1_name[-1] == ",": # Remove the comma at the end of the pitcher's name (if there is one)
                    pitcher_1_name = pitcher_1_name[:-1]
            pitcher_1_strikeouts = line[66] # Get the pitcher strikeouts from the line
            # print(f"pitcher_1_strikeouts = {pitcher_1_strikeouts}")
            single_pitcher_data_1 = [pitcher_1_name, pitcher_1_strikeouts] # Create a list of the pitcher's name and strikeouts
            

            half_line = line[halfway_index+2:] # Reset the line to the second half of the line
            pitcher_2_name = half_line.split(' ')[0] # Get the 2nd pitcher's name from the line
            # print(f"pitcher_2_name = {pitcher_2_name}")
            if pitcher_2_name == "":
                continue
            if pitcher_2_name[-1] == ",": # Remove the comma at the end of the pitcher's name (if there is one)
                    pitcher_2_name = pitcher_2_name[:-1]
            pitcher_2_strikeouts = half_line[66] # Get the pitcher strikeouts from the line
            # print(f"pitcher_2_strikeouts = {pitcher_2_strikeouts}")
            single_pitcher_data_2 = [pitcher_2_name, pitcher_2_strikeouts] # Create a list of the pitcher's name and strikeouts
            

            return [single_pitcher_data_1, single_pitcher_data_2] # Return the list of the pitcher's name and strikeouts
            
            # total_pitcher_data.append(single_pitcher_data) 


            
    



def get_names_and_strikeouts():

    total_stats = []

    for year in range(2024, 2025):

        games = statsapi.schedule(start_date=f'04/01/{year}',end_date=f'04/01/{year}')

        # Print the game IDs
        game_ids = []

        for i in range(len(games)):
            game_ids.append(games[i]['game_id'])

        for game_id in game_ids:
            game = statsapi.boxscore(game_id, battingBox=True, battingInfo=True, fieldingInfo=True, pitchingBox=True, gameInfo=True, timecode=None)        
            
            game_array = game.split("\n")

            # Print the game array
            for i in range(len(game_array)):
                print(f"line[{i}] = {game_array[i]}")
                #print(f"game_array[{i}] = {game_array[i]}")


            batter_names = get_batter_names(game_array)
            team1_batter_names, team2_batter_names = batter_names[0], batter_names[1] # Get the batter names from the list

            pitcher_data = get_pitcher_data(game_array)

        
            pitcher_1_data, pitcher_2_data = pitcher_data[0], pitcher_data[1] # Get the pitcher data from the list

            # format is [pitcher_name, strikeouts, opposing player names, year]

            pitcher_1_total_data = [pitcher_1_data[0], pitcher_1_data[1], team2_batter_names, year]
            pitcher_2_total_data = [pitcher_2_data[0], pitcher_2_data[1], team1_batter_names, year]

            #print(F"pitcher_1_total_data = {pitcher_1_total_data}")
            #print(F"pitcher_2_total_data = {pitcher_2_total_data}")

            total_stats.append(pitcher_1_total_data)
            total_stats.append(pitcher_2_total_data)

            # print(f"\n\n")

        # Print the total stats
        # print(f"\n\n\n\ntotal_stats = {total_stats}")

    return total_stats






def add_adv_stats(total_stats):
        
    
    # Print the total stats
    # print(f"\n\n\n\ntotal_stats = {total_stats}")
    
    file_path = f"raw_betting_data/adv_pitcher_stats_5-5-25.csv"

    

    for pitcher_data in total_stats:

        pitcher_name = pitcher_data[0]
        pitcher_strikeouts = pitcher_data[1]
        opposing_batter_names = pitcher_data[2]
        pitcher_year = pitcher_data[3]

        #print(f"pitcher_name = {pitcher_name}")
        #print(f"pitcher_strikeouts = {pitcher_strikeouts}")
        #print(f"opposing_batter_names = {opposing_batter_names}")

        same_name_counter = 0 # Keeps track of how many times the same name is found in the csv file

        with open(file_path, "r") as adv_pitcher_stats_file:
            adv_pitcher_stats_data = csv.reader(adv_pitcher_stats_file, delimiter=',')    # assigns csv to a variable
            next(adv_pitcher_stats_data)  # Skips the headers

            for row in adv_pitcher_stats_data:
                chart_year = row[2]
                # print(f"row = {row}")

                full_name = row[0]
                last_name = full_name.split(", ")[0] # Get the last name from the full name

                #print(f"\npitcher_name = {pitcher_name}")
                #print(f"last_name = {last_name}")
                #print(f"chart_year = {chart_year}")
                #print(f"pitcher_year = {pitcher_year}")
                #print(f"same name == {pitcher_name == last_name}")
                #print(f"same year == {pitcher_year == chart_year}")


                if pitcher_name == last_name and pitcher_year == int(chart_year):
                    print(f"\npitcher_name = {pitcher_name} found")
                    #print(f"last_name = {last_name}")
                    #print(f"chart_year = {chart_year}")
                    #print(f"pitcher_year = {pitcher_year}")
                    #print(f"same name == {pitcher_name == last_name}")
                    #print(f"same year == {pitcher_year == chart_year}")
                    same_name_counter += 1

            print(f"same_name_counter = {same_name_counter}")
            if same_name_counter == 1: # If the name is found in the csv file only once, add the data to the list
                adv_pitcher_data = row[5:29] # MIGHT WANT TO GET THE OTHER ADVANCED STATS TOO
                print(f"name = {pitcher_name}")
                print(f"year = {pitcher_year}")
                print(f"adv_pitcher_data = {adv_pitcher_data}")

                # new format is [pitcher_name, strikeouts, opposing player names, adv_pitcher_data]
                pitcher_data.append(adv_pitcher_data)
                

    new_total_stats = []
    
    for pitcher_data in total_stats:
        if len(pitcher_data) > 4:
            new_total_stats.append(pitcher_data)  # Remove the pitcher data if it doesn't have advanced stats
        
            # print(f"last_name = {last_name}\n\n")

    return new_total_stats           
                
            



def main():

    total_stats = get_names_and_strikeouts()
    total_stats = add_adv_stats(total_stats)

    # Print the total stats
    print(f"\n\n\n\n")
    for i in range(len(total_stats)):
        print(f"pitcher {i} = {total_stats[i]}")

main()










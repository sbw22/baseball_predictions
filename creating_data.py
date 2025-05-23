import statsapi
from pybaseball import team_game_logs
from pybaseball import team_ids
from pybaseball import schedule_and_record
import csv



class Baseball_player_data:
    def __init__(self):
        pass
    


    def get_batter_names(self, game_array):
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
                except ValueError:
                    continue

        return [team1_batter_names, team2_batter_names] #  NEED TO GET THE BATTER NAMES FROM THE BOTH TEAMS, AM ONLY GETTING NAMES FROM ONE TEAM RIGHT NOW

                


    def get_pitcher_data(self, game_array):
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
                if pitcher_1_name == "":
                    continue
                if pitcher_1_name[-1] == ",": # Remove the comma at the end of the pitcher's name (if there is one)
                        pitcher_1_name = pitcher_1_name[:-1]
                pitcher_1_strikeouts = line[66] # Get the pitcher strikeouts from the line
                single_pitcher_data_1 = [pitcher_1_name, pitcher_1_strikeouts] # Create a list of the pitcher's name and strikeouts
                

                half_line = line[halfway_index+2:] # Reset the line to the second half of the line
                pitcher_2_name = half_line.split(' ')[0] # Get the 2nd pitcher's name from the line
                if pitcher_2_name == "":
                    continue
                if pitcher_2_name[-1] == ",": # Remove the comma at the end of the pitcher's name (if there is one)
                        pitcher_2_name = pitcher_2_name[:-1]
                pitcher_2_strikeouts = half_line[66] # Get the pitcher strikeouts from the line
                # print(f"pitcher_2_strikeouts = {pitcher_2_strikeouts}")
                single_pitcher_data_2 = [pitcher_2_name, pitcher_2_strikeouts] # Create a list of the pitcher's name and strikeouts
                

                return [single_pitcher_data_1, single_pitcher_data_2] # Return the list of the pitcher's name and strikeouts
                

                
        



    def get_names_and_strikeouts(self, start_month_and_day, end_month_and_day, start_year, end_year):

        total_stats = []

        curr_year = 0

        for year in range(start_year, end_year+1): # end year is the last year to check, which is why we add 1 to the end_year

            games = statsapi.schedule(start_date=f'{start_month_and_day}{year}',end_date=f'{end_month_and_day}{year}')

            # Print the game IDs
            game_ids = []

            for i in range(len(games)):
                game_ids.append(games[i]['game_id'])

            for game_id in game_ids:
                new_year = year
                if new_year != curr_year:
                    curr_year = new_year
                    print(f"curr_year = {curr_year}")

                game = statsapi.boxscore(game_id, battingBox=True, battingInfo=True, fieldingInfo=True, pitchingBox=True, gameInfo=True, timecode=None)        
                
                game_array = game.split("\n")

                # Print the game array
                #for i in range(len(game_array)):
                #    print(f"line[{i}] = {game_array[i]}")


                batter_names = self.get_batter_names(game_array)
                team1_batter_names, team2_batter_names = batter_names[0], batter_names[1] # Get the batter names from the list

                pitcher_data = self.get_pitcher_data(game_array)

            
                pitcher_1_data, pitcher_2_data = pitcher_data[0], pitcher_data[1] # Get the pitcher data from the list

                # format here is [pitcher_name, strikeouts, opposing player names, year]

                pitcher_1_total_data = [pitcher_1_data[0], pitcher_1_data[1], team2_batter_names, year]
                pitcher_2_total_data = [pitcher_2_data[0], pitcher_2_data[1], team1_batter_names, year]


                total_stats.append(pitcher_1_total_data)
                total_stats.append(pitcher_2_total_data)


        return total_stats






    def add_adv_pitcher_stats(self, total_stats):
            
        
        file_path = f"raw_betting_data/historical_and_recent_pitcher_stats_5-13-25.csv"

        

        for pitcher_data in total_stats:

            pitcher_name = pitcher_data[0]
            pitcher_strikeouts = pitcher_data[1]
            opposing_batter_names = pitcher_data[2]
            pitcher_year = pitcher_data[3]


            same_name_counter = 0 # Keeps track of how many times the same name is found in the csv file

            with open(file_path, "r") as adv_pitcher_stats_file:
                adv_pitcher_stats_data = csv.reader(adv_pitcher_stats_file, delimiter=',')    # assigns csv to a variable
                next(adv_pitcher_stats_data)  # Skips the headers

                for row in adv_pitcher_stats_data:
                    chart_year = row[2]

                    full_name = row[0]
                    last_name = full_name.split(", ")[0] # Get the last name from the full name


                    if pitcher_name == last_name and pitcher_year == int(chart_year):
                        adv_pitcher_data = row[3:] 
                        # Might want to remove the indexes for row, to see if the code later in the script is successful at removing all empty stats

                        same_name_counter += 1

                if same_name_counter == 1: # If the name is found in the csv file only once, add the data to the list
                    # new format is [pitcher_name, strikeouts, opposing batter names, year, adv_pitcher_data]
                    pitcher_data.append(adv_pitcher_data)
                    

        new_total_stats = []
        
        for pitcher_data in total_stats:
            if len(pitcher_data) > 4:
                new_total_stats.append(pitcher_data)  # Remove the pitcher data if it doesn't have advanced stats
            

        return new_total_stats           



    def add_adv_batter_stats(self, total_stats):

        
        file_path = f"raw_betting_data/historical_and_recent_batter_stats_5-13-25.csv" # CHANGE THIS TO THE CORRECT FILE PATH

        new_total_stats = []
        

        for pitcher_data in total_stats:

            batter_names = pitcher_data[2]
            batter_year = pitcher_data[3]

            new_batter_data = []

            for batter_name in batter_names:


                same_name_counter = 0 # Keeps track of how many times the same name is found in the csv file

                with open(file_path, "r") as adv_batter_stats_file:
                    adv_batter_stats_data = csv.reader(adv_batter_stats_file, delimiter=',')    # assigns csv to a variable
                    next(adv_batter_stats_data)  # Skips the headers

                    for row in adv_batter_stats_data:
                        
                        chart_year = row[2]
                        full_name = row[0]
                        last_name = full_name.split(", ")[0] # Get the last name from the full name


                        if batter_name == last_name and batter_year == int(chart_year): # If the batter name and year match the csv file
                            same_name_counter += 1
                            adv_batter_data = row[3:] 
                            batter_info = [batter_name, adv_batter_data] # Create a list of the batter's name and advanced stats

                    if same_name_counter == 1: # If the name is found in the csv file only once, add the data to the list
                        new_batter_data.append(batter_info) # Add the batter name and year to the list

                        # new format is [pitcher_name, strikeouts, year, adv_pitcher_data, opposing batter info]
                        # opposing_batter_data = [batter_name, batter_stats]

                        
            new_total_stats.append([pitcher_data[0], pitcher_data[1], pitcher_data[3], pitcher_data[4], new_batter_data]) # Move the batter names and data to the back of the list
            

        return new_total_stats


    def convert_to_float(self, total_stats):


        for i in range(len(total_stats)):
            pitcher_data = total_stats[i]
            pitcher_data[1] = float(pitcher_data[1])
            pitcher_data[2] = int(pitcher_data[2])

            for k in range(len(pitcher_data[3])):
                pitcher_data[3][k] = float(pitcher_data[3][k])

            for j in range(len(pitcher_data[4])):
                batter_info = pitcher_data[4][j]

                batter_data = batter_info[1]
                rem_counter = 0 # Keeps track of how many times an item is removed from the list
                for l in range(len(batter_data)):
                    l -= rem_counter # Adjust the index to account for the removed items
                    try: # If the index is out of range, break the loop (because we are removing from the list INSIDE the list)

                        #batter_stat = batter_data[l]
                        if total_stats[i][4][j][1][l] == "":  # skip and remove empty stats

                            total_stats[i][4][j][1].remove(total_stats[i][4][j][1][l])  # COMMENTED THIS OUT TO NOT REMOVE THE EMPTY STATS. IF I DECIDE TO START TAKING OUT EMPTY STATS AGAIN AND DEAL WITH THE IRREGULARITIES, I CAN UNCOMMENT THIS
                            # If line above is commented out, I am just skipping converting the empty stats to float
                            rem_counter += 1
                            continue
                            
                        # print(f"batter_stat = {total_stats[i][4][j][1][l]}")
                        total_stats[i][4][j][1][l] = float(total_stats[i][4][j][1][l])
                    except IndexError:
                        break


        
        return total_stats

                    
                    




    def calculate_avg_batter_stats(self, total_stats):
        # Calculate the average batter stats for each pitcher
        # This function is not implemented yet

        # Get the first stat of every batter, calculate the average, and add it to a new list
        # Repeat for every stat
        # New list will replace the entire batter data list (no more batter names, just the stats)

        new_total_stats = []
        
        '''print(f"total_stats[0]: {total_stats[0]}\n")
        print(f"total_stats[0][4]: {total_stats[0][4]}\n")
        print(f"total_stats[0][4][0]: {total_stats[0][4][0]}\n")
        print(f"total_stats[0][4][0][1]: {total_stats[0][4][0][1]}\n")'''

        # total_stats[0] = [pitcher_name, strikeouts, year, adv_pitcher_data, batter_info]
        # pitcher_name[4] = [batter_1, batter_2, batter_3, . . .]
        # batter_stats[1]


        for pitcher_info in total_stats:

            if pitcher_info[4] == [] or pitcher_info[4][0] == [] or pitcher_info[4][0][1] == []: # If there are no batters, skip the pitcher
                continue

            if len(pitcher_info[4]) < 1:
                continue

            # print(f"length of total_stats[0][4][0][1]: {len(total_stats[0][4][0][1])}")


            new_total_batter_info = []

            skip_pitcher = False

            # pitcher_info = total_stats[i]
            for i in range(len(total_stats[0][4][0][1])): # Uses the length of the first batter's stats to determine how many stats there are

                batter_list = pitcher_info[4]
            
                new_batter_data = []

                # if i == 70 or i == 137: Skips columns where data is empty. Not using it right now because different rows have different indexes for their columns
                #   continue

                # Get the first stat of every batter, calculate the average, and add it to a new list
                # Repeat for every stat

                summed_batter_data = 0.0

                # for batter in batter_list:

                # ind_batter_info = total_stats[i][4][i]
                for ind_batter_info in batter_list:
                    
                    # j = ind_batter_info
                    #ind_batter_data = total_stats[i][4][j][1]
                    ind_batter_data = ind_batter_info[1]
                    if i < len(ind_batter_data):  # Check if the stat exists for this batter
                        # This if statement is here because some batters have less stats than others. This is kind of a bandaid fix, but it works. Might want to find the true cause of the problem later
                        single_ind_batter_data = ind_batter_data[i]

                        if single_ind_batter_data == "":  # skip empty stats
                            continue

                        new_batter_data.append(single_ind_batter_data)


                if len(new_batter_data) == 0:  # If there are no stats for this batter, skip the pitcher entirely (might want to remove this later)
                    skip_pitcher = True
                    break

                for stat in new_batter_data:
                    summed_batter_data += stat 

                averaged_batter_data = summed_batter_data / len(new_batter_data)

                new_total_batter_info.append(averaged_batter_data)
                
            if skip_pitcher:  # If there are no stats for this batter, skip the pitcher entirely
                continue
            
            #print(f"pitcher name: {pitcher_info[0]}")
            #print(f"new_total_batter_info: {new_total_batter_info}, length = {len(new_total_batter_info)}\n")

            new_total_stats.append([pitcher_info[0], pitcher_info[1], pitcher_info[2], pitcher_info[3], new_total_batter_info]) # Add the new batter data to the pitcher data, while removing old data
        

            # break


        return new_total_stats


    def write_to_csv(self, total_stats):
        # Write the total stats to a csv file
        with open("created_data/created_total_stats.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Pitcher Name", "Strikeouts", "Year", "Advanced Pitcher Data", "Batter Data"])
            for pitcher_data in total_stats:
                writer.writerow(pitcher_data)
    
        

    

def main():

    historic_player_data = Baseball_player_data()  # Create an instance of the baseball_player_data class

    start_month_and_day = "06/01/"
    end_month_and_day = "07/01/"
    start_year = 2016
    end_year = 2024

    total_stats = historic_player_data.get_names_and_strikeouts(start_month_and_day, end_month_and_day, start_year, end_year)  # Gets names and strikouts from pitchers, and names from batters
    total_stats = historic_player_data.add_adv_pitcher_stats(total_stats)  # Adds advanced stats to the pitcher data
    total_stats = historic_player_data.add_adv_batter_stats(total_stats)  # Adds advanced stats to the batter data
    total_stats = historic_player_data.convert_to_float(total_stats)  # Converts the stats to float
    total_stats = historic_player_data.calculate_avg_batter_stats(total_stats)  # Calculates the average batter stats for each pitcher

    historic_player_data.write_to_csv(total_stats)  # Writes the total stats to a csv file
    # format is [pitcher_name, strikeouts, year, adv_pitcher_data, batter_info]

    
    # Print the total stats
    print(f"\n\n\n\n")
    # print(f"total_stats = {total_stats}")

    
    for pitcher_data in total_stats:
        #batter_data = pitcher_data[4]
        #print(f"pitcher_data = {pitcher_data}")
                
        # print(f"pitcher {i} = {pitcher_data}")
        break

    #print(f"\n\n\n\n {total_stats}")



    return  

if __name__ == "__main__":
     main()
         

import pandas as pd
import ast
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr



def load_data():
    pitcher_file_path = "raw_betting_data/historical_and_recent_pitcher_stats_5-13-25.csv"
    batter_file_path = "raw_betting_data/historical_and_recent_batter_stats_5-13-25.csv"

    # pitcher_file_path = "raw_betting_data/all_pitchers_6-5-25.csv"
    # batter_file_path = "raw_betting_data/all_batters_6-4-25.csv"

    # Load the data
    raw_pitcher_data = pd.read_csv(pitcher_file_path)
    raw_batter_data = pd.read_csv(batter_file_path)
    created_total_stats = pd.read_csv("created_data/created_total_stats.csv")

    # print(f"{raw_pitcher_data}")
    print(f"{raw_pitcher_data}")
    # print(f"Batter data shape: {batter_data}")

    return raw_pitcher_data, raw_batter_data, created_total_stats

    # Calculate correlations
    # correlations = calculate_correlations(pitcher_data, batter_data)

    # Save the results
    # save_results(correlations, "output/correlations.csv")

def get_avg_so(raw_pitcher_data, created_total_stats):
        
    total_pitcher_data = []

    for i in range(len(raw_pitcher_data)):

        # Get pitcher name
        raw_pitcher_name = raw_pitcher_data.iloc[i, 0]
        raw_pitcher_last_name = raw_pitcher_name.split(" ")[0][:-1] # Gets the last name of the pitcher (takes out the comma at the end of the last name)
        raw_year = raw_pitcher_data.iloc[i, 2]

        
        game_counter = 0
        total_strikeouts = 0

        for k in range(len(created_total_stats)):  # Loop through the created total stats to find the matching pitcher. Gathers the total # of strikeouts.
            new_last_name = created_total_stats.iloc[k, 0]
            new_year = created_total_stats.iloc[k, 2]

            if raw_pitcher_last_name == new_last_name and raw_year == new_year: # If the last names and years match, we have found the pitcher. Add the strikeouts to the total.
                game_counter += 1
                total_strikeouts += float(created_total_stats.iloc[k, 1])
                # print(f"{created_total_stats.iloc[k, 0]}, {created_total_stats.iloc[k, 1]} strikeouts")
                

        # print(f"Pitcher: {raw_pitcher_name}, last name: {raw_pitcher_last_name}")

        if game_counter == 0:
            # print(f"Error: No games found for pitcher {raw_pitcher_name}")
            continue
        else:
            avg_strikeouts = total_strikeouts / game_counter

            pitcher_data = []

            pitcher_data.extend([float(stat) for stat in raw_pitcher_data.iloc[i, 3:]])  # Get all the stats for the pitcher. Starts from the 4th column (index 3) to the end of the row.
            
            # pitcher_data = raw_pitcher_data.iloc[i, 3]  # Get the pitcher data for the current pitcher

            # print(f"Pitcher data: {pitcher_data}, type: {type(pitcher_data)}")

            # Add total pitcher data to the new pitcher data list
            new_single_pitcher_data = [raw_pitcher_name, avg_strikeouts, pitcher_data]  # Pitcher name
            
            total_pitcher_data.append(new_single_pitcher_data)  # Append the new pitcher data to the total pitcher data list

            # Add the average strikeouts to the raw pitcher data
            # raw_pitcher_data.at[i, 'avg_strikeouts'] = avg_strikeouts

            # Print the updated row
            # print(raw_pitcher_data.iloc[i])

        

    return total_pitcher_data



def calculate_correlations(pitcher_data, batter_data, pitcher_stat_titles, batter_stat_titles):

    avg_so_list = [data[1] for data in pitcher_data]  # Extract average strikeouts from each pitcher's data

    corr_list = []  # List to hold the correlation coefficients

    for i in range(len(pitcher_data)):

        try:
            pitcher_stat_title = pitcher_stat_titles[i + 3]  # Get the stat title from the batter data (skipping the first column which is the name)
        except IndexError:
            break  # If the index is out of range, break the loop


        '''if i != 9 and i != 15: # Finds the correlation of a random stat that I picked. Change this to the stat you want to analyze.
            continue'''

        stat_list = [data[2][i] for data in pitcher_data]  # Extract the stats for the current stat index

        r = np.corrcoef(avg_so_list, stat_list)[0, 1]

        corr_list.append([r, pitcher_stat_title])  # Append the correlation coefficient to the list

        # Plot data
        plt.figure(figsize=(10, 6))
        plt.plot(avg_so_list, stat_list, marker='o', color='darkorange', linestyle='-')
        plt.title(f'Average Strikeouts vs. {pitcher_stat_title}')
        plt.xlabel('Average Strikeouts')
        plt.ylabel(f'{pitcher_stat_title}')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        
        # Add correlation text in top-left corner of plot
        plt.text(0.05, 0.95, f'r = {r:.3f}', transform=plt.gca().transAxes,
                fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

        plt.tight_layout()
        #  plt.show()

        # plt.scatter(x, y, label=f"r = {corr_coef:.2f}")

    sorted_corr_list = sorted(corr_list, key=lambda x: abs(x[0]), reverse=True)  # Sort the correlation list in descending order

    print(f"Correlation coefficients from greatest to least:")
    for corr, title in sorted_corr_list:
        print(f"{title}: {corr:.3f}")  # Print the correlation coefficient and the stat title





def main():

    # STEPS FOR CALCULATING CORRALATION FOR A PITCHER'S STRIKEOUTS
    # 1) Find the average strikeout count of all games for a year.
    # 2) Find correlation of average strikeout count to every stat for that pitcher for that year. 

    # Desired list shape: [pitcher_name, avg_strikeouts, [stat_1, stat_2, stat_3, ...]]

    raw_pitcher_data, raw_batter_data, created_total_stats = load_data()

    pitcher_stat_titles = raw_pitcher_data.columns.tolist()  # Get the stat titles from the first row of the CSV file
    batter_stat_titles = raw_batter_data.columns.tolist()  # Get the stat titles from the first row of the CSV file

    print(f"Stat titles: {pitcher_stat_titles}, length = {len(pitcher_stat_titles)}")
    print(f"Stat titles: {batter_stat_titles}, length = {len(batter_stat_titles)}")

    data_point = float(raw_pitcher_data.iloc[0, 7])
    list_of_stat_one = raw_pitcher_data.iloc[0:, 1].tolist()

    print(f"number of stats = {len(raw_pitcher_data.iloc[1])}")

    # print(f"data pitcher data: {data_point}, type = {type(data_point)}")
    # print(f"list of stat one: {list_of_stat_one}, len: {len(list_of_stat_one)}")

    # print(f"created_total_stats type: {type(ast.literal_eval(created_total_stats.iloc[0, 3])), ast.literal_eval(created_total_stats.iloc[0, 3])}")

    total_pitcher_data = get_avg_so(raw_pitcher_data, created_total_stats)  # total_pitcher data is a list of lists, where each list is a pitcher, their average strikeouts, and their stats

    print(f"After total_pitcher_data: {len(total_pitcher_data)} pitchers found")

    calculate_correlations(total_pitcher_data, raw_batter_data, pitcher_stat_titles, batter_stat_titles)  # Calculate the correlations between the average strikeouts and each stat for each pitcher


if __name__ == "__main__":
    main()
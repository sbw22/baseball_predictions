import pandas as pd



def load_data():
    pitcher_file_path = "raw_betting_data/historical_and_recent_pitcher_stats_5-13-25.csv"
    batter_file_path = "raw_betting_data/historical_and_recent_batter_stats_5-13-25.csv"

    # Load the data
    pitcher_data = pd.read_csv(pitcher_file_path)
    batter_data = pd.read_csv(batter_file_path)

    print(f"Pitcher data shape: {pitcher_data}")
    # print(f"Batter data shape: {batter_data}")

    return pitcher_data, batter_data

    # Calculate correlations
    # correlations = calculate_correlations(pitcher_data, batter_data)

    # Save the results
    # save_results(correlations, "output/correlations.csv")


def main():

    pitcher_data, batter_data = load_data()

    data_point = pitcher_data.iloc[0, 0]

    print(f"data pitcher data: {data_point}")


    


if __name__ == "__main__":
    main()
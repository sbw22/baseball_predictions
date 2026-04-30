import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

class ResultsMetrics:
    def __init__(self):
        pass

    def print_and_save_results(self, rounded_guesses, scaled_up_guesses, scaled_up_actual_strikeouts):

        avg_error = 0.0
        match_counter = 0
        within_one = 0
        within_two = 0
        within_three = 0
        within_four = 0
        within_five = 0
        within_six = 0

        total_num_of_so = [0,0,0,0,0,0,0,0,0,0]

        correct_actual_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        correct_guess_num_of_so = [0,0,0,0,0,0,0,0,0,0]

        actual_0 = 0
        actual_1 = 0
        actual_2 = 0
        actual_3 = 0
        actual_4 = 0
        actual_5 = 0
        actual_6 = 0
        actual_7 = 0
        actual_8 = 0
        actual_9 = 0

        guess_0 = 0
        guess_1 = 0
        guess_2 = 0
        guess_3 = 0
        guess_4 = 0
        guess_5 = 0
        guess_6 = 0
        guess_7 = 0
        guess_8 = 0
        guess_9 = 0
        

        actual_within_1_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        actual_within_2_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        actual_within_3_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        actual_within_4_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        actual_within_5_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        actual_within_6_num_of_so = [0,0,0,0,0,0,0,0,0,0]

        guess_within_1_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        guess_within_2_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        guess_within_3_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        guess_within_4_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        guess_within_5_num_of_so = [0,0,0,0,0,0,0,0,0,0]
        guess_within_6_num_of_so = [0,0,0,0,0,0,0,0,0,0]

        '''correct_on_1 = 0
        correct_on_2 = 0
        correct_on_3 = 0
        correct_on_4 = 0
        correct_on_5 = 0
        correct_on_6 = 0
        correct_on_7 = 0
        correct_on_8 = 0
        correct_on_9 = 0'''

        master_actual_normal_count = [actual_0, actual_1, actual_2, actual_3, actual_4, actual_5, actual_6, actual_7, actual_8, actual_9]
        master_guess_normal_count = [guess_0, guess_1, guess_2, guess_3, guess_4, guess_5, guess_6, guess_7, guess_8, guess_9]
        # I'm keeping correct_num_of_so in both master lists, idk if I should do that, guess we'll see
        master_actual_num_of_so = [correct_actual_num_of_so, actual_within_1_num_of_so, actual_within_2_num_of_so, actual_within_3_num_of_so, actual_within_4_num_of_so, actual_within_5_num_of_so, actual_within_6_num_of_so]
        master_guess_num_of_so = [correct_guess_num_of_so, guess_within_1_num_of_so, guess_within_2_num_of_so, guess_within_3_num_of_so, guess_within_4_num_of_so, guess_within_5_num_of_so, guess_within_6_num_of_so]

        for i in range(len(rounded_guesses)):
            guess = round(rounded_guesses[i].item(), 2)
            actual = round(scaled_up_actual_strikeouts[i].item(), 2)

            avg_error += abs(guess - actual)

            try:  # I think this part of the code is throwing an error (especially second line) because the guess is -0.0 or 10 (something less than 0 or greater than 9)
                master_actual_normal_count[int(actual)] += 1
                master_guess_normal_count[int(guess)] += 1
            except:
                continue

            match_counter += 1 if guess == actual else 0
            within_one += 1 if abs(guess - actual) <= 1 else 0
            within_two += 1 if abs(guess - actual) <= 2 else 0
            within_three += 1 if abs(guess - actual) <= 3 else 0
            within_four += 1 if abs(guess - actual) <= 4 else 0
            within_five += 1 if abs(guess - actual) <= 5 else 0
            within_six += 1 if abs(guess - actual) <= 6 else 0

            # Don't know if this is right, but it may not matter anyway?
            total_num_of_so[int(actual)] += 1

            correct_actual_num_of_so[int(actual)] += 1 if guess == actual else 0
            actual_within_1_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 1 else 0
            actual_within_2_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 2 else 0
            actual_within_3_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 3 else 0
            actual_within_4_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 4 else 0
            actual_within_5_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 5 else 0
            actual_within_6_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 6 else 0

            correct_guess_num_of_so[int(guess)] += 1 if guess == actual else 0
            guess_within_1_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 1 else 0
            guess_within_2_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 2 else 0
            guess_within_3_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 3 else 0
            guess_within_4_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 4 else 0
            guess_within_5_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 5 else 0
            guess_within_6_num_of_so[int(guess)] += 1 if abs(guess - actual) <= 6 else 0

            


            print(f"Predicted strikeouts: {guess}")
            print(f"Actual strikeouts: {actual}\n")



        # Calculate percent correct of guesses in each category
        
        for within_n, num_of_so in enumerate(master_guess_num_of_so):

            for i in range(len(num_of_so)):

                # Loop that finds the number of actual strikeouts that are n distance away from the guess

                # within_n = master_guess_num_of_so.index(num_of_so)
                total_actual_strikeouts = 0
                bottom_edge = i - within_n # Bottom/top edge is the actual number of strikeouts n distance away from the guess
                top_edge = i + within_n # For example, if the guess is 5 and within_n is 2, the bottom edge is 3 and the top edge is 7
                # We get within_n from the index of the num_of_so list, which is the number of strikeouts that are within n distance from the guess

                if within_n != 0: # We don't need to do this for perfect guesses
                    for j in range(bottom_edge, top_edge + 1):
                        if j < 0 or j > 9:   # If the index is negative, we skip it
                            continue

                        # total_actual_strikeouts += num_of_so[j]
                        # print(f"j = {j}")
                        # total_actual_strikeouts += master_actual_normal_count[j]
                        total_actual_strikeouts += master_guess_normal_count[j]


                        '''if abs(j - i) <= within_n: # If the index is within n distance from the guess, we add it to the count
                        total_actual_strikeouts += num_of_so[j]'''
                    # print(f"\n")
                else:
                    # total_actual_strikeouts = master_actual_normal_count[i]
                    total_actual_strikeouts = master_guess_normal_count[i]
                    # rint(f"\n")
                
                # Where I am trying to impliment the below list, might delete later
                total_actual_strikeouts = master_guess_normal_count[i]
            
                print(f"\n")

                new_percent = 0.0
                if total_actual_strikeouts > 0:
                    new_percent = round(num_of_so[i] / total_actual_strikeouts * 100, 2)

                else:
                    new_percent = -1.0
                num_of_so[i] = [num_of_so[i], new_percent]
        
        for i, item in enumerate(master_guess_normal_count):
            print(f"Guesses for {i} strikeouts: {item}")
        
        
        # Trying to predict:
        # If I predict x amount of strikeouts, what is the probability that the guess is within n distance of the actual strikeouts?
        # Need to find the total amount of guesses that I make for each number of strikeouts
        # guesses within n distance / total guesses for that number of strikeouts



        avg_error /= len(rounded_guesses)

        print(f"Average error: {avg_error:.2f}\n")

        print(f"Perfect guesses: {match_counter} out of {len(rounded_guesses)} -- {match_counter / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within one strikeout: {within_one} out of {len(rounded_guesses)} -- {within_one / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within two strikeouts: {within_two} out of {len(rounded_guesses)} -- {within_two / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within three strikeouts: {within_three} out of {len(rounded_guesses)} -- {within_three / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within four strikeouts: {within_four} out of {len(rounded_guesses)} -- {within_four / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within five strikeouts: {within_five} out of {len(rounded_guesses)} -- {within_five / len(rounded_guesses) * 100:.2f}%\n")
        print(f"Within six strikeouts: {within_six} out of {len(rounded_guesses)} -- {within_six / len(rounded_guesses) * 100:.2f}%\n\n")

        
        
        '''for i in range(10):
            try:
                print(f"Correct guesses for {i} strikeouts: {correct_num_of_so[i][0]} out of {total_num_of_so[i]} -- {correct_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")

            except ZeroDivisionError:
                print(f"Correct guesses for {i} strikeouts: {correct_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

            try:
                print(f"Within 1 strikeouts for {i} strikeouts: {within_1_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_1_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 1 strikeouts for {i} strikeouts: {within_1_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

            try:
                print(f"Within 2 strikeouts for {i} strikeouts: {within_2_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_2_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 2 strikeouts for {i} strikeouts: {within_2_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

            try:
                print(f"Within 3 strikeouts for {i} strikeouts: {within_3_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_3_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 3 strikeouts for {i} strikeouts: {within_3_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
            try:
                print(f"Within 4 strikeouts for {i} strikeouts: {within_4_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_4_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 4 strikeouts for {i} strikeouts: {within_4_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
            try:
                print(f"Within 5 strikeouts for {i} strikeouts: {within_5_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_5_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 5 strikeouts for {i} strikeouts: {within_5_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
            try:
                print(f"Within 6 strikeouts for {i} strikeouts: {within_6_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_6_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
            except ZeroDivisionError:
                print(f"Within 6 strikeouts for {i} strikeouts: {within_6_num_of_so[i]} out of {total_num_of_so[i]} -- 0.00%\n")'''


        # import above data to a csv file
        with open('prediction_stats/strikeout_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['actual_strikeouts', 'total_guesses', 'correct_guesses', 'within_1', 'within_2', 'within_3', 'within_4', 'within_5', 'within_6']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(10):
                try:
                    writer.writerow({
                        'actual_strikeouts': i,
                        'total_guesses': total_num_of_so[i],
                        'correct_guesses': correct_guess_num_of_so[i][0],
                        'within_1': guess_within_1_num_of_so[i][0],
                        'within_2': guess_within_2_num_of_so[i][0],
                        'within_3': guess_within_3_num_of_so[i][0],
                        'within_4': guess_within_4_num_of_so[i][0],
                        'within_5': guess_within_5_num_of_so[i][0],
                        'within_6': guess_within_6_num_of_so[i][0]
                    })
                except ZeroDivisionError:
                    writer.writerow({
                        'actual_strikeouts': i,
                        'total_guesses': 0,
                        'correct_guesses': 0,
                        'within_1': 0,
                        'within_2': 0,
                        'within_3': 0,
                        'within_4': 0,
                        'within_5': 0,
                        'within_6': 0
                    })
            
            # Write another row with the fieldnames
            writer.writerow({})

            writer.writerow({
                'actual_strikeouts': 'actual_strikeouts - percentages',
                'total_guesses': 'total_guesses',
                'correct_guesses': 'correct_guesses',
                'within_1': 'within_1',
                'within_2': 'within_2',
                'within_3': 'within_3',
                'within_4': 'within_4',
                'within_5': 'within_5',
                'within_6': 'within_6'
            })

            for i in range(10):
                try:
                    writer.writerow({
                        'actual_strikeouts': i,
                        'total_guesses': total_num_of_so[i],
                        'correct_guesses': f'{correct_guess_num_of_so[i][1]} + %',
                        'within_1': f'{guess_within_1_num_of_so[i][1]} + %',
                        'within_2': f'{guess_within_2_num_of_so[i][1]} + %',
                        'within_3': f'{guess_within_3_num_of_so[i][1]} + %',
                        'within_4': f'{guess_within_4_num_of_so[i][1]} + %',
                        'within_5': f'{guess_within_5_num_of_so[i][1]} + %',
                        'within_6': f'{guess_within_6_num_of_so[i][1]} + %'
                    })
                except ZeroDivisionError:
                    writer.writerow({
                        'actual_strikeouts': i,
                        'total_guesses': '0.0 %',
                        'correct_guesses': '0.0 %',
                        'within_1': '0.0 %',
                        'within_2': '0.0 %',
                        'within_3': '0.0 %',
                        'within_4': '0.0 %',
                        'within_5': '0.0 %',
                        'within_6': '0.0 %'
                    })



        '''# Print the confusion matrix
        cm = confusion_matrix(scaled_up_actual_strikeouts, rounded_guesses)
        plt.figure(figsize=(10, 7))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()
        tick_marks = np.arange(10)
        plt.xticks(tick_marks, range(10))
        plt.yticks(tick_marks, range(10))
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig('prediction_stats/confusion_matrix.png')
        plt.show()'''


        # --- Heatmap for counts ---
        counts_matrix = np.array([
            [correct_guess_num_of_so[i][0], guess_within_1_num_of_so[i][0], guess_within_2_num_of_so[i][0], guess_within_3_num_of_so[i][0],
            guess_within_4_num_of_so[i][0], guess_within_5_num_of_so[i][0], guess_within_6_num_of_so[i][0]]
            for i in range(10)
        ])
        plt.figure(figsize=(10, 7))
        plt.imshow(counts_matrix, cmap='coolwarm', aspect='auto', vmin=0, vmax=np.max(counts_matrix))
        plt.colorbar(label='Count')
        plt.xticks(range(7), ['Exact', 'Within 1', 'Within 2', 'Within 3', 'Within 4', 'Within 5', 'Within 6'])
        plt.yticks(range(10), [str(i) for i in range(10)])
        for i in range(counts_matrix.shape[0]):
            for j in range(counts_matrix.shape[1]):
                plt.text(j, i, counts_matrix[i, j], ha='center', va='center', color='black', fontsize=10, alpha=0.8)
        plt.title('Strikeout Prediction Counts Heatmap')
        plt.xlabel('Prediction Accuracy')
        plt.ylabel('Actual Strikeouts')
        plt.tight_layout()
        plt.savefig('prediction_stats/strikeout_counts_heatmap.png', dpi=200)
        plt.close()

        # --- Heatmap for percentages ---
        percent_matrix = np.array([
            [correct_guess_num_of_so[i][1], guess_within_1_num_of_so[i][1], guess_within_2_num_of_so[i][1], guess_within_3_num_of_so[i][1],
            guess_within_4_num_of_so[i][1], guess_within_5_num_of_so[i][1], guess_within_6_num_of_so[i][1]]
            for i in range(10)
        ])
        plt.figure(figsize=(10, 7))
        plt.imshow(percent_matrix, cmap='coolwarm', aspect='auto', vmin=0, vmax=100)
        plt.colorbar(label='Percent')
        plt.xticks(range(7), ['Exact', 'Within 1', 'Within 2', 'Within 3', 'Within 4', 'Within 5', 'Within 6'])
        plt.yticks(range(10), [str(i) for i in range(10)])
        for i in range(percent_matrix.shape[0]):
            for j in range(percent_matrix.shape[1]):
                plt.text(j, i, f"{percent_matrix[i, j]:.1f}%", ha='center', va='center', color='black', fontsize=10, alpha=0.8)
        plt.title('Strikeout Prediction Percentages Heatmap')
        plt.xlabel('Prediction Accuracy')
        plt.ylabel('Actual Strikeouts')
        plt.tight_layout()
        plt.savefig('prediction_stats/strikeout_percentages_heatmap.png', dpi=200)
        plt.close()

        # --- Heatmap for percentages of predictions ---

        return
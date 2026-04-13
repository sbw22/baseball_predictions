def main():
    # Graph the progress I have made in sports betting
    # Graph the progress of my model's predictions over time
    total_current_money = [88, 94, 88, 86, 86, 79, 80]
    days = ["3/27/26", "3/28/26", "3/29/26", "3/30/26", "4/1/26", "4/2/26", "4/11/26"]

    # Graph the progress
    import matplotlib.pyplot as plt
    plt.plot(days, total_current_money)
    plt.xlabel('Date')
    plt.ylabel('Total Money')
    plt.title('Progress of Sports Betting')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

import statsapi

# Data
odds = [-500, -450, -400, -366, -333, -300, -275, -250, -225, -200, -150, -130, -120, -110, -105, 100, 110, 120, 150, 200]
breakeven_percentages = [83.33, 81.82, 80.00, 78.54, 76.91, 75.00, 73.33, 71.43, 69.23, 66.67, 60.00, 56.52, 54.55, 52.38, 51.22, 50.00, 47.62, 45.45, 40.00, 33.33]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(odds, breakeven_percentages, marker='o', color='darkorange', linestyle='-')
plt.title('Breakeven Win Percentage vs. American Odds')
plt.xlabel('American Odds')
plt.ylabel('Breakeven Win Percentage (%)')
plt.axhline(52.38, color='gray', linestyle='--', label='Standard -110 Breakeven (52.38%)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()


plt.scatter(x, y, label=f"r = {corr_coef:.2f}")
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("nonblack_pixels.csv")

# Plotting coordinate pairs from columns "X" and "Y"
plt.figure(figsize=(8, 6))
plt.scatter(df['X'], df['Y'], color='blue', marker='.')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of Coordinates')
plt.grid(True)
plt.show()
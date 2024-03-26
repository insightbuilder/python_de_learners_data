
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('data.csv')

# Select columns for the line chart
selected_columns = ['column1', 'column2']

# Plot the line chart
df[selected_columns].plot(x=df.index, y=selected_columns, kind='line')
plt.xlabel('Index')
plt.ylabel('Values')
plt.title('Line Chart')
plt.legend(selected_columns)
plt.show()

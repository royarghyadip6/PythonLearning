import pandas as pd

# Create a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

df  = pd.DataFrame(data)
print("DataFrame:\n", df)

# Perform basic operations on the DataFrame
# 1. Display the first few rows
print("\nFirst few rows:\n", df.head())
# 2. Get summary statistics
print("\nSummary statistics:\n", df.describe())
# 3. Filter rows based on a condition
filtered_df = df[df['Age'] > 28]
print("\nFiltered DataFrame (Age > 28):\n", filtered_df)
# 4. Add a new column
df['Age in 5 Years'] = df['Age'] + 5
print("\nDataFrame with new column:\n", df)
# 5. Save the DataFrame to a CSV file
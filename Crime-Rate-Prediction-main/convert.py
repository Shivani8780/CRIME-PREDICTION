import pandas as pd

# Define the file paths
excel_file_path = 'Dataset/new_dataset.xlsx'  # Path to your Excel file
csv_file_path = 'Dataset/output2.csv'      # Path to save the output CSV file

# Read the Excel file (first sheet by default)
df = pd.read_excel(excel_file_path)

# Save the DataFrame as a CSV file
df.to_csv(csv_file_path, index=False)

print(f"Excel file '{excel_file_path}' has been converted to CSV file '{csv_file_path}'")

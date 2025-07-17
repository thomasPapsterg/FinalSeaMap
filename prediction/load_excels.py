import pandas as pd
import os

folder_path = "D:/MHNIAIES_METRHSEIS_2014_2019"
excel_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

all_data = []

for file in excel_files:
    full_path = os.path.join(folder_path, file)
    all_sheets = pd.read_excel(full_path, sheet_name=None)
    all_sheets.pop("INFO", None)

    for sheet_name, df in all_sheets.items():
        df["source_file"] = file
        df["month"] = sheet_name
        all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Προβολή
print(combined_df.head())
print("Σύνολο γραμμών:", len(combined_df))
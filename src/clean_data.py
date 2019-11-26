# Script to clean column names

import pandas as pd

df = pd.read_csv("data/WHO_life_expectancy_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace("  ", " ").str.replace(" ", "_").str.replace("-", "_")
df.to_csv("data/WHO_life_expectancy_data_clean.csv")


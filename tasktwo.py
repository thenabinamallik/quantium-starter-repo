import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Load all CSV files
# -----------------------------
DATA_DIR = Path("data")

dfs = []
for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# -----------------------------
# 2. DEBUG: confirm columns
# -----------------------------
print("Columns found:", combined_df.columns.tolist())

# -----------------------------
# 3. Normalize product column
# -----------------------------
combined_df["product"] = (
    combined_df["product"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# -----------------------------
# 4. Clean quantity column
# -----------------------------
combined_df["quantity"] = (
    combined_df["quantity"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+\.?\d*)")[0]
)

combined_df["quantity"] = pd.to_numeric(
    combined_df["quantity"], errors="coerce"
)

# -----------------------------
# 5. Clean price column
# -----------------------------
combined_df["price"] = (
    combined_df["price"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+\.?\d*)")[0]
)

combined_df["price"] = pd.to_numeric(
    combined_df["price"], errors="coerce"
)

# -----------------------------
# 6. Filter only Pink Morsels
# -----------------------------
pink_df = combined_df[
    combined_df["product"].str.contains("pink", na=False)
]

# -----------------------------
# 7. Calculate Sales (FORCED)
# -----------------------------
pink_df["Sales"] = pink_df["quantity"].fillna(0) * pink_df["price"].fillna(0)

# -----------------------------
# 8. Final required columns
# -----------------------------
final_df = pink_df[["Sales", "date", "region"]].rename(
    columns={
        "date": "Date",
        "region": "Region"
    }
)

# -----------------------------
# 9. Export output
# -----------------------------
final_df.to_csv("tasktwo_output.csv", index=False)

print("✅ Rows written:", len(final_df))
print(final_df.head())

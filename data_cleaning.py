import pandas as pd
import numpy as np

# --------------------------------
# 1. Load dataset
# --------------------------------

df = pd.read_csv("myntra_1500_products.csv")

print("Original shape:", df.shape)

# --------------------------------
# 2. Remove duplicate products
# --------------------------------

df = df.drop_duplicates(
    subset=["brand", "product_name"]
)

# --------------------------------
# 3. Clean Price
# --------------------------------

df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("Rs.", "", regex=False)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

# --------------------------------
# 4. Clean Original Price
# --------------------------------

df["original_price"] = (
    df["original_price"]
    .astype(str)
    .str.replace("Rs.", "", regex=False)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["original_price"] = pd.to_numeric(
    df["original_price"],
    errors="coerce"
)

# --------------------------------
# 5. Clean Discount
# --------------------------------

df["discount"] = (
    df["discount"]
    .astype(str)
    .str.extract(r"(\d+)")
)

df["discount"] = pd.to_numeric(
    df["discount"],
    errors="coerce"
)

# --------------------------------
# 6. Clean Rating
# --------------------------------

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

# --------------------------------
# 7. Clean Reviews
# --------------------------------

df["reviews"] = pd.to_numeric(
    df["reviews"],
    errors="coerce"
)

# --------------------------------
# 8. Handle missing values
# --------------------------------

df["rating"] = df["rating"].fillna(
    df["rating"].median()
)

df["reviews"] = df["reviews"].fillna(0)

# Price missing rows
df = df.dropna(
    subset=["price"]
)

# --------------------------------
# 9. Create Discount Amount
# --------------------------------

df["discount_amount"] = (
    df["original_price"] - df["price"]
)

# --------------------------------
# 10. Create Price Segment
# --------------------------------

df["price_segment"] = pd.cut(
    df["price"],
    bins=[0, 500, 1000, 2000, 5000, np.inf],
    labels=[
        "Under 500",
        "500-1000",
        "1000-2000",
        "2000-5000",
        "5000+"
    ]
)

# --------------------------------
# 11. Check dataset
# --------------------------------

print("\nCleaned shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)

print("\nFirst 10 rows:")
print(df.head(10))

# --------------------------------
# 12. Save cleaned dataset
# --------------------------------

df.to_csv(
    "myntra_cleaned.csv",
    index=False
)

print("\nSaved: myntra_cleaned.csv")
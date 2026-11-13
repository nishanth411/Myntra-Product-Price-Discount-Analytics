import pandas as pd
import numpy as np

print("\n========== EDA ==========")


# --------------------------------
# 1. Load dataset
# --------------------------------

df = pd.read_csv("myntra_cleaned.csv")

print("Original shape:", df.shape)

print("\nAverage Price:")
print(df["price"].mean())

print("\nAverage Discount:")
print(df["discount"].mean())

print("\nAverage Rating:")
print(df["rating"].mean())

print("\nTotal Products:")
print(len(df))

print("\nTop Brands:")
print(
    df["brand"]
    .value_counts()
    .head(10)
)

print("\nAverage Price by Brand:")
print(
    df.groupby("brand")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\nAverage Discount by Brand:")
print(
    df.groupby("brand")["discount"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
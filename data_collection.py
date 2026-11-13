from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# -----------------------------------
# SETTINGS
# -----------------------------------

BASE_URL = "https://www.myntra.com/men-tshirts"

TARGET_PRODUCTS = 1500

# -----------------------------------
# CHROME SETUP
# -----------------------------------

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# -----------------------------------
# STORAGE
# -----------------------------------

all_products = []

page = 1

# -----------------------------------
# SCRAPING
# -----------------------------------

while len(all_products) < TARGET_PRODUCTS:

    print(f"\nScraping Page {page}...")

    url = f"{BASE_URL}?p={page}"

    driver.get(url)

    # Wait for products
    time.sleep(4)

    soup = BeautifulSoup(
        driver.page_source,
        "html.parser"
    )

    products = soup.find_all(
        "li",
        class_="product-base"
    )

    print(
        "Products found:",
        len(products)
    )

    # Stop if page has no products
    if len(products) == 0:
        print("No more products found.")
        break

    # -----------------------------------
    # EXTRACT PRODUCTS
    # -----------------------------------

    for product in products:

        # Brand
        brand = product.find(
            "h3",
            class_="product-brand"
        )

        # Product name
        product_name = product.find(
            "h4",
            class_="product-product"
        )

        # Selling price
        price = product.find(
            "span",
            class_="product-discountedPrice"
        )

        # Original price
        original_price = product.find(
            "span",
            class_="product-strike"
        )

        # Discount
        discount = product.find(
            "span",
            class_="product-discountPercentage"
        )

        # Rating
        rating_box = product.find(
            "div",
            class_="product-ratingsContainer"
        )

        # -----------------------------------
        # TEXT EXTRACTION
        # -----------------------------------

        brand = (
            brand.get_text(strip=True)
            if brand else None
        )

        product_name = (
            product_name.get_text(strip=True)
            if product_name else None
        )

        price = (
            price.get_text(strip=True)
            if price else None
        )

        original_price = (
            original_price.get_text(strip=True)
            if original_price else None
        )

        discount = (
            discount.get_text(strip=True)
            if discount else None
        )

        # -----------------------------------
        # RATING & REVIEWS
        # -----------------------------------

        rating = None
        reviews = None

        if rating_box:

            rating_text = rating_box.get_text(
                " ",
                strip=True
            )

            # Example:
            # 4.3 | 1200

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                rating_text
            )

            if len(numbers) >= 1:
                rating = numbers[0]

            if len(numbers) >= 2:
                reviews = numbers[1]

        # -----------------------------------
        # ADD RECORD
        # -----------------------------------

        all_products.append({

            "brand": brand,

            "product_name": product_name,

            "category": "T-Shirts",

            "gender": "Men",

            "price": price,

            "original_price": original_price,

            "discount": discount,

            "rating": rating,

            "reviews": reviews

        })

        # Stop at 1,500
        if len(all_products) >= TARGET_PRODUCTS:
            break

    print(
        "Total collected:",
        len(all_products)
    )

    page += 1

    # Safety limit
    if page > 40:
        print("Safety limit reached.")
        break


# -----------------------------------
# CLOSE BROWSER
# -----------------------------------

driver.quit()

# -----------------------------------
# DATAFRAME
# -----------------------------------

df = pd.DataFrame(all_products)

# Remove duplicate records
df = df.drop_duplicates(
    subset=[
        "brand",
        "product_name"
    ]
)

# Keep maximum 1,500
df = df.head(TARGET_PRODUCTS)

# -----------------------------------
# SAVE DATA
# -----------------------------------

df.to_csv(
    "myntra_1500_products.csv",
    index=False
)

# -----------------------------------
# RESULTS
# -----------------------------------

print("\n================================")
print("SCRAPING COMPLETED")
print("================================")

print(
    "Total products:",
    len(df)
)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 records:")
print(df.head(10))

print("\nMissing values:")
print(df.isnull().sum())

print(
    "\nFile saved as: "
    "myntra_1500_products.csv"
)
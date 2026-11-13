CREATE DATABASE myntra_analytics;

USE myntra_analytics;

CREATE TABLE myntra_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100),
    product_name VARCHAR(255),
    category VARCHAR(100),
    gender VARCHAR(20),
    price DECIMAL(10,2),
    original_price DECIMAL(10,2),
    discount DECIMAL(5,2),
    rating DECIMAL(3,2),
    reviews INT,
    discount_amount DECIMAL(10,2),
    price_segment VARCHAR(50)
);

USE myntra_analytics;

SELECT COUNT(*) AS total_products
FROM myntra_products;


DESCRIBE myntra_products;


SELECT
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(discount), 2) AS average_discount,
    ROUND(AVG(rating), 2) AS average_rating
FROM myntra_products;


SELECT
    COUNT(*) AS total_products,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(original_price), 2) AS avg_mrp,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(SUM(discount_amount), 2) AS total_discount_value
FROM myntra_products;


SELECT
    product_name,
    brand,
    price,
    original_price,
    discount,
    rating
FROM myntra_products
ORDER BY price DESC
LIMIT 10;


SELECT
    product_name,
    brand,
    price,
    discount,
    rating
FROM myntra_products
ORDER BY price ASC
LIMIT 10;


SELECT
    brand,
    COUNT(*) AS product_count
FROM myntra_products
GROUP BY brand
ORDER BY product_count DESC
LIMIT 10;


SELECT
    brand,
    COUNT(*) AS products,
    ROUND(AVG(price), 2) AS avg_price
FROM myntra_products
GROUP BY brand
ORDER BY avg_price DESC;


SELECT
    brand,
    COUNT(*) AS products,
    ROUND(AVG(discount), 2) AS avg_discount
FROM myntra_products
GROUP BY brand
ORDER BY avg_discount DESC;


SELECT
    product_name,
    brand,
    price,
    original_price,
    discount
FROM myntra_products
WHERE discount IS NOT NULL
ORDER BY discount DESC
LIMIT 10;


SELECT
    product_name,
    brand,
    price,
    discount,
    rating
FROM myntra_products
WHERE rating >= 4
ORDER BY rating DESC;


SELECT
    product_name,
    brand,
    price,
    original_price,
    discount,
    rating
FROM myntra_products
WHERE rating >= 4
  AND discount >= 30
ORDER BY rating DESC, discount DESC;


SELECT
    price_segment,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(AVG(rating), 2) AS avg_rating
FROM myntra_products
GROUP BY price_segment
ORDER BY avg_price;


SELECT
    brand,
    ROUND(AVG(price), 2) AS avg_price,
    RANK() OVER (
        ORDER BY AVG(price) DESC
    ) AS price_rank
FROM myntra_products
GROUP BY brand;


SELECT
    brand,
    product_name,
    price,
    rating,
    RANK() OVER (
        PARTITION BY brand
        ORDER BY rating DESC
    ) AS brand_rating_rank
FROM myntra_products;


SELECT
    product_name,
    brand,
    price,
    rating
FROM myntra_products
WHERE price > (
    SELECT AVG(price)
    FROM myntra_products
)
ORDER BY price DESC;


SELECT
    product_name,
    brand,
    price,
    original_price,
    discount
FROM myntra_products
WHERE discount >= 40
  AND price <= 1000
ORDER BY discount DESC;


SELECT
    brand,
    COUNT(*) AS total_products,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(discount_amount) AS total_discount_value
FROM myntra_products
GROUP BY brand
ORDER BY total_products DESC;


CREATE VIEW myntra_brand_analysis AS
SELECT
    brand,
    COUNT(*) AS total_products,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(original_price), 2) AS avg_mrp,
    ROUND(AVG(discount), 2) AS avg_discount,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(discount_amount) AS total_discount_value
FROM myntra_products
GROUP BY brand;


SELECT *
FROM myntra_brand_analysis;


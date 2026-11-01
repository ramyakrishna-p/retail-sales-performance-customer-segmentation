-- SYNTHETIC data analysis queries
-- Total revenue and AOV
SELECT SUM(revenue) AS total_revenue, AVG(revenue) AS aov, COUNT(*) AS orders FROM orders;
-- Monthly trend
SELECT substr(order_date,1,7) AS month, SUM(revenue) AS revenue FROM orders GROUP BY 1 ORDER BY 1;
-- Top products
SELECT product, SUM(revenue) AS revenue FROM orders GROUP BY product ORDER BY revenue DESC LIMIT 10;
-- Category performance
SELECT category, SUM(revenue) AS revenue, COUNT(*) AS orders FROM orders GROUP BY category ORDER BY revenue DESC;
-- RFM base
SELECT customer_id, MAX(order_date) AS last_order, COUNT(*) AS frequency, SUM(revenue) AS monetary FROM orders GROUP BY customer_id;

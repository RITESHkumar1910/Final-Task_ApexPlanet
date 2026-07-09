use APEX_PLANET;

-- CREATE TABLE superstore (
--     Row_ID INT,
--     Order_ID VARCHAR(50),
--     Order_Date VARCHAR(20),
--     Ship_Date VARCHAR(20),
--     Ship_Mode VARCHAR(50),
--     Customer_ID VARCHAR(50),
--     Customer_Name VARCHAR(100),
--     Segment VARCHAR(50),
--     Country VARCHAR(50),
--     City VARCHAR(50),
--     State VARCHAR(50),
--     Postal_Code VARCHAR(20),
--     Region VARCHAR(50),
--     Product_ID VARCHAR(50),
--     Category VARCHAR(50),
--     Sub_Category VARCHAR(50),
--     Product_Name VARCHAR(255),
--     Sales FLOAT,
--     Quantity INT,
--     Discount FLOAT,
--     Profit FLOAT
-- );


-- SET GLOBAL local_infile = 1;
-- LOAD DATA LOCAL INFILE 'C:/Users/Igrit/OneDrive/Desktop/Apex_planet/Sample - Superstore.csv'
-- INTO TABLE superstore
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;


-- SELECT Product_Name, ROUND(SUM(Sales),2) AS Total_Sales
-- FROM superstore
-- GROUP BY Product_Name
-- ORDER BY Total_Sales DESC
-- LIMIT 5;


-- Q2: Total Sales by Category
-- SELECT Category, ROUND(SUM(Sales),2) AS Total_Sales
-- FROM superstore
-- GROUP BY Category
-- ORDER BY Tot-- al_Sales DESC;


-- -- Q3: Most Profitable Region
-- SELECT Region, ROUND(SUM(Profit),2) AS Total_Profit
-- FROM superstore
-- GROUP BY Region
-- ORDER BY Total_Profit DESC;

-- -- Q4: Top 5 Customers by Sales
-- SELECT Customer_Name, ROUND(SUM(Sales),2) AS Total_Sales
-- FROM superstore
-- GROUP BY Customer_Name
-- ORDER BY Total_Sales DESC
-- LIMIT 5;

-- -- Q5: Sales by Segment
-- SELECT Segment, ROUND(SUM(Sales),2) AS Total_Sales
-- FROM superstore
-- GROUP BY Segment;

-- -- Q6: Least Profitable Sub-Categories
-- SELECT Sub_Category, ROUND(SUM(Profit),2) AS Total_Profit
-- FROM superstore
-- GROUP BY Sub_Category
-- ORDER BY Total_Profit ASC
-- LIMIT 5;

-- -- Q7: Orders by Ship Mode
-- SELECT Ship_Mode, COUNT(*) AS Total_Orders
-- FROM superstore
-- GROUP BY Ship_Mode
-- ORDER BY Total_Orders DESC;

-- -- Q8: Average Discount by Category
-- SELECT Category, ROUND(AVG(Discount),2) AS Avg_Discount
-- FROM superstore
-- GROUP BY Category;

-- -- Q9: Top 5 States by Sales
-- SELECT State, ROUND(SUM(Sales),2) AS Total_Sales
-- FROM superstore
-- GROUP BY State
-- ORDER BY Total_Sales DESC
-- LIMIT 5;

-- -- Q10: Total Revenue, Profit, Orders
-- SELECT 
--   COUNT(*) AS Total_Orders,
--   ROUND(SUM(Sales),2) AS Total_Revenue,
--   ROUND(SUM(Profit),2) AS Total_Pro-- fit
-- -- FROM superstore;

-- Q11: Row Number - Customers ranked by Sales
-- SELECT Customer_Name, 
--        ROUND(SUM(Sales),2) AS Total_Sales,
--        RANK() OVER (ORDER BY SUM(Sales) DESC) AS Sales_Rank
-- FROM superstore
-- GROUP BY Customer_Name
-- LIMIT 10;

-- -- Q12: CTE - High Value Orders (Sales > 1000)
-- WITH High_Value AS (
--     SELECT Order_ID, Customer_Name, Sales, Profit
--     FROM superstore
--     WHERE Sales > 1000
-- )
-- SELECT * FROM High_Value
-- ORDER BY Sales DESC
-- LIMIT 10;

-- -- Q13: LAG - Compare Sales (Month over Month trend)
-- SELECT Order_Date, 
--        ROUND(SUM(Sales),2) AS Monthly_Sales,
--        LAG(ROUND(SUM(Sales),2)) OVER (ORDER BY Order_Date) AS Prev_Sales
-- FROM superstore
-- GROUP BY Order_Date
-- LIMIT 10;

-- -- Q14: Create a View
-- CREATE VIEW top_customers AS
-- SELECT Customer_Name, 
--        ROUND(SUM(Sales),2) AS Total_Sales,
--        ROUND(SUM(Profit),2) AS Total_Profit
-- FROM superstore
-- GROUP BY Customer_Name
-- ORDER BY Total_Sales DESC;

-- -- Check View
-- SELECT * FROM top_customers LIMIT 5;


SELECT*FROM superstore;


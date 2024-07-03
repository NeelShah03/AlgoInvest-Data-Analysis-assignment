SELECT SUM(TotalValue) AS TotalSales FROM Sales;
SELECT ProductID, SUM(TotalValue) AS TotalSales FROM Sales
GROUP BY ProductID
ORDER BY TotalSales DESC
LIMIT 3;
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(OrderDate, '%Y-%m') AS Month,
        SUM(TotalValue) AS MonthlySales
    FROM Sales
    GROUP BY DATE_FORMAT(OrderDate, '%Y-%m')
),
MonthlyGrowth AS (
    SELECT 
        Month,
        MonthlySales,
        LAG(MonthlySales) OVER (ORDER BY Month) AS PreviousMonthSales
    FROM MonthlySales
)
SELECT 
    Month,
    MonthlySales,
    PreviousMonthSales,
    CASE 
        WHEN PreviousMonthSales IS NULL THEN NULL
        ELSE (MonthlySales - PreviousMonthSales) / PreviousMonthSales * 100 
    END AS GrowthPercentage
FROM MonthlyGrowth
ORDER BY Month;
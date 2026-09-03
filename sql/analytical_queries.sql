-- ============================================================
-- RECRUITMENT DATA WAREHOUSE
-- ANALYTICAL QUERIES
-- ============================================================


-- ============================================================
-- R1 - HIRING TRENDS
-- ============================================================

SELECT
    d.Year,
    COUNT(*) AS Total_Applications,
    SUM(f.Hiring_Outcome) AS Hired_Candidates,
    COUNT(*) - SUM(f.Hiring_Outcome) AS Not_Hired_Candidates,
    ROUND(
        100.0 * SUM(f.Hiring_Outcome) / COUNT(*),
        2
    ) AS Hiring_Rate_Percent
FROM Fact_Application f
JOIN Dim_Date d
    ON f.Date_Key = d.Date_Key
GROUP BY d.Year
ORDER BY d.Year;


-- ============================================================
-- R2 - TECHNOLOGY ANALYSIS
-- ============================================================

SELECT
    t.Technology,
    COUNT(*) AS Total_Applications,
    SUM(f.Hiring_Outcome) AS Hired_Candidates,
    COUNT(*) - SUM(f.Hiring_Outcome) AS Not_Hired_Candidates,
    ROUND(
        100.0 * SUM(f.Hiring_Outcome) / COUNT(*),
        2
    ) AS Hiring_Rate_Percent
FROM Fact_Application f
JOIN Dim_Technology t
    ON f.Technology_Key = t.Technology_Key
GROUP BY t.Technology
ORDER BY Hired_Candidates DESC;


-- ============================================================
-- R3 - CANDIDATE PROFILE ANALYSIS
-- ============================================================

SELECT
    p.Seniority,
    COUNT(*) AS Total_Applications,
    ROUND(AVG(f.YOE), 2) AS Average_YOE,
    SUM(f.Hiring_Outcome) AS Hired_Candidates,
    COUNT(*) - SUM(f.Hiring_Outcome) AS Not_Hired_Candidates,
    ROUND(
        100.0 * SUM(f.Hiring_Outcome) / COUNT(*),
        2
    ) AS Hiring_Rate_Percent
FROM Fact_Application f
JOIN Dim_Profile p
    ON f.Profile_Key = p.Profile_Key
GROUP BY p.Seniority
ORDER BY Hiring_Rate_Percent DESC;


-- R3 - YOE ANALYSIS

SELECT
    CASE
        WHEN YOE <= 2 THEN '0-2 years'
        WHEN YOE <= 5 THEN '3-5 years'
        WHEN YOE <= 10 THEN '6-10 years'
        WHEN YOE <= 15 THEN '11-15 years'
        ELSE '16+ years'
    END AS YOE_Range,
    COUNT(*) AS Total_Applications,
    SUM(Hiring_Outcome) AS Hired_Candidates,
    ROUND(
        100.0 * SUM(Hiring_Outcome) / COUNT(*),
        2
    ) AS Hiring_Rate_Percent
FROM Fact_Application
GROUP BY YOE_Range
ORDER BY MIN(YOE);


-- ============================================================
-- R4 - TECHNICAL ASSESSMENT EFFECTIVENESS
-- ============================================================

SELECT
    'Code Challenge' AS Assessment,
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 1
                THEN Code_Challenge_Score
            END
        ),
        2
    ) AS Hired_Average_Score,
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 0
                THEN Code_Challenge_Score
            END
        ),
        2
    ) AS Not_Hired_Average_Score,
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 1
                THEN Code_Challenge_Score
            END
        )
        -
        AVG(
            CASE
                WHEN Hiring_Outcome = 0
                THEN Code_Challenge_Score
            END
        ),
        2
    ) AS Score_Difference
FROM Fact_Application

UNION ALL

SELECT
    'Technical Interview' AS Assessment,
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 1
                THEN Technical_Interview_Score
            END
        ),
        2
    ),
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 0
                THEN Technical_Interview_Score
            END
        ),
        2
    ),
    ROUND(
        AVG(
            CASE
                WHEN Hiring_Outcome = 1
                THEN Technical_Interview_Score
            END
        )
        -
        AVG(
            CASE
                WHEN Hiring_Outcome = 0
                THEN Technical_Interview_Score
            END
        ),
        2
    )
FROM Fact_Application;


-- ============================================================
-- R5 - TECHNOLOGY-ASSESSMENT ANALYSIS
-- ============================================================

SELECT
    t.Technology,
    COUNT(*) AS Total_Applications,
    ROUND(
        AVG(f.Code_Challenge_Score),
        2
    ) AS Avg_Code_Challenge_Score,
    ROUND(
        AVG(f.Technical_Interview_Score),
        2
    ) AS Avg_Technical_Interview_Score,
    SUM(f.Hiring_Outcome) AS Hired_Candidates,
    ROUND(
        100.0 * SUM(f.Hiring_Outcome) / COUNT(*),
        2
    ) AS Hiring_Rate_Percent
FROM Fact_Application f
JOIN Dim_Technology t
    ON f.Technology_Key = t.Technology_Key
GROUP BY t.Technology
ORDER BY Hiring_Rate_Percent DESC;
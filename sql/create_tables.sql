-- ============================================================
-- RECRUITMENT DATA WAREHOUSE
-- MySQL Dimensional Model
-- ============================================================

-- ------------------------------------------------------------
-- Create database
-- ------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS recruitment_dw;

USE recruitment_dw;


-- ------------------------------------------------------------
-- Reset existing tables
-- Fact table is dropped first because it references
-- the dimension tables through foreign keys.
-- ------------------------------------------------------------

DROP TABLE IF EXISTS Fact_Application;
DROP TABLE IF EXISTS Dim_Profile;
DROP TABLE IF EXISTS Dim_Technology;
DROP TABLE IF EXISTS Dim_Date;


-- ============================================================
-- DIMENSION: DATE
-- ============================================================

CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY,
    Application_Date DATE NOT NULL,
    Day INT NOT NULL,
    Month INT NOT NULL,
    Quarter INT NOT NULL,
    Year INT NOT NULL
);


-- ============================================================
-- DIMENSION: TECHNOLOGY
-- ============================================================

CREATE TABLE Dim_Technology (
    Technology_Key INT PRIMARY KEY,
    Technology VARCHAR(150) NOT NULL UNIQUE
);


-- ============================================================
-- DIMENSION: PROFILE
-- ============================================================

CREATE TABLE Dim_Profile (
    Profile_Key INT PRIMARY KEY,
    Seniority VARCHAR(50) NOT NULL UNIQUE
);


-- ============================================================
-- FACT: APPLICATION
-- ============================================================

CREATE TABLE Fact_Application (
    Application_Key INT PRIMARY KEY,
    
    Date_Key INT NOT NULL,
    Technology_Key INT NOT NULL,
    Profile_Key INT NOT NULL,

    YOE INT NOT NULL,
    Code_Challenge_Score INT NOT NULL,
    Technical_Interview_Score INT NOT NULL,
    Hiring_Outcome TINYINT NOT NULL,

    -- --------------------------------------------------------
    -- Foreign Keys
    -- --------------------------------------------------------

    CONSTRAINT fk_fact_date
        FOREIGN KEY (Date_Key)
        REFERENCES Dim_Date(Date_Key),

    CONSTRAINT fk_fact_technology
        FOREIGN KEY (Technology_Key)
        REFERENCES Dim_Technology(Technology_Key),

    CONSTRAINT fk_fact_profile
        FOREIGN KEY (Profile_Key)
        REFERENCES Dim_Profile(Profile_Key),

    -- --------------------------------------------------------
    -- Business validation
    -- --------------------------------------------------------

    CONSTRAINT chk_hiring_outcome
        CHECK (Hiring_Outcome IN (0, 1)),

    CONSTRAINT chk_yoe
        CHECK (YOE >= 0),

    CONSTRAINT chk_code_challenge_score
        CHECK (Code_Challenge_Score BETWEEN 0 AND 10),

    CONSTRAINT chk_technical_interview_score
        CHECK (Technical_Interview_Score BETWEEN 0 AND 10)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_fact_application_date
    ON Fact_Application(Date_Key);

CREATE INDEX idx_fact_application_technology
    ON Fact_Application(Technology_Key);

CREATE INDEX idx_fact_application_profile
    ON Fact_Application(Profile_Key);
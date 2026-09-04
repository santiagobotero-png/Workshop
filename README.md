# Recruitment Data Warehouse - ETL

## 1. Project Objective

The objective of this project is to design and implement an ETL process to transform transactional data from a technology recruitment process into a dimensional Data Warehouse oriented toward analysis.

The project comprises the stages of extraction, preparation, business rule transformation, dimensional modeling, loading into a Data Warehouse, and analysis through SQL queries and a Business Intelligence tool.

The Data Warehouse is designed to address five business requirements related to hiring trends, technology analysis, candidate profiles, technical assessment effectiveness, and the relationship between technologies, assessments, and hiring.

## 2. Business Context

The organization in the case study is a company dedicated to recruiting professionals in the technology field. The company receives thousands of candidate applications for different profiles and technologies.

Each application contains information about the candidate, the application date, country, years of experience, seniority level, associated technology, and the results obtained in two technical assessments:

- Code Challenge Score
- Technical Interview Score

The organization needs to transform this operational data into analytical information that allows it to identify hiring patterns and support decision-making.

To determine whether an application results in a hire, the following business rule is used:

HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7

Therefore, a candidate is considered hired only when they obtain a score of at least 7 in both assessments.


## 3. Business Requirements

### R1 - Hiring Trends

Analyze hiring trends over time to study how application and hiring behavior evolves across different periods.

**Business Question:**

How has the volume of applications and the number of hired candidates evolved over time?

---

### R2 - Technology Analysis

Compare hiring results across different technologies to identify which ones generate the highest number and proportion of hired candidates.

**Business Question:**

Which technologies have the highest number and proportion of hired candidates?

---

### R3 - Candidate Profile Analysis

Analyze hiring results according to the candidates' seniority level and years of professional experience.

**Business Question:**

How does the hiring outcome vary according to seniority level and years of professional experience?

---

### R4 - Technical Assessment Effectiveness

Evaluate the descriptive effectiveness of the two technical assessments by comparing their results between hired and non-hired candidates.

**Business Question:**

Which technical assessment presents a greater difference between hired and non-hired candidates?

---

### R5 - Technology-Assessment Analysis

Analyze the performance of technical assessments across different technologies and study their descriptive relationship with hiring outcomes.

**Business Question:**

How does technical assessment performance vary across technologies, and how is it related to hiring?


## 4. Requirements Traceability

The following matrix relates each business requirement to the Data Warehouse tables, the main metrics used, and the analysis performed.

| Requirement | DW Tables Used | Main KPIs / Metrics | Visualization / Analysis |
|---|---|---|---|
| R1 - Hiring Trends | Fact_Application, Dim_Date | Total Applications, Hired Candidates, Hiring Rate | Application and hiring trends by year |
| R2 - Technology Analysis | Fact_Application, Dim_Technology | Hired Candidates, Total Applications, Hiring Rate | Hiring comparison by technology |
| R3 - Candidate Profile Analysis | Fact_Application, Dim_Profile | Hiring Rate, Average YOE, Hired Candidates | Comparison by seniority and experience ranges |
| R4 - Technical Assessment Effectiveness | Fact_Application | Average Code Challenge Score, Average Technical Interview Score, Score Difference | Comparison of assessments between HIRED and NOT HIRED |
| R5 - Technology-Assessment Analysis | Fact_Application, Dim_Technology | Average Code Challenge Score, Average Technical Interview Score, Hiring Rate | Comparison of technical performance and hiring by technology |

Each requirement is supported by attributes and metrics available in the Data Warehouse. No dimensions or attributes were incorporated solely because they were available in the dataset; the elements of the model were selected according to their analytical usefulness.


## 5. Dataset Description

The input dataset corresponds to the `candidates.csv` file, located at:

`data/raw/candidates.csv`

The file contains transactional information related to candidate applications to technology recruitment processes.

The file uses `;` as the separator and contains 50,000 records and 10 original columns:

| Field | Description |
|---|---|
| First Name | Candidate's first name |
| Last Name | Candidate's last name |
| Email | Email address registered in the application |
| Application Date | Date on which the application was submitted |
| Country | Country associated with the application |
| YOE | Years of Experience; years of professional experience |
| Seniority | Candidate's professional level |
| Technology | Technology or technical profile associated with the application |
| Code Challenge Score | Score obtained in the Code Challenge, on a scale from 0 to 10 |
| Technical Interview Score | Score obtained in the Technical Interview, on a scale from 0 to 10 |

### Temporal Scope

Application dates range from:

- Minimum date: `2018-01-01`
- Maximum date: `2022-07-04`

Therefore, the year 2022 represents a partial period and should not be directly compared with the previous full years in terms of annual volume.

### Data Characteristics

The dataset represents individual applications and not necessarily unique candidates. During profiling, 49,833 unique email addresses were identified across 50,000 records, indicating the existence of candidates with multiple applications according to the Email field.

Because the email address presents inconsistencies in some records and does not constitute a reliable candidate identifier, it was not used as a key in the dimensional model.

The dataset is preserved without modifications in `data/raw/` as the original source of the ETL process.



## 6. Main Profiling Findings

Before performing the business transformations and constructing the dimensional model, a profiling process was performed on the original dataset.

The main results were as follows:

| Aspect | Result |
|---|---:|
| Records | 50,000 |
| Original columns | 10 |
| Unique emails | 49,833 |
| Records with multiple applications | 165 candidates identified through Email |
| Exact duplicates | 0 |
| Missing values | 0 |
| Minimum application date | 2018-01-01 |
| Maximum application date | 2022-07-04 |
| Code Challenge Score range | 0–10 |
| Technical Interview Score range | 0–10 |
| YOE range | 0–30 years |
| HIRED | 6,698 |
| NOT HIRED | 43,302 |

### Data Quality

No missing values were found in the columns of the original dataset, and no completely duplicated records were identified.

Dates, years of experience, and scores were converted to appropriate data types during the preparation stage.

The categorical variables `Seniority` and `Technology` were standardized by removing unnecessary spaces.

### Multiple Applications

The profiling showed that there are records associated with the same Email across different applications. For this reason, these rows were not removed as duplicates.

The analysis of the data also showed that some email addresses are associated with different candidate names and characteristics. This indicates that the Email field cannot be considered a reliable identifier within this dataset.

Consequently, it was decided to model each record as an independent application and not to build a candidate dimension based on Email.

### Hiring Rule

Based on the business rule:

`HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7`

the following distribution was obtained:

- HIRED: 6,698 applications
- NOT HIRED: 43,302 applications
- Total: 50,000 applications

Therefore, approximately 13.40% of applications simultaneously meet the established hiring criteria.

### Decisions Derived from Profiling

The profiling results allowed several decisions to be established for the following stages of the project:

1. Keep the 50,000 applications as independent events.
2. Do not remove multiple applications as if they were duplicates.
3. Do not use Email as a key in the dimensional model.
4. Keep both HIRED and NOT HIRED records, since both are necessary for the technical assessment effectiveness analyses.
5. Convert dates, years of experience, and scores to appropriate numeric or temporal data types.
6. Standardize categorical variables before building the dimensions.


## 6. Main Profiling Findings

Before performing the business transformations and constructing the dimensional model, a profiling process was performed on the original dataset.

The main results were as follows:

| Aspect | Result |
|---|---:|
| Records | 50,000 |
| Original columns | 10 |
| Unique emails | 49,833 |
| Records with multiple applications | 165 candidates identified through Email |
| Exact duplicates | 0 |
| Missing values | 0 |
| Minimum application date | 2018-01-01 |
| Maximum application date | 2022-07-04 |
| Code Challenge Score range | 0–10 |
| Technical Interview Score range | 0–10 |
| YOE range | 0–30 years |
| HIRED | 6,698 |
| NOT HIRED | 43,302 |

### Data Quality

No missing values were found in the columns of the original dataset, and no completely duplicated records were identified.

Dates, years of experience, and scores were converted to appropriate data types during the preparation stage.

The categorical variables `Seniority` and `Technology` were standardized by removing unnecessary spaces.

### Multiple Applications

The profiling showed that there are records associated with the same Email across different applications. For this reason, these rows were not removed as duplicates.

The analysis of the data also showed that some email addresses are associated with different candidate names and characteristics. This indicates that the Email field cannot be considered a reliable identifier within this dataset.

Consequently, it was decided to model each record as an independent application and not to build a candidate dimension based on Email.

### Hiring Rule

Based on the business rule:

`HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7`

the following distribution was obtained:

- HIRED: 6,698 applications
- NOT HIRED: 43,302 applications
- Total: 50,000 applications

Therefore, approximately 13.40% of applications simultaneously meet the established hiring criteria.

### Decisions Derived from Profiling

The profiling results allowed several decisions to be established for the following stages of the project:

1. Keep the 50,000 applications as independent events.
2. Do not remove multiple applications as if they were duplicates.
3. Do not use Email as a key in the dimensional model.
4. Keep both HIRED and NOT HIRED records, since both are necessary for the technical assessment effectiveness analyses.
5. Convert dates, years of experience, and scores to appropriate numeric or temporal data types.
6. Standardize categorical variables before building the dimensions.




---

# 8. Grain Definition

Here we want to be particularly clear, because **granularity** is one of the most important concepts in the model.


## Grain Definition

The granularity of the `Fact_Application` table is defined as:

> **One row in `Fact_Application` represents one individual application submitted by a candidate to the recruitment process.**

Therefore, each record in the fact table corresponds to an application event and retains the information necessary to analyze the outcome of that event.

The selected grain allows the following analyses:

- Number of applications.
- Number of hired and non-hired applications.
- Hiring rates.
- Average technical assessment scores.
- Hiring outcomes by date.
- Hiring outcomes by technology.
- Hiring outcomes by seniority.
- Hiring outcomes by years-of-experience ranges.

### Grain Implications

Multiple applications from the same candidate are not automatically considered duplicates. Each application represents an independent event within the business process and is therefore preserved as a different row in `Fact_Application`.

The `Email` field is not used as a candidate identifier or as the key of the fact table, due to the inconsistencies detected during profiling.

The fact table uses `Application_Key` as a surrogate key to identify each application record within the Data Warehouse.

### Relationship Between Grain and Requirements

The selected grain allows all five business requirements to be satisfied:

| Requirement | Information Supported by the Grain |
|---|---|
| R1 - Hiring Trends | Date and outcome of each application |
| R2 - Technology Analysis | Technology and outcome of each application |
| R3 - Candidate Profile Analysis | Seniority, YOE, and outcome |
| R4 - Technical Assessment Effectiveness | Scores from both assessments and outcome |
| R5 - Technology-Assessment Analysis | Technology, scores, and outcome |

The selected grain preserves the level of detail required to perform the analyses without losing information during the transformation into the dimensional model.

---

## 9. Dimensional Model - Star Schema

The Data Warehouse was implemented using a **Star Schema dimensional model**. 
The `Fact_Application` fact table is located at the center of the model and contains 
the application events, while the dimensions provide the necessary context for the different analyses.

### Model Diagram

![Data Warehouse Star Schema](diagrams/star_schema.png)

### Model Structure

The model consists of one fact table and three dimensions:

- `Fact_Application`: stores application events and their analytical values.
- `Dim_Date`: provides temporal context.
- `Dim_Technology`: provides context related to technology.
- `Dim_Profile`: provides context related to seniority level.

The relationships in the model are:

```text
Dim_Date          1 ─────── N Fact_Application
Dim_Technology    1 ─────── N Fact_Application
Dim_Profile       1 ─────── N Fact_Application




---

# 10. Description of Dimensions and Fact Table

We now document each table in greater detail.

```markdown
## 10. Description of Dimensions and Fact Table

### 10.1 Dim_Date

The `Dim_Date` dimension contains the temporal information associated with each application date.

Its purpose is to facilitate the analysis of applications and hiring over time without having to perform transformations on the date stored in the fact table.

| Field | Type | Key | Description |
|---|---|---|---|
| `Date_Key` | INT | PK | Surrogate key for the date. |
| `Application_Date` | DATE | - | Date on which the application was submitted. |
| `Day` | INT | - | Day corresponding to the date. |
| `Month` | INT | - | Month corresponding to the date. |
| `Quarter` | INT | - | Quarter corresponding to the date. |
| `Year` | INT | - | Year corresponding to the date. |

The dimension is built from the unique dates present in the applications. A **surrogate key** (`Date_Key`) is generated for each date.

This dimension primarily supports requirement **R1 - Hiring Trends**.

---

### 10.2 Dim_Technology

The `Dim_Technology` dimension contains the technologies associated with the applications.

Its purpose is to enable the analysis and comparison of hiring outcomes across different technologies.

| Field | Type | Key | Description |
|---|---|---|---|
| `Technology_Key` | INT | PK | Surrogate key for the technology. |
| `Technology` | VARCHAR(150) | - | Name of the technology or technical area. |

Technology values are deduplicated before surrogate keys are generated. This ensures that each technology appears only once in the dimension.

This dimension primarily supports:

- **R2 - Technology Analysis**
- **R5 - Technology-Assessment Analysis**

---

### 10.3 Dim_Profile

The `Dim_Profile` dimension contains the seniority level associated with each application.

Its purpose is to provide the necessary context to analyze hiring outcomes according to the candidate's professional profile.

| Field | Type | Key | Description |
|---|---|---|---|
| `Profile_Key` | INT | PK | Surrogate key for the profile. |
| `Seniority` | VARCHAR(50) | - | Candidate's seniority level. |

Seniority values are deduplicated before surrogate keys are generated.

This dimension primarily supports:

- **R3 - Candidate Profile Analysis**

Years of experience (`YOE`) are not stored in this dimension. They remain in `Fact_Application` because they represent a numeric value for each application and can be used to calculate averages, ranges, and hiring rates.

---

### 10.4 Fact_Application

`Fact_Application` is the central table of the dimensional model. Each row represents an individual application, according to the previously defined grain.

It contains the keys that relate each application to the dimensions and the quantitative values required to perform the analyses.

| Field | Type | Key | Description |
|---|---|---|---|
| `Application_Key` | INT | PK | Unique surrogate key for the application. |
| `Date_Key` | INT | FK | Reference to `Dim_Date`. |
| `Technology_Key` | INT | FK | Reference to `Dim_Technology`. |
| `Profile_Key` | INT | FK | Reference to `Dim_Profile`. |
| `YOE` | INT | - | Years of professional experience. |
| `Code_Challenge_Score` | INT | - | Score obtained in the Code Challenge. |
| `Technical_Interview_Score` | INT | - | Score obtained in the Technical Interview. |
| `Hiring_Outcome` | TINYINT | - | Hiring outcome indicator: `1 = HIRED`, `0 = NOT HIRED`. |

The table preserves both hired and non-hired applications. This is necessary because several requirements require comparisons between both groups.

For example, requirement **R4** requires comparing the average technical assessment scores between hired and non-hired candidates. If non-hired applications were removed during the ETL process, this analysis would not be possible.

For this reason, `Hiring_Outcome` functions as an analytical indicator that allows the calculation of:

- Total applications.
- Total hired applications.
- Total non-hired applications.
- Hiring rate.
- Average technical assessment scores.
- Differences between hired and non-hired candidates.

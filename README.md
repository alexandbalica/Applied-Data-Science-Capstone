# Predicting Falcon 9 First-Stage Landing Success 🚀

**End-to-End Data Science Project | IBM Data Science Professional Certificate**

## Project Overview

This project investigates the factors associated with successful SpaceX Falcon 9 first-stage landings and evaluates whether landing outcomes can be predicted using historical launch data.

The analysis combines data acquisition, feature engineering, exploratory analysis, SQL, geospatial visualization, interactive dashboarding, and machine learning.

**[View the Complete Project Report (PDF)](SpaceX_Falcon9_Landing_Prediction_Report.pdf)**

## Objectives

- Explore how landing outcomes relate to flight history, launch site, orbit type, payload mass, and booster characteristics.
- Identify geographic patterns and examine launch-site proximity to selected infrastructure.
- Develop an interactive dashboard for exploring mission characteristics and landing outcomes.
- Train, tune, and compare classification models for predicting first-stage landing success.

## Technical Workflow

| Stage | Tools & Techniques |
|---|---|
| Data Collection | REST APIs, web scraping, BeautifulSoup |
| Data Preparation | Pandas, cleaning, feature engineering |
| Exploratory Analysis | SQL, Matplotlib, Seaborn |
| Geospatial Analysis | Folium, marker clustering, Haversine distance |
| Interactive Dashboard | Plotly, Dash |
| Machine Learning | Scikit-learn, GridSearchCV, classification pipelines |

## Machine Learning Results

Four classification algorithms were evaluated:

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | 83.33% |
| Decision Tree | 83.33% |
| K-Nearest Neighbors | 83.33% |
| Support Vector Machine | 83.33% |

**Key findings:**

- All four models achieved the same accuracy on the 18-observation test set.
- Successful landings were correctly identified in 12 of 12 cases.
- Failed landings were correctly identified in 3 of 6 cases.
- The models exceeded the test set's majority-class accuracy baseline of 66.67%.

**Limitation:** The small test set restricts confidence in the generalizability of these results. The project demonstrates a complete classification workflow rather than a production-ready predictive system.

## Exploratory & Geospatial Findings

- Observed landing success improved across later Falcon 9 flights.
- Landing outcomes varied across orbit types, payload ranges, and launch sites.
- Interactive Folium maps illustrated launch-site geography and landing-outcome distributions.
- Distance calculations quantified the proximity of selected launch sites to geographic and transportation reference points.

These findings describe observed associations and should not be interpreted as proof of causation.

## Repository Contents

The repository includes Jupyter notebooks covering data collection, wrangling, SQL, exploratory visualization, Folium mapping, and classification.

It also includes a final presentation report documenting the methodology, visualizations, results, and limitations.

Standalone dashboard and geospatial scripts supplement the notebook-based analyses.

## Attribution

This project was completed as part of **IBM's Applied Data Science Capstone on Coursera**. IBM Skills Network provided the educational framework, datasets, and guided laboratory materials.

I completed and adapted the analytical implementations and developed additional dashboard and geospatial visualizations, with AI-assisted code review and refinement.

## Author

**Alexandru Balica**

[GitHub Profile](https://github.com/alexandbalica)

# Predicting Falcon 9 First-Stage Landing Success 🚀

**End-to-End Data Science Project | IBM Data Science Professional Certificate**

## Project Overview

This project investigates the factors associated with successful SpaceX Falcon 9 first-stage landings and evaluates whether landing outcomes can be predicted using historical launch data.

The project demonstrates an end-to-end data science workflow, combining **API data collection, web scraping, data wrangling, SQL analysis, exploratory visualization, geospatial mapping, interactive dashboarding, and machine learning**.

**[📄 View the Complete Project Report (PDF)](SpaceX_Falcon9_Landing_Prediction_Report.pdf)**

## Project Objectives

- Investigate relationships between first-stage landing outcomes and launch site, orbit type, payload mass, booster characteristics, and flight history.
- Explore historical trends in landing outcomes using Python visualizations and SQL.
- Examine launch-site geography and proximity to selected transportation infrastructure.
- Develop an interactive Plotly Dash dashboard for exploring landing outcomes.
- Train, tune, and evaluate classification models to predict first-stage landing success.

## Technical Workflow

| Stage | Tools & Techniques |
|---|---|
| Data Collection | REST API, Requests, BeautifulSoup, HTML Parsing |
| Data Preparation | Pandas, NumPy, Data Cleaning, Feature Engineering |
| Exploratory Data Analysis | Pandas, Matplotlib, Seaborn |
| SQL Analysis | SQLite, Filtering, Aggregation, GROUP BY |
| Geospatial Analysis | Folium, Marker Clustering, Haversine Distance |
| Interactive Dashboard | Plotly, Dash, Interactive Callbacks |
| Machine Learning | Scikit-learn, Pipelines, GridSearchCV, Cross-Validation |
| Model Evaluation | Accuracy, Precision, Recall, F1-score, Confusion Matrix |

## Machine Learning Results

Four supervised classification algorithms were trained and evaluated using historical Falcon 9 launch characteristics.

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | 83.33% |
| Decision Tree | 83.33% |
| K-Nearest Neighbors (KNN) | 83.33% |
| Support Vector Machine (SVM) | 83.33% |

### Key Findings

- All four models achieved 83.33% accuracy on the 18-observation test set.
- **Successful landings:** 12 of 12 correctly identified (100% sensitivity).
- **Failed landings:** 3 of 6 correctly identified (50% specificity).
- **Precision for successful landings:** 80%.
- **Majority-class baseline:** 66.67% accuracy.

Although all four models achieved identical test accuracy, the evaluation revealed weaker identification of unsuccessful landings.

**Limitations:** The relatively small test set limits confidence in generalization performance. These results demonstrate the classification workflow rather than a production-ready prediction system.

To reduce data leakage, feature scaling for applicable models was incorporated into scikit-learn Pipelines during cross-validation. A fixed random seed was also used to improve Decision Tree reproducibility.

## Exploratory & Geospatial Findings

The exploratory analysis revealed several descriptive patterns:

- First-stage landing success became more common across later Falcon 9 flights.
- Landing outcomes varied across orbit types, payload ranges, launch sites, and booster configurations.
- Interactive Folium maps illustrated the geographic distribution of launch sites in Florida and California.
- Color-coded markers and clustering enabled exploration of landing outcomes at individual launch sites.
- Haversine distance calculations quantified straight-line proximity to selected coastline, railway, highway, and city reference points.

These patterns should be interpreted as **associations, not evidence of causation**.

## Repository Contents

### Jupyter Notebooks

The six notebooks document the primary analytical workflow.

| Notebook | Description |
|---|---|
| [01 — SpaceX API Collection](01_spacex_api_collection.ipynb) | API acquisition, launch-data enrichment, and archived-data fallback |
| [02 — Web Scraping](02_spacex_web_scraping.ipynb) | Extracting historical launch records from HTML tables |
| [03 — Data Wrangling](03_spacex_data_wrangling.ipynb) | Data cleaning, binary landing labels, and feature preparation |
| [04 — SQL Analysis](04_spacex_sql_analysis.ipynb) | Mission filtering, aggregation, payload analysis, and outcome queries |
| [05 — EDA & Visualization](05_spacex_eda_visualization.ipynb) | Landing patterns across flights, launch sites, payloads, and orbits |
| [06 — Machine Learning Classification](06_spacex_ml_classification.ipynb) | Model training, cross-validation, hyperparameter tuning, and evaluation |

### Standalone Python Applications

| File | Description |
|---|---|
| [Interactive SpaceX Dashboard](scripts/spacex_dashboard.py) | Launch-site and payload exploration using Plotly Dash |
| [Launch Site Overview](scripts/launch_site_overview.py) | Geographic distribution of SpaceX launch sites |
| [Vandenberg Landing Outcomes](scripts/vandenberg_landing_outcomes.py) | Color-coded landing outcomes at VAFB SLC-4E |
| [Florida Landing Outcomes](scripts/florida_landing_outcomes.py) | Interactive mapping of Florida launch records |
| [Launch Site POI Distances](scripts/launch_site_poi_distances.py) | Haversine distances to selected geographic and transportation points |

### Additional Resources

- [Complete Project Report — PDF](SpaceX_Falcon9_Landing_Prediction_Report.pdf)
- [Python Dependencies](requirements.txt)

## Getting Started

### 1. Clone the Repository

`git clone https://github.com/alexandbalica/spacex-falcon9-landing-prediction.git`

`cd spacex-falcon9-landing-prediction`

### 2. Install Dependencies

Requires a compatible Python 3 environment.

`python -m pip install -r requirements.txt`

### 3. Explore the Notebooks

Open the Jupyter notebooks in VS Code or Jupyter Notebook.

The notebooks are numbered to follow the analytical workflow. Some stages use IBM's archived historical datasets to preserve consistency with the educational project.

### 4. Run the Interactive Dashboard

`python scripts/spacex_dashboard.py`

Open the local Dash address displayed in the terminal, typically `http://127.0.0.1:8050/`.

The dashboard supports:

- Filtering by launch site.
- Interactive exploration of payload ranges.
- Visual comparison of first-stage landing outcomes.
- Exploration of payload mass and booster characteristics.

The landing-distribution chart responds to launch-site selection, while the payload scatter plot responds to both launch-site and payload-range filters.

### 5. Explore the Geospatial Maps

Run any of the standalone Folium scripts in the `scripts/` directory.

Each script generates an interactive HTML map that can be opened in a browser.

## Data Sources & Methodological Notes

**Data Sources**

- SpaceX public launch-data API.
- IBM Skills Network historical SpaceX datasets.
- Publicly available historical launch information.

**API Availability**

The original SpaceX API may be unavailable. The API collection notebook contains a documented fallback to IBM's archived historical dataset to support reproducible analysis when live API requests fail.

**Landing Outcome Definition**

The binary classification target follows the IBM capstone's educational labeling convention, which includes certain controlled ocean landing outcomes in the positive class.

Consequently, the target should not be interpreted as an exact measurement of successful booster recovery for reuse.

**Geospatial Distances**

Distances to transportation and geographic reference points are calculated as straight-line approximations. They do not represent driving distances or prove that specific infrastructure influenced launch-site selection.

**Historical Scope**

The analysis uses historical datasets from the IBM capstone. Results should not be interpreted as reflecting SpaceX's current operational performance.

## Attribution & Acknowledgments

This project was developed as part of **IBM's Applied Data Science Capstone**, included in the **IBM Data Science Professional Certificate on Coursera**.

IBM Skills Network provided the educational project framework, guided laboratory materials, and supporting datasets.

I completed, adapted, debugged, and extended the analytical implementations, including additional interactive dashboard and geospatial visualization work, with AI-assisted code review and refinement.

The project builds upon IBM's educational material while presenting my implementation, analytical interpretation, improvements, and technical learning.

## Author

**Alexandru Balica**

[GitHub Profile](https://github.com/alexandbalica)

---

*An end-to-end data science portfolio project demonstrating the full analytical lifecycle, from raw data collection to exploratory analysis, predictive modeling, and interactive visualization.*

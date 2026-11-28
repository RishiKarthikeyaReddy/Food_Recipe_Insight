# Food Recipe Insight

## Project Overview

Food Recipe Insight is a Python-based data science project that analyzes the Food.com Recipes and User Interactions datasets. The project evaluates and ranks recipes using three methods: Average Rating, Median Rating, and Bayesian Weighted Rating. It aims to provide more reliable recipe rankings by considering both user ratings and the number of ratings received by each recipe. The results are presented through an interactive Streamlit dashboard.

## Objectives

- Explore and understand recipe and user rating data.
- Perform data cleaning and statistical analysis.
- Implement and compare different recipe-ranking methods.
- Analyze user ratings and recipe popularity.
- Visualize recipe rankings and rating distributions.
- Develop an interactive dashboard using Streamlit.

## Ranking Methods

1. **Average Rating:** Calculates the arithmetic mean of user ratings for each recipe.
2. **Median Rating:** Calculates the middle value of user ratings, reducing the influence of unusually high or low ratings.
3. **Bayesian Weighted Rating:** Combines the average rating, number of user ratings, and overall dataset average to generate a more reliable ranking.

The Bayesian method helps prevent recipes with very few ratings from dominating the rankings.

For the final rankings, only recipes with at least 10 user ratings are considered. This helps reduce the influence of recipes with very limited rating data.

## Project Structure

```text
Food_Recipe_Insight/
│
├── app/
│   └── streamlit_app.py
│
├── assets/
│   └── style.css
│
├── data/
│   ├── raw/
│   │   ├── RAW_recipes.csv
│   │   └── RAW_interactions.csv
│   │
│   └── processed/
│       └── processed_recipe_data.csv
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── outputs/
│   ├── figures/
│   └── rankings/
│       └── recipe_rankings.csv
│
├── src/
│   ├── __init__.py
│   ├── recipe_analysis.py
│   └── test_recipe_analysis.py
│
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

### Folder Description

- `app/`: Contains the Streamlit dashboard application.
- `assets/`: Contains CSS files for dashboard styling.
- `data/raw/`: Contains the original Food.com datasets.
- `data/processed/`: Contains cleaned and processed recipe data.
- `notebooks/`: Contains exploratory data analysis.
- `outputs/figures/`: Stores generated visualizations.
- `outputs/rankings/`: Stores recipe ranking results.
- `src/`: Contains data processing functions and unit tests.

## Technologies and Libraries

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Streamlit
- Git and Git LFS

## Dataset

This project uses two datasets from Food.com:

- `RAW_recipes.csv` – Contains recipe information.
- `RAW_interactions.csv` – Contains user ratings and reviews.

The datasets are stored in `data/raw/` and tracked using Git Large File Storage (Git LFS).

The dataset is publicly available on Kaggle:

[Food.com Recipes and Interactions Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/RishiKarthikeyaReddy/Food_Recipe_Insight.git
cd Food_Recipe_Insight
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment (Windows)

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Dashboard

Start the Streamlit application using:

```bash
python -m streamlit run app/streamlit_app.py
```

The interactive dashboard allows users to explore recipe rankings based on Average Rating, Median Rating, and Bayesian Weighted Rating.

## Outputs and Validation

The project generates a recipe rankings CSV file:

`outputs/rankings/recipe_rankings.csv`

The output contains:

- Recipe ID
- Average Rating
- Median Rating
- Rating Count
- Rating Standard Deviation
- Bayesian Rating
- Average Rank
- Bayesian Rank

The generated rankings were reviewed to ensure that the recipe statistics and ranking results were produced correctly.

## Testing

The project includes a test module:

`src/test_recipe_analysis.py`

It is used to validate the recipe analysis functionality.

Run the tests from the project root directory using:

```bash
python -m pytest src/test_recipe_analysis.py -v
```

## Author

**Rishi Karthikeya Reddy Kavalakuntla**

Data Science Project | Python | Data Analysis | Statistical Ranking
# Food Recipe Insight

## Project Overview
Food Recipe Insight is a Python-based data science project that analyzes Food.com recipe and user interaction data. It ranks recipes using three different rating methods and presents the results through an interactive Streamlit dashboard.

## Objectives
- Explore and understand recipe and rating data.
- Perform data cleaning and statistical analysis.
- Compare different recipe-ranking methods.
- Visualize recipe ratings and rankings.
- Build an interactive dashboard for exploring recipes.

## Ranking Methods
1. **Average Rating:** Calculates the mean user rating for each recipe.
2. **Median Rating:** Calculates the middle user rating for each recipe.
3. **Bayesian Weighted Rating:** Combines a recipe's average rating and number of ratings to produce a more reliable ranking.

## Project Structure

```text
Food-Recipe-Insight/
├── app/
│   └── streamlit_app.py
├── data/
│   └── raw/
│       ├── RAW_interactions.csv
│       └── RAW_recipes.csv
├── notebooks/
│   └── 01_data_exploration.ipynb
├── outputs/
│   ├── figures/
│   └── rankings/
├── src/
│   ├── __init__.py
│   ├── recipe_analysis.py
│   └── test_recipe_analysis.py
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

## Technologies and Libraries
- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Streamlit
- Git and Git LFS

## Dataset
The project uses Food.com recipe and interaction datasets:
- `RAW_recipes.csv`
- `RAW_interactions.csv`

The CSV files are stored in `data/raw/` and tracked using Git LFS.

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/RishiKarthikeyaReddy/Food_Recipe_Insight.git
cd Food-Recipe-Insight
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
python -m streamlit run app/streamlit_app.py
```

The dashboard allows users to explore recipe rankings using Average Rating, Median Rating, and Bayesian Weighted Rating.

## Author
Developed as a data science project using Python.

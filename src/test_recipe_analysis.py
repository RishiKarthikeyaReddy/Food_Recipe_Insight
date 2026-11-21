from pathlib import Path

from recipe_analysis import (
    load_data,
    calculate_recipe_stats,
    calculate_bayesian_rating
)


# Get the main project folder
project_path = Path(__file__).resolve().parent.parent

# Dataset paths
recipes_path = project_path / "data" / "raw" / "RAW_recipes.csv"
interactions_path = project_path / "data" / "raw" / "RAW_interactions.csv"


# Load datasets
recipes, interactions = load_data(recipes_path, interactions_path)

if recipes is not None and interactions is not None:

    # Calculate overall average rating
    overall_mean = interactions.loc[
        interactions["rating"] > 0, "rating"
    ].mean()

    # Calculate recipe statistics
    recipe_stats = calculate_recipe_stats(interactions)

    # Calculate Bayesian ratings
    recipe_stats = calculate_bayesian_rating(
        recipe_stats, overall_mean
    )

    print("Datasets loaded successfully!")
    print("\nRecipe statistics:")
    print(recipe_stats.head())

    print("\nTotal recipes:", len(recipe_stats))

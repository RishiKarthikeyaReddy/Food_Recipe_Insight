import pandas as pd


def load_data(recipes_path, interactions_path):
    """
    Load recipe and user interaction datasets.

    Parameters:
        recipes_path: Path to the recipes CSV file.
        interactions_path: Path to the interactions CSV file.

    Returns:
        recipes and interactions DataFrames.
    """
    try:
        recipes = pd.read_csv(recipes_path)
        interactions = pd.read_csv(interactions_path)

        return recipes, interactions

    except FileNotFoundError:
        print("Error: Dataset file not found.")
        return None, None


def calculate_recipe_stats(interactions):
    """
    Calculate rating statistics for each recipe.

    Parameters:
        interactions: DataFrame containing user interactions
                      and recipe ratings.

    Returns:
        DataFrame containing recipe ID, average rating,
        median rating, rating count, and rating standard deviation.
    """
    rated_interactions = interactions[
        interactions["rating"] > 0
    ].copy()

    recipe_stats = rated_interactions.groupby(
        "recipe_id"
    )["rating"].agg(
        ["mean", "median", "count", "std"]
    ).reset_index()

    recipe_stats.columns = [
        "recipe_id",
        "average_rating",
        "median_rating",
        "rating_count",
        "rating_std"
    ]

    return recipe_stats


def calculate_bayesian_rating(recipe_stats, overall_mean, m=10):
    """
    Calculate Bayesian weighted ratings for recipes.

    Parameters:
        recipe_stats: DataFrame containing average ratings and rating counts.
        overall_mean: Overall average rating across all rated interactions.
        m: Smoothing parameter controlling the influence of the overall mean.

    Returns:
        DataFrame containing Bayesian weighted ratings.
    """
    recipe_stats = recipe_stats.copy()

    recipe_stats["bayesian_rating"] = (
        (recipe_stats["rating_count"] /
         (recipe_stats["rating_count"] + m))
        * recipe_stats["average_rating"]
        +
        (m / (recipe_stats["rating_count"] + m))
        * overall_mean
    )

    return recipe_stats


def save_processed_data(recipe_stats, recipes, output_path):
    """
    Merge recipe statistics with recipe names and save the data.

    Parameters:
        recipe_stats: DataFrame containing calculated recipe statistics.
        recipes: DataFrame containing recipe IDs and names.
        output_path: File path where the processed CSV will be saved.

    Returns:
        DataFrame containing processed recipe information and statistics.
    """
    processed_data = recipe_stats.merge(
        recipes[["id", "name"]],
        left_on="recipe_id",
        right_on="id",
        how="left"
    )

    processed_data = processed_data[
        [
            "recipe_id",
            "name",
            "average_rating",
            "median_rating",
            "rating_count",
            "rating_std",
            "bayesian_rating"
        ]
    ]

    processed_data = processed_data.rename(
        columns={"name": "recipe_name"}
    )

    processed_data.to_csv(output_path, index=False)

    return processed_data


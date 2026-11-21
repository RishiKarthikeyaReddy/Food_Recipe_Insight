
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

from src.recipe_analysis import (
    load_data,
    calculate_recipe_stats,
    calculate_bayesian_rating
)

# Page configuration
st.set_page_config(
    page_title="Food Recipe Insight",
    page_icon="🍽️",
    layout="wide"
)

# Project title
st.title("🍽️ Food Recipe Insight")
st.subheader("Recipe Analysis and Intelligent Ranking System")
st.write(
    "Food Recipe Insight is an interactive data science application "
    "that explores Food.com recipe and user interaction data. "
    "It analyzes recipe ratings using Average Rating, Median Rating, "
    "and Bayesian Weighted Rating to generate meaningful recipe rankings. "
    "Users can explore recipe insights, compare ranking methods, "
    "and discover highly rated recipes through interactive visualizations."
)

# Load datasets
recipes_path = "data/raw/RAW_recipes.csv"
interactions_path = "data/raw/RAW_interactions.csv"

try:
    recipes, interactions = load_data(
        recipes_path,
        interactions_path
    )

    # Dataset overview
    st.header("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Recipes", f"{len(recipes):,}")
    col2.metric("Total Reviews", f"{len(interactions):,}")

    # Calculate overall average rating
    overall_mean = interactions.loc[
        interactions["rating"] > 0, "rating"
    ].mean()

    col3.metric("Average Rating", f"{overall_mean:.2f} / 5")

    # Calculate recipe statistics
    recipe_stats = calculate_recipe_stats(interactions)

    # Keep recipes with at least 10 ratings
    filtered_recipes = recipe_stats[
        recipe_stats["rating_count"] >= 10
    ].copy()

    # Calculate Bayesian weighted rating
    filtered_recipes = calculate_bayesian_rating(
        filtered_recipes,
        overall_mean
    )

    # Rating distribution
    st.header("⭐ User Rating Distribution")

    rating_distribution = (
        interactions.loc[
            interactions["rating"] > 0, "rating"
        ].value_counts().sort_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        rating_distribution.index.astype(str),
        rating_distribution.values
    )

    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Number of Ratings")
    ax.set_title("Distribution of User Ratings")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Recipe search
    st.header("🔍 Search for a Recipe")

    search_name = st.text_input("Enter a recipe name:")

    if search_name:
        search_results = filtered_recipes.merge(
            recipes[["id", "name"]],
            left_on="recipe_id",
            right_on="id",
            how="left"
        )

        search_results = search_results[
            search_results["name"].str.contains(
                search_name,
                case=False,
                na=False
            )
        ]

        if not search_results.empty:

            st.dataframe(
                search_results[
                    ["recipe_id", "name", "average_rating",
                     "rating_count", "bayesian_rating"]
                ].head(10),
                width="stretch"
            )

            # Select a recipe to view details
            selected_recipe_id = st.selectbox(
                "Select a recipe to view details:",
                search_results["recipe_id"].head(10)
            )

            recipe_details = recipes[
                recipes["id"] == selected_recipe_id
            ].iloc[0]

            st.subheader(recipe_details["name"])

            col1, col2 = st.columns(2)

            col1.metric(
                "Cooking Time",
                f"{recipe_details['minutes']} minutes"
            )

            col2.metric(
                "Number of Ingredients",
                recipe_details["n_ingredients"]
            )

            st.write("**Ingredients:**")
            st.write(recipe_details["ingredients"])

            # Display preparation steps
            st.write("**Preparation Steps:**")

            try:
                steps = ast.literal_eval(recipe_details["steps"])

                for step_number, step in enumerate(steps, start=1):
                    st.write(f"**Step {step_number}:** {step}")

            except (ValueError, SyntaxError, TypeError):
                st.warning("Preparation steps are unavailable.")

        else:
            st.warning("No matching recipes found.")

    # Explain ranking methods
    st.header("📖 How Does Recipe Ranking Work?")

    st.subheader("1. Average Rating")

    st.write(
        "This method calculates the average rating given by users "
        "for each recipe. However, it does not consider how many "
        "users rated the recipe."
    )

    st.subheader("2. Median Rating")

    st.write("This method calculates the middle rating given by users "
             "for each recipe. It is less affected by unusually high "
             "or low ratings, but does not consider how many users "
             "rated the recipe."
             )

    st.subheader("3. Bayesian Weighted Rating")

    st.write(
        "This method considers both the average rating and the "
        "number of ratings. Recipes with fewer ratings are adjusted "
        "towards the overall average rating, making the ranking "
        "more reliable."
    )

    st.info(
        "Only recipes with at least 10 ratings are included "
        "in the ranking."
    )

    # Recipe rankings
    st.header("🏆 Recipe Rankings")

    ranking_method = st.selectbox(
        "Choose a ranking method:",
        ["Average Rating", "Median Rating", "Bayesian Rating"]
    )

    # Select ranking method
    if ranking_method == "Average Rating":
        ranking_column = "average_rating"

    elif ranking_method == "Median Rating":
        ranking_column = "median_rating"

    else:
        ranking_column = "bayesian_rating"

    # Get top 10 recipes
    top_recipes = filtered_recipes.sort_values(
        ranking_column,
        ascending=False
    ).head(10)

    # Add recipe names
    top_recipes = top_recipes.merge(
        recipes[["id", "name"]],
        left_on="recipe_id",
        right_on="id",
        how="left"
    )

    # Select columns for display
    top_recipes = top_recipes[
        ["recipe_id", "name", "average_rating", "median_rating",
         "rating_count", "bayesian_rating"]
    ]

    # Display ranking table
    st.subheader(f"Top 10 Recipes by {ranking_method}")

    st.dataframe(
        top_recipes,
        width="stretch"
    )

    # Display ranking chart
    st.subheader("📈 Recipe Ranking Chart")

    if ranking_method == "Average Rating":
        chart_column = "average_rating"

    elif ranking_method == "Median Rating":
        chart_column = "median_rating"

    else:
        chart_column = "bayesian_rating"

    chart_data = top_recipes.sort_values(
        chart_column,
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.barh(
        chart_data["recipe_id"].astype(str),
        chart_data[chart_column]
    )

    ax.set_xlabel(ranking_method)
    ax.set_xlim(4, 5.1)
    ax.set_ylabel("Recipe ID")
    ax.set_title(f"Top 10 Recipes by {ranking_method}")
    ax.set_xlim(4, 5.1)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

except FileNotFoundError:
    st.error(
        "Dataset files not found. Please check the data/raw folder."
    )

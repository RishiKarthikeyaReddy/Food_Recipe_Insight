
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

from src.recipe_analysis import (
    load_data,
    calculate_recipe_stats,
    calculate_bayesian_rating,
    save_processed_data
)

# Page configuration
st.set_page_config(
    page_title="Food Recipe Insight",
    page_icon="🍽️",
    layout="wide"
)

# Load external CSS file
with open("Assets/style.css") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
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

    # Save processed recipe data
    processed_path = "data/processed/processed_recipe_data.csv"

    save_processed_data(
        filtered_recipes,
        recipes,
        processed_path
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
    ranking_limit = st.selectbox(
    "How many recipes do you want to see?",
    [10, 20]
    )

    # Select ranking method
    if ranking_method == "Average Rating":
        ranking_column = "average_rating"

    elif ranking_method == "Median Rating":
        ranking_column = "median_rating"

    else:
        ranking_column = "bayesian_rating"

    # Get top recipes based on selected limit
    top_recipes = filtered_recipes.sort_values(
        ranking_column,
        ascending=False
        ).head(ranking_limit)

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
    st.subheader(f"Top {ranking_limit} Recipes by {ranking_method}")

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
    ax.set_title(f"Top {ranking_limit} Recipes by {ranking_method}")
    ax.set_xlim(4, 5.1)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Ranking Comparison
    st.header("📊 Ranking Method Comparison")

    st.write(
    "Compare how different ranking methods evaluate recipes "
    "and identify differences in their rankings."
    )

        # Calculate rankings for each method
    average_ranking = filtered_recipes.sort_values(
        ["average_rating", "rating_count"],
        ascending=[False, False]
    ).copy()

    median_ranking = filtered_recipes.sort_values(
        ["median_rating", "average_rating", "rating_count"],
        ascending=[False, False, False]
    ).copy()

    bayesian_ranking = filtered_recipes.sort_values(
        "bayesian_rating",
        ascending=False
    ).copy()

        # Add ranking positions
    average_ranking["average_rank"] = range(
        1, len(average_ranking) + 1
    )

    median_ranking["median_rank"] = range(
        1, len(median_ranking) + 1
    )

    bayesian_ranking["bayesian_rank"] = range(
        1, len(bayesian_ranking) + 1
    )

        # Combine all ranking results
    ranking_comparison = average_ranking[
        ["recipe_id", "average_rating", "average_rank"]
    ].merge(
        median_ranking[
            ["recipe_id", "median_rating", "median_rank"]
        ],
        on="recipe_id"
    ).merge(
        bayesian_ranking[
            ["recipe_id", "bayesian_rating", "bayesian_rank"]
        ],
        on="recipe_id"
    )

            # Select comparison size
    comparison_limit = st.selectbox(
        "Choose comparison size:",
        [10, 20]
    )

    # Display ranking comparison
    st.subheader(
        f"Top {comparison_limit} Recipes: Ranking Comparison"
    )

    comparison_results = ranking_comparison.sort_values(
        "bayesian_rank",
        ascending=True
    ).head(comparison_limit)

    # Add recipe names
    comparison_results = comparison_results.merge(
        recipes[["id", "name"]],
        left_on="recipe_id",
        right_on="id",
        how="left"
    )

    # Select columns for display
    comparison_results = comparison_results[
        [
            "recipe_id",
            "name",
            "average_rating",
            "average_rank",
            "median_rating",
            "median_rank",
            "bayesian_rating",
            "bayesian_rank"
        ]
    ]

    # Display comparison table
    st.dataframe(
        comparison_results,
        width="stretch"
    )

            # Find common recipes in selected Top N rankings
    average_top = set(
        average_ranking.head(comparison_limit)["recipe_id"]
    )

    median_top = set(
        median_ranking.head(comparison_limit)["recipe_id"]
    )

    bayesian_top = set(
        bayesian_ranking.head(comparison_limit)["recipe_id"]
    )

    common_recipes = (
        average_top
        & median_top
        & bayesian_top
    )

    st.subheader(
        f"Common Recipes Across All Three Top {comparison_limit} Rankings"
    )

    st.metric(
        f"Recipes appearing in all three Top {comparison_limit} lists",
        len(common_recipes)
    )

    # Compare overlap between each pair of ranking methods
    common_average_median = average_top & median_top
    common_average_bayesian = average_top & bayesian_top
    common_median_bayesian = median_top & bayesian_top

    st.subheader("Pairwise Ranking Comparison")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average vs Median",
        len(common_average_median)
    )

    col2.metric(
        "Average vs Bayesian",
        len(common_average_bayesian)
    )

    col3.metric(
        "Median vs Bayesian",
        len(common_median_bayesian)
    )

        # Ranking Movement Analysis
    st.subheader("Ranking Movement Analysis")

    # Combine ranking positions
    movement_analysis = average_ranking[
        ["recipe_id", "average_rank"]
    ].merge(
        median_ranking[["recipe_id", "median_rank"]],
        on="recipe_id"
    ).merge(
        bayesian_ranking[["recipe_id", "bayesian_rank"]],
        on="recipe_id"
    )

    # Calculate ranking movement
    movement_analysis["average_to_bayesian_change"] = (
        movement_analysis["average_rank"]
        - movement_analysis["bayesian_rank"]
    )

    movement_analysis["median_to_bayesian_change"] = (
        movement_analysis["median_rank"]
        - movement_analysis["bayesian_rank"]
    )

        # Add recipe names
    movement_analysis = movement_analysis.merge(
        recipes[["id", "name"]],
        left_on="recipe_id",
        right_on="id",
        how="left"
    )

    movement_analysis = movement_analysis.rename(
        columns={"name": "recipe_name"}
    )

    # Arrange columns and remove duplicate id
    movement_analysis = movement_analysis[
        [
            "recipe_id",
            "recipe_name",
            "average_rank",
            "median_rank",
            "bayesian_rank",
            "average_to_bayesian_change",
            "median_to_bayesian_change"
        ]
    ]

    st.write(
        "Positive values indicate that a recipe ranks higher "
        "in the Bayesian method than in the other method."
    )

    st.dataframe(
        movement_analysis.sort_values(
            "average_to_bayesian_change",
            ascending=False
        ).head(10).reset_index(drop=True),
        width="stretch"
    )

except FileNotFoundError:
    st.error(
        "Dataset files not found. Please check the data/raw folder."
    )
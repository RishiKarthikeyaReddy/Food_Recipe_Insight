
import unittest
import pandas as pd

from src.recipe_analysis import (
    calculate_recipe_stats,
    calculate_bayesian_rating
)


class TestRecipeAnalysis(unittest.TestCase):

    def setUp(self):
        self.interactions = pd.DataFrame({
            "recipe_id": [1, 1, 1, 2, 2, 3],
            "rating": [5, 4, 3, 5, 0, 2]
        })

    def test_calculate_recipe_stats(self):
        result = calculate_recipe_stats(self.interactions)

        self.assertEqual(len(result), 3)

        recipe_1 = result[result["recipe_id"] == 1].iloc[0]

        self.assertEqual(recipe_1["average_rating"], 4)
        self.assertEqual(recipe_1["median_rating"], 4)
        self.assertEqual(recipe_1["rating_count"], 3)

    def test_zero_ratings_are_excluded(self):
        result = calculate_recipe_stats(self.interactions)

        recipe_2 = result[result["recipe_id"] == 2].iloc[0]

        self.assertEqual(recipe_2["rating_count"], 1)
        self.assertEqual(recipe_2["average_rating"], 5)

    def test_calculate_bayesian_rating(self):
        recipe_stats = pd.DataFrame({
            "recipe_id": [1],
            "average_rating": [4.0],
            "rating_count": [10]
        })

        result = calculate_bayesian_rating(
            recipe_stats,
            overall_mean=3.5,
            m=10
        )

        self.assertAlmostEqual(
            result.loc[0, "bayesian_rating"],
            3.75
        )


if __name__ == "__main__":
    unittest.main()

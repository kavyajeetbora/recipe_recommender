import numpy as np


def cosine_similarity(vec1, vec2):
    """
    Returns the cosine similarity between two vectors of n dimension
    """
    denom = np.sqrt(np.sum(np.square(vec1))) * np.sqrt(np.sum(np.square(vec2)))
    return np.round(np.dot(vec1, vec2) / denom * 100, 2)


def find_similar_recipe(recipe, df, num_recipes):
    if recipe in df["name"].to_list():
        index = df[df["name"] == recipe].index[0]

        data = df.iloc[index]
        recipe, vector = data["name"], data["embedding"]

        ## Find similar recipe
        df_result = df.copy()
        df_result["similarity"] = df_result["embedding"].apply(
            lambda x: cosine_similarity(vector, x)
        )
        df_result = df_result.sort_values(by="similarity", ascending=False).iloc[
            1 : num_recipes + 1
        ]
        df_result.drop("embedding", inplace=True, axis=1)

        return df_result

    else:
        return None

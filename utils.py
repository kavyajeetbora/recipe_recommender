import numpy as np
import plotly.graph_objects as go


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


def setColor(pdv):
    if pdv < 5:
        return "red"

    elif pdv >= 5 and pdv < 20:
        return "red"

    elif pdv > 20:
        return "red"


def plot_nutrition(data):
    x = data.index[8:13]
    y = data.values[8:13]

    fig = go.Figure(
        go.Bar(
            name="",
            x=x,
            y=y,
            width=0.2,
            uirevision=True,
            # marker=dict(color=list(map(setColor, y))),
            hovertemplate="<br><b>%{x}</b>: %{y:.2f}",
        ),
    )
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        width=500,
        height=200,
    )
    fig.update_xaxes(
        showgrid=False,
    )
    # fig.update_yaxes(
    #     showgrid=False,
    #     showticklabels=False
    # )
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    return fig

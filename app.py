import streamlit as st
from glob import glob
import pandas as pd
import utils

## Session state variables
## -------------------------------------------------------------------

if "data" not in st.session_state:
    files = glob(r"data\*.parquet")
    df = pd.read_parquet(files)
    df["ingredients"] = (
        df["ingredients"]
        .str.strip("[]")
        .str.replace("'", "")
        .str.replace('"', "")
        .str.split(",")
        .apply(lambda x: [y.strip() for y in x])
    )

    st.session_state["data"] = df

## App Layout
## -------------------------------------------------------------------

st.header("Food Recipe Recommeder")
st.text("Search similary recipes based on their ingredients")

recipe = st.selectbox(
    label="Search the recipe:", options=st.session_state["data"]["name"]
)
num_recipes = st.slider(label="Number of similar recipes", min_value=3, max_value=10)

## Find similarity
## -------------------------------------------------------------------

if "result" not in st.session_state:
    st.session_state["result"] = None


def assign_values():
    st.session_state["result"] = utils.find_similar_recipe(
        recipe, st.session_state["data"], num_recipes
    )


search = st.button(label="Search", on_click=assign_values)


## Display the results
## -------------------------------------------------------------------

x = st.session_state["data"].iloc[0]
if search:
    for row_index in range(st.session_state["result"].shape[0]):
        dfx = st.session_state["result"].iloc[row_index]

        with st.expander(dfx["name"]):
            tab_1, tab_2, tab_3 = st.tabs(["Summary", "Ingredients", "Recipe"])

            with tab_1:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="Calories", value=dfx["calories"])

                with col2:
                    st.metric(label="Number of Steps", value=dfx["n_steps"])

                with col3:
                    st.metric(label="Number of Ingredients", value=dfx["n_ingredients"])

                with col4:
                    st.metric(label="Minutes", value=dfx["minutes"])

            with tab_2:
                st.text(f"Number of Ingredients: {dfx['n_ingredients']}")
                for step in dfx["ingredients"]:
                    st.markdown(f"- {step}")

            with tab_3:
                st.text(f"Recipe")
                for step in dfx["steps"]:
                    st.markdown(f"- {step}")


# if st.session_state["result"] is not None:
#     st.dataframe(st.session_state["result"])

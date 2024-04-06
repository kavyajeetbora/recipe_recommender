import streamlit as st
from glob import glob
import pandas as pd
import utils

## STREAMLIT CONFIGURATION
## --------------------------------------------------------------------------------##
st.set_page_config(
    page_title="Food Recipe Recommeder", page_icon=r"images/logo-color.ico"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

## Session state variables
## -------------------------------------------------------------------

if "data" not in st.session_state:
    files = glob(r"data/*.parquet")
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

st.image(r"images/logo-no-background.png", width=400)

recipe = st.selectbox(
    label="Search the recipe:", options=st.session_state["data"]["name"], index=100
)

col1, col2 = st.columns([1, 3])
with col1:
    num_recipes = st.number_input(
        label="Number of similar recipes", min_value=3, max_value=10, step=1
    )
# num_recipes = st.slider(label="Number of similar recipes", min_value=3, max_value=10)

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
    for i, row_index in enumerate(range(st.session_state["result"].shape[0])):
        dfx = st.session_state["result"].iloc[row_index]

        with st.expander(
            f"{i+1}. "
            + f"{dfx['name'].capitalize()} | Similarity :blue[{dfx['similarity']}] %"
        ):
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
                    st.metric(label="Cooking Time", value=f"{dfx['minutes']} Mins")

                fig = utils.plot_nutrition(dfx)
                st.plotly_chart(fig)

            with tab_2:
                st.text(f"Number of Ingredients: {dfx['n_ingredients']}")
                for i, step in enumerate(dfx["ingredients"]):
                    st.markdown(f"{i+1}. {step}")

            with tab_3:
                st.text(f"Recipe")
                for i, step in enumerate(dfx["steps"]):
                    st.markdown(f"{i+1}. {step}")

    #  del st.session_state["data"]

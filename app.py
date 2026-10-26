"""Developmental Biology & Disease Research Explorer — main entry point.

Run with:  streamlit run app.py
"""
import streamlit as st

from modules import (
    bioinformatics,
    cell_development,
    disease_research,
    genetics,
    home,
    model_systems,
    navigation as nav,
    quiz,
    sources,
    virtual_lab,
)

st.set_page_config(page_title="Developmental Biology Research Explorer", page_icon="🧬", layout="wide")

PAGES = {
    nav.CELL: cell_development.render,
    nav.GENETICS: genetics.render,
    nav.MODELS: model_systems.render,
    nav.DISEASE: disease_research.render,
    nav.LAB: virtual_lab.render,
    nav.BIOINFO: bioinformatics.render,
    nav.QUIZ: quiz.render,
    nav.SOURCES: sources.render,
}


def go_to(page_name: str) -> None:
    """Callback used by buttons on the home page to change the page."""
    st.session_state["nav_page"] = page_name


if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = nav.HOME

st.sidebar.title("🧬 Research Explorer")
st.sidebar.radio("Navigate", nav.PAGE_ORDER, key="nav_page")
st.sidebar.caption(
    "Educational project. Simulated data are always labelled. Not medical advice."
)

current = st.session_state["nav_page"]
if current == nav.HOME:
    home.render(go_to)
else:
    PAGES[current]()

"""Home page: purpose, research workflow, module cards and example research questions."""
from __future__ import annotations

import textwrap

from modules import navigation as nav

WORKFLOW_STEPS = [
    "Identify a biological question",
    "Review what is already known",
    "Develop a hypothesis",
    "Select a suitable model and method",
    "Collect observations or measurements",
    "Analyse the data",
    "Interpret results and limitations",
    "Identify the next research question",
]


def workflow_dot() -> str:
    """Graphviz description of the research cycle (drawn in the browser by Streamlit)."""
    lines = ["digraph G {", "rankdir=LR;", 'node [shape=box, style="rounded,filled", fillcolor="#eaf3f0", fontname="Helvetica", fontsize=11];']
    for i, step in enumerate(WORKFLOW_STEPS, 1):
        label = "\\n".join(textwrap.wrap(f"{i}. {step}", 24))  # '\\n' is a line break inside a DOT label
        lines.append(f'n{i} [label="{label}"];')
    for i in range(1, len(WORKFLOW_STEPS)):
        lines.append(f"n{i} -> n{i + 1};")
    lines.append(f'n{len(WORKFLOW_STEPS)} -> n1 [style=dashed, label="new question"];')
    lines.append("}")
    return "\n".join(lines)


CARDS = [
    (nav.CELL, "Cell biology & development", "From fertilised egg to organs: the cell cycle, differentiation, stem cells and signalling."),
    (nav.GENETICS, "Genetics & molecular biology", "Analyse DNA, follow transcription and translation, explore mutations and gene expression."),
    (nav.MODELS, "Model systems & zebrafish", "Why researchers use zebrafish, flies, worms, mice, yeast, human cells and organoids."),
    (nav.DISEASE, "Disease & human biology", "Neural and heart development, regeneration and genetic disease."),
    (nav.LAB, "Virtual research lab", "Practise interpreting (fictional) experimental data."),
    (nav.BIOINFO, "Beginner bioinformatics", "Compare sequences and meet the ideas behind real tools."),
    (nav.QUIZ, "Knowledge check", "Test your reasoning with explained questions."),
    (nav.SOURCES, "Sources & limitations", "Where to read more and what this app cannot do."),
]

EXPLORE = [
    ("How do cells become specialised?", "Cells in one body share broadly the same genome but switch different sets of genes on and off, guided by signals from their surroundings.", nav.CELL),
    ("How can a change in DNA affect a protein?", "A change in a coding sequence can alter a codon, which may change an amino acid, introduce a stop, or shift the reading frame. Try it with fictional sequences.", nav.GENETICS),
    ("How do researchers study the formation of organs?", "They watch development with imaging, change gene activity and observe the consequences, and grow organ-like structures in dishes.", nav.CELL),
    ("Why are zebrafish useful in developmental biology?", "Their embryos develop outside the mother and are transparent early on, so tissues can be watched forming in a living vertebrate.", nav.MODELS),
    ("How can a model organism help investigate human disease?", "A model can show what a gene does in a living system and suggest mechanisms to test, though results must be checked for relevance to humans.", nav.DISEASE),
    ("How can scientists distinguish a genuine pattern from experimental noise?", "By using controls, replication, appropriate statistics and cautious interpretation. Practise in the virtual lab.", nav.LAB),
]


def render(go_to) -> None:
    """``go_to(page_name)`` is a callback that switches the page."""
    import streamlit as st

    st.title("Developmental Biology & Disease Research Explorer")
    st.subheader("How do scientists study the processes that build and maintain living organisms?")
    st.write(
        "Researchers combine **microscopy and imaging**, **genetics**, **molecular biology**, **cell culture**, **model organisms**, "
        "**computational analysis** and careful **experimental design** to investigate how genes, cells, development and disease are connected. "
        "This app lets you explore those ideas with interactive tools."
    )
    st.info(
        "Clearly labelled throughout: **established background** (simplified), **simulated data** (invented for teaching) and the app's own interpretations. "
        "This is an educational project, not a source of medical advice."
    )

    st.markdown("### The research workflow")
    st.graphviz_chart(workflow_dot())
    st.caption("Real research loops back: results usually raise new questions.")

    st.markdown("### Modules")
    columns = st.columns(2)
    for index, (page, title, text) in enumerate(CARDS):
        with columns[index % 2].container(border=True):
            st.markdown(f"**{title}**")
            st.write(text)
            st.button("Open", key=f"card_{index}", on_click=go_to, args=(page,))

    st.markdown("### Explore a research question")
    for index, (question, answer, page) in enumerate(EXPLORE):
        with st.expander(question):
            st.write(answer)
            st.button("Go to the related module", key=f"explore_{index}", on_click=go_to, args=(page,))

"""Module E: Disease and human biology.

Educational background and fictional examples only. Nothing here diagnoses a condition,
predicts a person's outcome or recommends a treatment.
"""
from __future__ import annotations

THEMES = {
    "Neural development": {
        "question": "How do progenitor cells become neurons, and how do neurons connect into circuits?",
        "concepts": ["Neural induction and neural tube formation", "Neural progenitor cells and neurogenesis", "Axon guidance and synapse formation", "Cell-cell signalling"],
        "methods": ["Fluorescent labelling of neurons and live imaging", "Changing gene activity and observing neuron numbers", "Single-cell RNA sequencing to identify cell types", "Recording electrical activity"],
        "model": "Zebrafish (transparent embryos allow neurons to be watched forming), mouse (mammalian brain), and human stem-cell-derived neurons or brain organoids.",
        "hypothetical": "HYPOTHETICAL: In a made-up experiment, reducing the activity of a fictional gene 'NEURO-X' leaves fewer labelled neurons and more unspecialised progenitor cells. One interpretation is that the gene helps progenitors commit to a neuron fate.",
        "limitations": "Simple models cannot reproduce the size and complexity of the human brain; organoids are immature; behavioural and cognitive effects are very hard to model.",
        "think": "What other explanation could produce fewer labelled neurons besides 'the gene helps progenitors commit'?",
    },
    "Heart development": {
        "question": "How do developing cells organise into a heart that pumps blood, and what happens when the process changes?",
        "concepts": ["Cardiac progenitors and the heart tube", "Looping and chamber formation", "Valve formation", "Forces from blood flow influence development"],
        "methods": ["Fluorescent reporters for heart cells", "Imaging heartbeat and blood flow", "Changing gene activity and scoring heart shape", "Stem-cell-derived heart muscle cells in dishes"],
        "model": "Zebrafish (early embryos can be imaged while the heart forms and can survive a period without full blood circulation because oxygen reaches the tissues by diffusion), mouse, and human stem-cell-derived heart cells.",
        "hypothetical": "HYPOTHETICAL: In a made-up experiment, reducing a fictional gene 'HEART-Y' produces a heart tube that fails to loop. Chamber shape is abnormal.",
        "limitations": "The zebrafish heart has two main chambers, whereas the human heart has four, so some defects cannot be modelled in the same way.",
        "think": "How could you tell whether abnormal looping came from the gene's own role or indirectly from altered blood flow?",
    },
    "Regeneration": {
        "question": "Why can some organisms and tissues repair or replace lost cells much better than others?",
        "concepts": ["Injury response and signalling", "Progenitor cells and cells that re-enter the cell cycle", "Scar formation versus tissue replacement", "Differences in regenerative ability between species and tissues"],
        "methods": ["Labelling cells to trace where new cells come from (lineage tracing)", "Measuring regrowth over time", "Comparing gene activity before and after injury", "Altering signalling pathways in animals under ethical oversight"],
        "model": "Zebrafish (can regrow fins and repair some heart tissue), other regenerating species such as salamanders and planarian worms, compared with mammals.",
        "hypothetical": "HYPOTHETICAL: In a made-up experiment, blocking a fictional signalling pathway slows regrowth of a tissue compared with a control group.",
        "limitations": "Regeneration varies widely across species and tissues, so a mechanism in fish may not work in humans; the evolutionary reasons for these differences remain debated.",
        "think": "Why might the ability to regenerate differ between species? Suggest a hypothesis and say what evidence would test it.",
    },
    "Genetic disease": {
        "question": "How can a change in DNA alter a protein or pathway, and why do outcomes vary between people?",
        "concepts": ["Genetic variants and their effects on proteins (loss or gain of function)", "Inheritance patterns", "Penetrance and variable expression", "Modifier genes and environment"],
        "methods": ["DNA sequencing and family studies", "Cells made from patients' own cells (with consent)", "Model organisms carrying an equivalent change", "Laboratory tests of protein function"],
        "model": "Depends on the question: patient-derived cells for protein function in human cells, zebrafish or mice for effects on development or whole-body physiology.",
        "hypothetical": "HYPOTHETICAL: In a made-up experiment, a fictional variant in 'GENE-Z' makes a protein less stable in cultured cells, and animals with reduced activity of the matching gene show a smaller tissue. Together these would suggest, but not prove, a link.",
        "limitations": "A model cannot predict an individual's medical outcome. Many conditions involve several genes and the environment.",
        "think": "Why might two people with the same genetic variant have different outcomes?",
        "established": "**Established background:** sickle-cell disease is associated with a single-base change in the gene for the β-globin part of haemoglobin, which changes one amino acid and alters how the protein behaves. Even for this well-studied example, severity varies between individuals.",
    },
}


def render() -> None:
    import streamlit as st

    from modules.ui_helpers import background_notice

    st.title("Disease & human biology")
    st.write("Research on development and molecular mechanisms helps scientists form and test ideas about how disease processes arise.")
    st.error(
        "**This is an educational tool, not medical advice.** It does not diagnose conditions, predict anyone's health or recommend treatments."
    )
    theme = st.radio("Choose a theme", list(THEMES), horizontal=True, key="disease_theme")
    info = THEMES[theme]
    st.subheader(theme)
    st.markdown(f"**Research question:** {info['question']}")
    c1, c2 = st.columns(2)
    c1.markdown("**Relevant biological concepts**\n" + "\n".join(f"- {c}" for c in info["concepts"]))
    c2.markdown("**Example research methods**\n" + "\n".join(f"- {m}" for m in info["methods"]))
    st.markdown(f"**Potential model system(s):** {info['model']}")
    if "established" in info:
        background_notice(info["established"].replace("**Established background:** ", ""))
    st.warning(info["hypothetical"])
    st.info(f"**Limitations of the models:** {info['limitations']}")
    st.markdown(f"**Think about it:** {info['think']}")
    st.text_area("Write your own thoughts (they are not saved or sent anywhere)", key=f"disease_notes_{theme}")

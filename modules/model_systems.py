"""Module C: Biological model systems (zebrafish has its own subsection in zebrafish.py).

All descriptions are simplified general background. Numbers such as generation times are
approximate and depend on conditions.
"""
from __future__ import annotations

MODEL_ORDER = ["Zebrafish", "Fruit fly", "Nematode worm", "Mouse", "Yeast", "Human cell cultures", "Organoids"]

MODELS = {
    "Zebrafish": {
        "what": "A small freshwater fish (Danio rerio). Embryos develop outside the mother and are transparent in early stages.",
        "questions": "Early vertebrate development, organ formation (e.g. heart, blood vessels, nervous system), gene function, regeneration, some disease mechanisms.",
        "advantages": "Live imaging of whole embryos; many embryos per mating; rapid development; many genetic tools including fluorescent labelling of cells.",
        "limitations": "Fish biology differs from mammals (e.g. different organ structures, extra gene copies from an ancient genome duplication); adults are less transparent; findings need checking in other systems.",
        "measure": "Size and shape of tissues, cell movements, gene activity patterns, heartbeat and blood flow, behaviour, survival.",
        "human_relevance": "A vertebrate, so many genes and pathways are shared with humans, but relevance must be tested for each question.",
        "ethics": "Vertebrate research is regulated (in the UK, fish are protected once they begin to feed independently, around five days after fertilisation). Researchers follow the 3Rs: replace, reduce, refine.",
    },
    "Fruit fly": {
        "what": "The insect Drosophila melanogaster, kept in small vials.",
        "questions": "How body plans are set up, how signalling pathways work in development, genetics of organs such as eyes and wings, some neurobiology.",
        "advantages": "Short life cycle (about 10 days at 25 °C); powerful genetic tools; low cost; large numbers can be studied.",
        "limitations": "An invertebrate with a very different body plan (e.g. no heart like ours, no adaptive immune system); some human-relevant processes are absent.",
        "measure": "Adult and larval body structures, gene-activity patterns, behaviour, lifespan.",
        "human_relevance": "Several key developmental signalling pathways were first worked out in flies and are shared with vertebrates; details differ.",
        "ethics": "Insects are generally not covered by the animal-research licensing used for vertebrates in the UK, but good husbandry and sensible numbers still matter.",
    },
    "Nematode worm": {
        "what": "Caenorhabditis elegans, a transparent roundworm about 1 mm long.",
        "questions": "Cell lineages, programmed cell death, ageing, nervous-system wiring, basic gene function.",
        "advantages": "Transparent body; about 3 days from egg to adult at 20 °C; the fate of each cell in development has been mapped; easy to grow in large numbers.",
        "limitations": "No vertebrate organs (e.g. heart, bones, adaptive immunity); very simple anatomy.",
        "measure": "Cell divisions and fates under the microscope, movement, lifespan, fluorescent markers.",
        "human_relevance": "Fundamental processes (such as programmed cell death) are conserved, though most human organ biology cannot be studied directly.",
        "ethics": "Not covered by vertebrate-licensing rules in the UK; ethical practice still includes minimising unnecessary use.",
    },
    "Mouse": {
        "what": "A mammal (Mus musculus) widely used in biomedical research.",
        "questions": "Mammalian development, physiology, immunity, metabolism, behaviour, genetic disease.",
        "advantages": "A mammal with organs and physiology similar to humans in many ways; well-developed genetic tools and resources.",
        "limitations": "Embryos develop inside the mother, so live observation is harder; slower and costlier than small models; mice are not small humans, and results often differ.",
        "measure": "Whole-body physiology, tissue structure, gene activity, behaviour, disease-related features.",
        "human_relevance": "Often high for mammalian physiology, but many treatments that worked in mice have not worked in people.",
        "ethics": "Strictly regulated; justification, welfare and the 3Rs (replace, reduce, refine) are central.",
    },
    "Yeast": {
        "what": "Single-celled fungi, most often Saccharomyces cerevisiae (baker's/budding yeast).",
        "questions": "The cell cycle, DNA repair, protein production and transport, basic gene regulation.",
        "advantages": "Doubles in about 90 minutes in rich medium; very easy genetics; inexpensive; huge numbers of cells.",
        "limitations": "Single-celled, so no tissues or organ development; lacks many animal-specific processes.",
        "measure": "Growth rate, cell-cycle stage, protein location, response to changes in genes or conditions.",
        "human_relevance": "Core cell machinery is shared by all eukaryotes, so basic findings can apply to human cells; multicellular behaviour cannot be studied.",
        "ethics": "Few ethical concerns about the organism itself; usual laboratory safety applies.",
    },
    "Human cell cultures": {
        "what": "Human cells grown in dishes in a laboratory, either from cell lines or taken from donors.",
        "questions": "How human cells divide, respond to signals or drugs, express genes and handle specific genetic variants.",
        "advantages": "Human cells directly; controlled conditions; easy to measure and repeat; no whole animal needed.",
        "limitations": "No whole-body context; conditions are artificial; some cell lines have accumulated genetic changes (many come from cancers), so they may not behave like normal cells.",
        "measure": "Cell number and shape, gene and protein activity, response to treatments.",
        "human_relevance": "Directly human, but a dish of cells cannot show how a whole body or organ behaves.",
        "ethics": "Consent, source of cells, donor privacy and data protection must be handled carefully.",
    },
    "Organoids": {
        "what": "Small 3D structures grown from stem cells that self-organise and resemble some features of an organ (e.g. gut or brain tissue).",
        "questions": "How tissues self-organise, early organ development, how a tissue responds to genetic changes or drugs.",
        "advantages": "Three-dimensional human tissue-like structures; can be made from specific people's cells; reduce the need for some animal experiments.",
        "limitations": "Usually lack blood vessels, immune cells and whole-body signals; often resemble immature tissue; vary between batches; they are not whole organs.",
        "measure": "Cell types present, tissue architecture, gene activity, response to treatments.",
        "human_relevance": "Human-derived, so can be informative about human tissue, but they capture only part of real organ complexity.",
        "ethics": "Stem-cell sources and consent matter; there are ongoing discussions about how to treat especially complex brain organoids.",
    },
}

COMPARISON = {
    "Zebrafish": {"Type": "Vertebrate (fish)", "Approx. generation time": "~3 months", "Embryo observation": "External, transparent early",
                  "Genetic tools": "Extensive", "Whole-organism physiology": "Yes (fish)", "Ethical oversight": "Regulated vertebrate research"},
    "Fruit fly": {"Type": "Invertebrate (insect)", "Approx. generation time": "~10 days", "Embryo observation": "External, can be imaged",
                  "Genetic tools": "Very extensive", "Whole-organism physiology": "Yes (insect)", "Ethical oversight": "Generally no animal-licensing rules (UK)"},
    "Nematode worm": {"Type": "Invertebrate (nematode)", "Approx. generation time": "~3 days", "Embryo observation": "Transparent, cell lineage mapped",
                      "Genetic tools": "Extensive", "Whole-organism physiology": "Yes (simple)", "Ethical oversight": "Generally no animal-licensing rules (UK)"},
    "Mouse": {"Type": "Vertebrate (mammal)", "Approx. generation time": "~2–3 months", "Embryo observation": "Inside mother; harder to observe live",
              "Genetic tools": "Extensive but slower", "Whole-organism physiology": "Yes (mammal)", "Ethical oversight": "Strictly regulated vertebrate research"},
    "Yeast": {"Type": "Single-celled fungus", "Approx. generation time": "~90 minutes (doubling)", "Embryo observation": "Not applicable",
              "Genetic tools": "Very extensive", "Whole-organism physiology": "No (single cell)", "Ethical oversight": "Minimal"},
    "Human cell cultures": {"Type": "Human cells in dishes", "Approx. generation time": "Often ~1 day per doubling (varies widely)", "Embryo observation": "Not applicable",
                            "Genetic tools": "Available, varies by cell type", "Whole-organism physiology": "No", "Ethical oversight": "Consent and donor-privacy rules"},
    "Organoids": {"Type": "3D human or animal stem-cell-derived tissue", "Approx. generation time": "Weeks to months to form", "Embryo observation": "Models some tissue development only",
                  "Genetic tools": "Available, still developing", "Whole-organism physiology": "No", "Ethical oversight": "Stem-cell consent; ongoing debate for brain organoids"},
}

# ---------------------------------------------------------------------------
# "Choose a model" activity
# ---------------------------------------------------------------------------
# fit: 0 = poor direct fit, 3 = strong fit for this question. Only the main candidates are listed.
CHOOSER_QUESTIONS = {
    "Observing vertebrate embryo development": {
        "Zebrafish": (3, "Embryos develop outside the mother and are transparent early, so development can be watched live in a vertebrate."),
        "Mouse": (2, "A mammal, but embryos develop inside the mother, which makes continuous live observation difficult."),
        "Organoids": (1, "Can model some early tissue organisation, but are not whole embryos."),
        "Fruit fly": (1, "Easy to image, but not a vertebrate."),
        "Nematode worm": (1, "Transparent and well mapped, but not a vertebrate."),
    },
    "Investigating a developmental gene": {
        "Zebrafish": (3, "Gene activity can be changed and effects on a vertebrate embryo observed directly."),
        "Fruit fly": (3, "Very powerful genetics; many developmental genes were first studied here, though the animal is an insect."),
        "Mouse": (2, "Shows gene function in a mammal, but takes longer and costs more."),
        "Nematode worm": (2, "Simple, well-mapped development makes some gene functions easy to follow."),
        "Human cell cultures": (1, "Can show what a gene does in a cell, but not in a developing organism."),
        "Organoids": (1, "Can show effects on a developing tissue, with limits."),
    },
    "Studying basic cell-cycle mechanisms": {
        "Yeast": (3, "Fast, simple and genetically flexible; the core cell-cycle machinery is shared by all eukaryotes."),
        "Human cell cultures": (2, "Directly human, allowing checks that mechanisms hold in human cells."),
        "Fruit fly": (1, "Useful for cell division in a developing animal."),
        "Zebrafish": (1, "Allows cell division to be watched in a developing vertebrate."),
        "Nematode worm": (1, "Early embryo divisions are easy to watch."),
    },
    "Investigating mammalian physiology": {
        "Mouse": (3, "A mammal whose organs and body systems work together, which no dish or simple animal can reproduce."),
        "Zebrafish": (1, "A vertebrate, but a fish, so differs from mammals in many organ systems."),
        "Organoids": (1, "Can model parts of an organ, not whole-body interactions."),
        "Human cell cultures": (1, "Cells alone cannot show how organs interact."),
    },
    "Examining human-cell behaviour in a laboratory": {
        "Human cell cultures": (3, "Directly uses human cells under controlled conditions."),
        "Organoids": (2, "Human cells in a 3D arrangement, closer to a tissue than a flat dish."),
        "Mouse": (0, "Does not use human cells (unless special humanised systems are used)."),
    },
    "Studying tissue organisation in an organoid": {
        "Organoids": (3, "The question is about the organoid itself."),
        "Human cell cultures": (1, "A simpler comparison to see what flat cultures miss."),
        "Mouse": (1, "Provides an in-body reference for how the real tissue is organised."),
        "Zebrafish": (1, "Provides a living-animal reference for tissue organisation."),
    },
}

# Extra points (0-2) used only to re-order options according to the user's priority.
PRIORITY_SCORES = {
    "Whole-organism context": {"Zebrafish": 2, "Fruit fly": 1, "Nematode worm": 1, "Mouse": 2, "Yeast": 0, "Human cell cultures": 0, "Organoids": 0},
    "Speed and low cost": {"Zebrafish": 1, "Fruit fly": 2, "Nematode worm": 2, "Mouse": 0, "Yeast": 2, "Human cell cultures": 1, "Organoids": 0},
    "Closeness to human biology": {"Zebrafish": 1, "Fruit fly": 0, "Nematode worm": 0, "Mouse": 2, "Yeast": 0, "Human cell cultures": 2, "Organoids": 2},
    "Live imaging": {"Zebrafish": 2, "Fruit fly": 1, "Nematode worm": 2, "Mouse": 0, "Yeast": 1, "Human cell cultures": 1, "Organoids": 1},
}


def rank_models(question: str, priority: str, top_n: int = 3) -> list[dict]:
    """Rank models for a question. Fit counts double; the priority breaks ties.

    This is a teaching aid: it returns *potentially suitable* options with reasons,
    not "the" correct answer.
    """
    if question not in CHOOSER_QUESTIONS:
        raise ValueError(f"Unknown question: {question!r}")
    if priority not in PRIORITY_SCORES:
        raise ValueError(f"Unknown priority: {priority!r}")
    ranked = []
    for model, (fit, reason) in CHOOSER_QUESTIONS[question].items():
        if fit == 0:  # listed only to show a poor fit; never recommended
            continue
        score = 2 * fit + PRIORITY_SCORES[priority][model]
        ranked.append({"model": model, "fit": fit, "score": score, "reason": reason})
    ranked.sort(key=lambda r: (-r["score"], -r["fit"], MODEL_ORDER.index(r["model"])))
    return ranked[:top_n]


def comparison_table(selected: list[str]):
    """DataFrame comparing the selected models (rows = features)."""
    import pandas as pd

    unknown = [m for m in selected if m not in COMPARISON]
    if unknown:
        raise ValueError(f"Unknown model(s): {', '.join(unknown)}")
    if not selected:
        raise ValueError("Select at least one model.")
    return pd.DataFrame({m: COMPARISON[m] for m in selected})


# ---------------------------------------------------------------------------
# Streamlit page
# ---------------------------------------------------------------------------
def render() -> None:
    import streamlit as st

    from modules import zebrafish
    from modules.ui_helpers import background_notice

    st.title("Biological model systems")
    st.write(
        "No single system answers every question. Researchers choose models by balancing the question, the available methods, "
        "ethical constraints and each system's limitations."
    )
    tab_over, tab_cmp, tab_choose, tab_zf = st.tabs(
        ["Model profiles", "Compare models", "Choose a model", "Zebrafish research"]
    )

    with tab_over:
        background_notice("Simplified summaries; numbers are approximate and vary with conditions.")
        name = st.selectbox("Choose a model system", MODEL_ORDER, key="models_profile")
        info = MODELS[name]
        st.subheader(name)
        st.markdown(f"**What it is:** {info['what']}")
        st.markdown(f"**Questions it can help address:** {info['questions']}")
        c1, c2 = st.columns(2)
        c1.success(f"**Advantages:** {info['advantages']}")
        c2.warning(f"**Limitations:** {info['limitations']}")
        st.markdown(f"**What can be measured or observed:** {info['measure']}")
        st.markdown(f"**Relevance to human biology:** {info['human_relevance']}")
        st.markdown(f"**Ethical considerations:** {info['ethics']}")

    with tab_cmp:
        chosen = st.multiselect("Select models to compare", MODEL_ORDER, default=["Zebrafish", "Mouse", "Yeast"], key="models_compare")
        if chosen:
            st.dataframe(comparison_table(chosen))
        else:
            st.info("Select at least one model to see the table.")
        st.caption("Values are approximate generalisations; real timings and rules depend on species strain, conditions and country.")

    with tab_choose:
        st.write("Pick a research question and what matters most to you. The tool suggests **potentially suitable** models and explains why.")
        question = st.selectbox("Research question", list(CHOOSER_QUESTIONS), key="models_question")
        priority = st.radio("What matters most?", list(PRIORITY_SCORES), horizontal=True, key="models_priority")
        for place, item in enumerate(rank_models(question, priority), start=1):
            label = {3: "Strong fit", 2: "Reasonable fit", 1: "Partial fit", 0: "Weak fit"}[item["fit"]]
            st.markdown(f"**{place}. {item['model']}** — {label}\n\n{item['reason']}")
        st.info(
            "There is no single correct model. A different priority, method or ethical constraint could reasonably lead to a different choice, "
            "and many research projects use several models together to check that findings agree."
        )

    with tab_zf:
        zebrafish.render()

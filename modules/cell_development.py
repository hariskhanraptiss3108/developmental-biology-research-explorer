"""Module A: Cell biology and development.

Content is stored in dictionaries/lists at the top so it is easy to read and edit.
"""
from __future__ import annotations

DEVELOPMENT_STAGES = [
    {
        "name": "1. Fertilised egg (zygote)",
        "happening": "A sperm and an egg combine, giving one cell that contains genetic material from both parents.",
        "processes": "Fertilisation, activation of the egg, start of the first cell cycle.",
        "genes": "In many animals the earliest development uses RNA and proteins already stored in the egg. The embryo's own genes are switched on a little later (the timing differs between species).",
        "observe": "Fusion of the genetic material, the first division.",
        "methods": "Microscopy, fluorescent labels, time-lapse imaging.",
        "uncertain": "Exact timing of the switch to the embryo's own gene activity varies by species, and early human development is hard to study for technical and ethical reasons.",
    },
    {
        "name": "2. Cleavage divisions",
        "happening": "The embryo divides rapidly into more and smaller cells.",
        "processes": "Mitosis and cytokinesis; in many animals there is little overall growth at this stage, so cells get smaller.",
        "genes": "Maternal factors dominate at first; the embryo's own genes begin to contribute.",
        "observe": "Cell number rising, cell size falling, the pattern of divisions.",
        "methods": "Live imaging (easy in transparent embryos), cell tracking software.",
        "uncertain": "Species differ a lot: zebrafish cells divide on top of a yolk, whereas mammal embryos divide slowly before implanting in the uterus.",
    },
    {
        "name": "3. Patterning and gastrulation",
        "happening": "Cells are told where they are in the embryo and move to form the main layers (ectoderm, mesoderm, endoderm) and body axes.",
        "processes": "Cell signalling (e.g. gradients of signalling molecules), cell movements, early fate decisions.",
        "genes": "Regulatory genes (transcription factors) are switched on in particular regions, setting up a pattern.",
        "observe": "Where genes are active, how groups of cells move.",
        "methods": "Gene-activity staining, fluorescent reporters, labelling cells to follow their descendants, live imaging.",
        "uncertain": "How cells interpret signals so precisely and reliably is still actively studied.",
    },
    {
        "name": "4. Cell differentiation",
        "happening": "Cells become specialised (e.g. neurons, muscle, blood), taking on distinct structures and roles.",
        "processes": "Changes in which genes are active, often driven by transcription factors and signals from neighbours.",
        "genes": "Different sets of genes are switched on or off; the DNA sequence itself is broadly the same in different cells.",
        "observe": "Cell shape, specialised proteins ('markers'), function.",
        "methods": "Antibody staining, single-cell RNA sequencing, reporter genes.",
        "uncertain": "Fate decisions can be partly random, and some cells can change identity under certain conditions.",
    },
    {
        "name": "5. Tissue organisation",
        "happening": "Cells stick together, migrate and arrange into sheets, tubes and layers.",
        "processes": "Cell adhesion, migration, signalling between neighbouring cells, shape changes.",
        "genes": "Genes for adhesion molecules and signalling components are important.",
        "observe": "Tissue shape and layering.",
        "methods": "Live imaging, 3D microscopy, computer models.",
        "uncertain": "Mechanical forces inside tissues are difficult to measure directly.",
    },
    {
        "name": "6. Organ formation",
        "happening": "Several tissues combine, fold and grow into organs such as the heart or brain.",
        "processes": "Growth, folding, branching and interactions between different tissues.",
        "genes": "Many genes work in networks; a change in one can alter several others.",
        "observe": "Organ shape and early function (e.g. a beating heart).",
        "methods": "Genetic changes in model organisms, imaging, organoid cultures.",
        "uncertain": "Coordinating processes from the molecular to the whole-organ level is complex; findings in one species need testing in others.",
    },
    {
        "name": "7. Growth, remodelling and cell death",
        "happening": "Organs keep growing and being reshaped; some cells are removed in a controlled way.",
        "processes": "Cell growth, division, and programmed cell death (apoptosis), which helps shape tissues — for example by removing cells between developing fingers and toes in many vertebrates.",
        "genes": "Genes that promote or restrain cell death and division are balanced.",
        "observe": "Changes in size and shape; molecular markers of programmed cell death.",
        "methods": "Staining for cell-death markers, time-lapse imaging.",
        "uncertain": "The balance between cell survival, division and death in different tissues is complex and context dependent.",
    },
]

CELL_TYPES = {
    "Neuron": {
        "role": "Sends and receives electrical and chemical signals.",
        "features": "Long extensions (axons and dendrites); synapses for communication.",
        "genes": "Genes for ion channels, neurotransmitter receptors and synaptic proteins are active. Transcription factors such as NEUROD1 help promote neuron formation.",
        "note": "Most neurons stop dividing once mature.",
    },
    "Muscle cell": {
        "role": "Contracts to produce movement or force.",
        "features": "Contractile fibres; skeletal muscle fibres have several nuclei.",
        "genes": "Genes for actin, myosin and related proteins are active. The transcription factor MYOD1 helps drive muscle identity.",
        "note": "Muscle also contains stem-like cells that can contribute to repair.",
    },
    "Epithelial cell": {
        "role": "Forms linings and barriers (e.g. skin, gut lining).",
        "features": "Cells tightly joined in sheets; the two sides of the sheet differ.",
        "genes": "Genes for cell-junction proteins (such as E-cadherin) and structural proteins (keratins) are active.",
        "note": "Many epithelia are constantly renewed from stem cells.",
    },
    "Red blood cell": {
        "role": "Carries oxygen around the body.",
        "features": "Packed with haemoglobin; the biconcave shape suits gas exchange.",
        "genes": "Haemoglobin genes are highly active in developing red blood cells; the transcription factor GATA1 is important.",
        "note": "Mature red blood cells in mammals have lost their nucleus, so they are an exception to 'every cell has the genome'. They arise from precursor cells that did contain it.",
    },
}

CELL_CYCLE_PHASES = {
    "G1": ("Gap 1", "The cell grows and carries out its normal work. Signals here influence whether the cell commits to dividing, pauses, or differentiates."),
    "S": ("Synthesis", "DNA is copied so each daughter cell can receive a full set."),
    "G2": ("Gap 2", "More growth; the cell checks that DNA copying is complete and prepares for division."),
    "M": ("Mitosis + cytokinesis", "Mitosis separates the copied chromosomes (prophase, metaphase, anaphase, telophase); cytokinesis then divides the cell into two."),
}
MITOSIS_STEPS = {
    "Prophase": "Chromosomes condense and become visible; the spindle begins to form.",
    "Metaphase": "Chromosomes line up across the middle of the cell.",
    "Anaphase": "Sister chromatids are pulled apart to opposite ends.",
    "Telophase": "New nuclear envelopes form around the two sets of chromosomes; cytokinesis follows.",
}


def cleavage_cell_counts(rounds: int) -> list[int]:
    """Idealised number of cells after 0..rounds synchronous divisions (1, 2, 4, ...)."""
    if rounds < 0:
        raise ValueError("rounds cannot be negative")
    return [2 ** n for n in range(rounds + 1)]


def render() -> None:
    import pandas as pd
    import streamlit as st
    from matplotlib.figure import Figure

    from modules.ui_helpers import background_notice

    st.title("Cell biology & development")
    background_notice(
        "Development is not a simple one-way chain. Many processes (division, signalling, movement, differentiation, cell death) "
        "overlap and influence each other, and different organisms do it differently."
    )
    tab_dev, tab_cycle, tab_diff, tab_more = st.tabs(
        ["Development explorer", "Cell cycle & division", "Differentiation explorer", "Stem cells, signalling & cell death"]
    )

    with tab_dev:
        names = [stage["name"] for stage in DEVELOPMENT_STAGES]
        chosen = st.select_slider("Move through development", options=names, key="cell_stage")
        stage = DEVELOPMENT_STAGES[names.index(chosen)]
        st.subheader(stage["name"])
        st.markdown(f"**What is happening:** {stage['happening']}")
        st.markdown(f"**Cell processes involved:** {stage['processes']}")
        st.markdown(f"**Gene expression:** {stage['genes']}")
        st.markdown(f"**What scientists can observe:** {stage['observe']}")
        st.markdown(f"**Research methods:** {stage['methods']}")
        st.warning(f"**What is uncertain or hard to measure:** {stage['uncertain']}")
        st.caption("Stages overlap in time and differ between species; this is a simplified teaching sequence, not a universal timetable.")
        with st.expander("Idealised cell-number chart for early divisions"):
            rounds = st.slider("Rounds of division", 1, 8, 5, key="cell_rounds")
            counts = cleavage_cell_counts(rounds)
            st.bar_chart(pd.Series(counts, index=[str(i) for i in range(rounds + 1)], name="Cells"))
            st.caption("Idealised: assumes every cell divides together. Real embryos are not perfectly synchronous, and some cells die.")

    with tab_cycle:
        phase = st.radio("Explore a phase of the cell cycle", list(CELL_CYCLE_PHASES), horizontal=True, key="cell_phase")
        fig = Figure(figsize=(3.6, 3.6))
        ax = fig.subplots()
        sizes = [45, 30, 20, 5]  # illustrative only
        explode = [0.08 if p == phase else 0 for p in CELL_CYCLE_PHASES]
        ax.pie(sizes, labels=list(CELL_CYCLE_PHASES), explode=explode, startangle=90, counterclock=False, wedgeprops={"width": 0.45})
        ax.set_title("Cell cycle (illustrative proportions)", fontsize=9)
        left, right = st.columns([1, 1])
        left.pyplot(fig)
        full, text = CELL_CYCLE_PHASES[phase]
        right.markdown(f"### {phase}: {full}\n{text}")
        st.caption("The wedge sizes are NOT real measurements: the length of each phase varies hugely between cell types and conditions.")
        if phase == "M":
            step = st.selectbox("Stages of mitosis", list(MITOSIS_STEPS), key="cell_mitosis")
            st.write(MITOSIS_STEPS[step])
        st.markdown("#### Three different things")
        st.dataframe(
            pd.DataFrame(
                {
                    "Process": ["Cell growth", "Cell division", "Cell differentiation"],
                    "What changes": ["The cell gets bigger / makes more material", "One cell becomes two (number of cells increases)", "A cell becomes specialised (type changes)"],
                    "Example": ["A cell increases in volume during G1", "Mitosis and cytokinesis", "A progenitor cell becomes a muscle cell"],
                    "Can happen without the others?": ["Yes — a cell can grow without dividing", "Yes — e.g. rapid early embryo divisions with little growth", "Yes — many differentiated cells no longer divide"],
                }
            ),
            hide_index=True,
        )

    with tab_diff:
        cell = st.selectbox("Choose a cell type", list(CELL_TYPES), key="cell_type")
        info = CELL_TYPES[cell]
        st.subheader(cell)
        st.markdown(f"**Role:** {info['role']}")
        st.markdown(f"**Notable features:** {info['features']}")
        st.markdown(f"**Gene-expression patterns that support the role:** {info['genes']}")
        st.markdown(f"**Extra note:** {info['note']}")
        st.info(
            "Most specialised cells in one individual contain broadly the same genome (the same DNA). What differs is "
            "**which genes are used** — the pattern of gene expression — plus the proteins and signals around them. "
            "(A few exceptions exist, such as mature mammalian red blood cells that lose their nucleus.)"
        )

    with tab_more:
        st.markdown("#### Stem cells")
        st.markdown(
            "A **stem cell** can renew itself and can give rise to more specialised cells. How many types it can produce varies:\n"
            "- **Pluripotent** stem cells (e.g. embryonic stem cells, or induced pluripotent stem cells made by reprogramming other cells) can form all the cell types of the body.\n"
            "- **Multipotent** (tissue) stem cells produce a more limited range, e.g. blood stem cells produce blood cell types.\n"
            "Stem-cell behaviour depends on context and signals; the word describes what a cell *can do*, not a single fixed kind of cell."
        )
        st.markdown("#### Cell signalling")
        st.markdown(
            "Cells communicate with signalling molecules and contact between neighbours. A signal binds a receptor and triggers changes "
            "inside the receiving cell, often altering gene expression. The same few signalling pathways (for example Wnt, Notch, Hedgehog, BMP and FGF) "
            "are reused many times in different tissues, so the *context* decides the outcome."
        )
        st.markdown("#### Programmed cell death")
        st.markdown(
            "Apoptosis is an orderly, controlled form of cell death. It is a normal part of development (it helps sculpt tissues) and of keeping tissues healthy. "
            "Too little or too much can contribute to disease, so it is tightly regulated."
        )

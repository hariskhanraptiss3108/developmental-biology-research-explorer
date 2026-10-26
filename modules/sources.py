"""Sources and limitations page."""
from __future__ import annotations

# NOTE FOR THE AUTHOR: these links were supplied by you. When this project was built there was no
# internet access, so the links were NOT opened or checked. Descriptions are deliberately general.
SOURCES = [
    {"name": "YourGenome — What are model organisms?",
     "url": "https://www.yourgenome.org/theme/what-are-model-organisms/",
     "use": "Educational background on why scientists use model organisms."},
    {"name": "Washington University — Developmental Biology: model systems",
     "url": "https://developmentalbiology.wustl.edu/research/model-systems/",
     "use": "University research page about model systems used in developmental biology."},
    {"name": "NIH developmental biology resources",
     "url": "https://developmentalbiology.nih.gov/",
     "use": "Public-sector resources on developmental biology."},
    {"name": "Open-access article on PubMed Central (PMC9335277)",
     "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9335277/",
     "use": "Peer-reviewed literature. Open it, then add its real title, authors and year to your own notes — they are not stated here because they were not checked."},
    {"name": "Max Planck Institute of Molecular Cell Biology and Genetics — Organoids and organisms",
     "url": "https://www.mpi-cbg.de/research/our-research/research-areas/organoids-and-organisms",
     "use": "Research-institute overview of organoid and organism research."},
]


def render() -> None:
    import streamlit as st

    st.title("Sources & limitations")
    st.subheader("Starting sources")
    st.warning(
        "These links were provided as starting points. They have **not** been checked by the author of this app, "
        "and no specific findings are attributed to them. Open each one, confirm it is relevant, and record proper citations yourself."
    )
    for src in SOURCES:
        st.markdown(f"- [{src['name']}]({src['url']}) — {src['use']}")

    st.subheader("What is what in this app")
    st.markdown(
        "- **Established background (simplified):** general biology explained in the author's own words, e.g. the genetic code, "
        "the cell cycle, why model organisms are used. Check it against textbooks and the sources above.\n"
        "- **Simulated / fictional data and case studies:** the expression values, virtual-lab datasets, the zebrafish case study, "
        "and the 'hypothetical results' in the disease module. They were invented for teaching.\n"
        "- **The app's own interpretations:** model suggestions, the simple statistics and the explanatory text are teaching aids, not expert judgement."
    )
    st.subheader("Limitations")
    st.markdown(
        "- Nothing here is real research data, medical advice or a diagnostic tool.\n"
        "- The DNA tools treat sequences as strings of letters; they do not identify genes or predict disease.\n"
        "- The statistics are simple permutation tests on tiny fictional datasets.\n"
        "- Numbers such as generation times and phase lengths are approximate and vary with conditions.\n"
        "- The app does not connect to any database, so it cannot search for real sequences."
    )

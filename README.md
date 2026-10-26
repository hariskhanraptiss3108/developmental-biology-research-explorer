# Developmental Biology & Disease Research Explorer

An interactive educational web app, built with Python and Streamlit, that lets students explore **how scientists investigate the relationship between genes, cells, development and disease**.

## Overview
Eight linked areas: cell biology & development, genetics & molecular biology, model systems (with a zebrafish subsection), disease & human biology, a virtual research lab, beginner bioinformatics, a quiz and a sources page. Zebrafish are an important part of the project but not the only topic.

## Why this project exists
It was created as a learning project by a Year 12 student interested in genetics, biotechnology, cell biology and developmental biology, to practise both biology and Python. *(Edit this paragraph to say it in your own words.)*

## Features
- **Home page** with an 8-step research workflow, module cards and example research questions that link to modules.
- **A. Cell biology & development** – 7-stage development explorer, cell-cycle explorer, differentiation explorer (neuron, muscle, epithelial, red blood cell), stem cells, signalling, cell death.
- **B. Genetics** – DNA analyser (length, counts, %, GC content, complement, reverse complement) with validation; transcription & translation using the full standard genetic code; mutation explorer that classifies substitutions/insertions/deletions only when the sequence supports it; simulated gene-expression explorer.
- **C. Model systems** – profiles of zebrafish, fruit flies, nematodes, mice, yeast, human cell cultures and organoids; comparison table; "choose a model" activity; zebrafish subsection with a fully simulated case study.
- **E. Disease & human biology** – neural development, heart development, regeneration, genetic disease (not medical advice).
- **F. Virtual lab** – three fictional scenarios (two-group, cell-growth, paired time points) with charts of individual observations and permutation tests.
- **G. Bioinformatics** – multi-sequence checker (FASTA-style input), sequence comparison, a simple ORF finder, and explanations of what real tools do. No database searches.
- **H. Knowledge check** – 20 reasoning questions, feedback only after submitting, score and retry.
- **Works offline** once dependencies are installed.

## Screenshots
*No screenshots are included yet.* After you run the app, take your own screenshots (on a Chromebook: `Ctrl + Show windows` key, or `Shift + Ctrl + Show windows`), save them in a `screenshots/` folder, and add them here with:
```markdown
![Home page](screenshots/home.png)
```

## Technologies
Python 3.10+, [Streamlit](https://streamlit.io), pandas, matplotlib. Tests use Python's built-in `unittest`.

## Project structure
```text
developmental-biology-research-explorer/
├── app.py                      # Main entry point: sidebar and page routing
├── requirements.txt
├── README.md  LICENSE  .gitignore
├── modules/
│   ├── navigation.py           # Page names
│   ├── ui_helpers.py           # Banners and a reusable check-your-answer question
│   ├── home.py                 # Home page
│   ├── cell_development.py     # Module A
│   ├── genetics.py             # Module B (logic + page)
│   ├── model_systems.py        # Module C (profiles, comparison, chooser)
│   ├── zebrafish.py            # Zebrafish subsection and simulated case study
│   ├── disease_research.py     # Module E
│   ├── virtual_lab.py          # Module F
│   ├── stats_utils.py          # Simple statistics (permutation tests)
│   ├── bioinformatics.py       # Module G
│   ├── quiz.py                 # Module H
│   └── sources.py              # Sources & limitations page
├── data/
│   ├── example_datasets.csv    # FICTIONAL data
│   └── make_example_datasets.py# Script that generated the CSV
├── tests/
│   ├── test_genetics.py
│   ├── test_bioinformatics.py
│   └── test_experiments.py     # stats, datasets, model chooser, quiz
└── docs/
    ├── scientific_background.md
    └── project_journal_template.md
```
(There is no Module D file: the zebrafish subsection is inside the Model systems page, as requested.)

## Setup

### Option 1 – no installation, no terminal (recommended on a Chromebook)
1. **Unzip** the project on your Chromebook (Files app → double-click the ZIP → drag the folder out to *My files*).
2. Create a free account at [github.com](https://github.com) and create a **new public repository** (e.g. `developmental-biology-research-explorer`).
3. In the repository click **Add file → Upload files** and drag in the *contents* of the project folder (the folders `modules`, `data`, `tests`, `docs` and the files `app.py`, `requirements.txt`, etc.). Click **Commit changes**.
4. Go to [share.streamlit.io](https://share.streamlit.io) (Streamlit Community Cloud), sign in with GitHub, choose **Create app**, pick your repository, branch `main`, main file `app.py`, and **Deploy**.
5. If something fails, open **Manage app** (bottom right of the running app) to read the logs. Copy the error message into your journal and fix the file on GitHub (click the file → pencil icon → *Commit changes*); the app reloads.

> I could not check the current rules or limits of GitHub or Streamlit Community Cloud when writing this, so please read their pages to confirm they are free for your use and available with your school or personal account.

### Option 2 – GitHub Codespaces (a coding environment in the browser)
After uploading to GitHub (steps 1–3 above): on your repository click **Code → Codespaces → Create codespace**. A browser-based editor with a terminal opens. Then run:
```bash
pip install -r requirements.txt
streamlit run app.py
```
A pop-up offers to open the app in your browser. Save your work with the **Source Control** panel (write a message → **Commit** → **Sync**). Check GitHub's current free monthly allowance for Codespaces, and stop the codespace when you finish.

### Option 3 – your own computer / Chromebook Linux environment
If Linux is enabled on your Chromebook (not always possible on school-managed devices):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Testing
```bash
python -m unittest discover -s tests -v
```
(`pytest` also works if installed.) The tests cover DNA validation, nucleotide counts, GC content, complement/reverse complement, translation with the genetic code, mutation classification, ORF finding, dataset loading, statistics, the model chooser, and quiz answer checking, including empty and invalid inputs.

**What has and has not been tested** — see "Testing status" below.

## Testing status (honest summary)
- **Done:** 83 automated unit tests pass; all Python files compile; every page's code was executed once against a stand-in for Streamlit to check there are no crashes in the page code.
- **Not done:** the app has **not** been launched in a real Streamlit server or viewed in a browser by the author of the code; the layout, charts and clicking behaviour are therefore untested visually. The external links were not opened. Behaviour on specific Streamlit versions was not tested. If you see an error, please note it in your journal and fix or report it.

## Scientific limitations
- All gene-expression values, virtual-lab datasets, the zebrafish case study and the "hypothetical results" in the disease module are **fictional**.
- Example DNA sequences are **fictional**, not real genes. The DNA tools treat sequences as text; they cannot identify genes, predict disease or establish function.
- The statistics are simple permutation tests on very small fictional datasets and say nothing about real biology.
- Biological summaries are simplified; numbers like generation times are approximate.
- Not medical advice and not a diagnostic tool.
- No database is searched.

## Sources
See the in-app *Sources & limitations* page and `docs/scientific_background.md`. The starting links supplied were **not verified**; open them and add proper citations yourself.

## AI assistance
This project's code, text and structure were drafted with the help of an AI assistant (Claude, by Anthropic) from a specification written by the project owner. The owner is responsible for reviewing, understanding and testing the work, and should describe their own contributions honestly in the project journal. *(Edit this section to reflect what you actually did.)*

## Suggested GitHub repository description and topics
**Description:** Interactive Streamlit app exploring how genes, cells, development and disease are studied: model organisms (incl. zebrafish), genetics tools, simulated data and experimental reasoning.

**Topics:** `streamlit`, `python`, `biology`, `developmental-biology`, `genetics`, `bioinformatics`, `zebrafish`, `education`, `model-organisms`, `data-visualization`

## Publishing to GitHub (summary)
1. Create a repository on github.com. 2. **Add file → Upload files** and upload the project contents. 3. Edit `LICENSE` to put your name and the year. 4. Add the description and topics in the repository's **About** (gear icon) panel. 5. Add your own screenshots once you have them.

## Licence
MIT – see `LICENSE` (replace `<YOUR NAME HERE>`).

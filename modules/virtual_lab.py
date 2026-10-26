"""Module F: Virtual research laboratory (all data are fictional)."""
from __future__ import annotations

from pathlib import Path

from modules.stats_utils import (
    cohens_d,
    mean,
    paired_sign_flip_test,
    permutation_test_independent,
    sample_sd,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "example_datasets.csv"
REQUIRED_COLUMNS = ["scenario", "group", "subject_id", "value"]


# ---------------------------------------------------------------------------
# Dataset handling
# ---------------------------------------------------------------------------
def load_datasets(path=DATA_PATH):
    """Read the CSV and check it has the expected columns and numeric values."""
    import pandas as pd

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing column(s): {', '.join(missing)}")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if df["value"].isna().any():
        raise ValueError("Dataset contains non-numeric values in the 'value' column.")
    return df


def get_scenario_data(df, scenario: str):
    """Rows of one scenario. Raises ValueError for an unknown name."""
    subset = df[df["scenario"] == scenario]
    if subset.empty:
        raise ValueError(f"Unknown scenario: {scenario!r}")
    return subset.reset_index(drop=True)


def group_values(subset, group: str) -> list[float]:
    return subset.loc[subset["group"] == group, "value"].tolist()


def paired_values(subset, first_group: str, second_group: str) -> tuple[list[float], list[float]]:
    """Values for the same subject ids at two time points, in matching order."""
    a = subset[subset["group"] == first_group].set_index("subject_id")["value"]
    b = subset[subset["group"] == second_group].set_index("subject_id")["value"]
    shared = [sid for sid in a.index if sid in b.index]
    if not shared:
        raise ValueError("No subjects appear in both groups, so the data cannot be paired.")
    return [a[s] for s in shared], [b[s] for s in shared]


def summarise(subset) -> list[dict]:
    """Mean, SD and n for each group."""
    rows = []
    for group in subset["group"].unique():
        vals = group_values(subset, group)
        rows.append({"Group": group, "n": len(vals), "Mean": round(mean(vals), 1),
                     "SD": round(sample_sd(vals), 1) if len(vals) > 1 else None,
                     "Min": min(vals), "Max": max(vals)})
    return rows


def analyse_scenario(subset, design: str, seed: int = 42) -> dict:
    """Run the appropriate permutation test and effect size for a scenario."""
    groups = list(subset["group"].unique())
    if len(groups) != 2:
        raise ValueError("Exactly two groups are needed for this comparison.")
    if design == "paired":
        before, after = paired_values(subset, groups[0], groups[1])
        result = paired_sign_flip_test(before, after, seed=seed)
        result["test"] = "Paired sign-flip permutation test"
    elif design == "independent":
        a, b = group_values(subset, groups[0]), group_values(subset, groups[1])
        result = permutation_test_independent(a, b, seed=seed)
        result["cohens_d"] = cohens_d(a, b)
        result["test"] = "Two-group permutation test (difference in means)"
    else:
        raise ValueError("design must be 'independent' or 'paired'")
    result["groups"] = groups
    return result


# ---------------------------------------------------------------------------
# Scenario descriptions
# ---------------------------------------------------------------------------
SCENARIOS = {
    "tissue_size": {
        "title": "1 · Tissue size in two groups of embryos",
        "design": "independent",
        "unit": "tissue size (arbitrary units)",
        "question": "Does reducing the activity of a developmental gene change the size of a tissue in fictional embryos?",
        "hypothesis": "Embryos with reduced gene activity will have a smaller tissue than control embryos.",
        "independent": "Gene activity (normal vs reduced)",
        "dependent": "Tissue size (arbitrary units)",
        "control": "Control embryos with normal gene activity",
        "quiz": {
            "prompt": "Which statement best fits the data and the analysis?",
            "options": [
                "The data prove the gene controls tissue size in all animals.",
                "The groups differ on average, and the analysis helps judge whether chance alone is a plausible explanation, but the dataset is small and fictional so it cannot establish a real biological conclusion.",
                "The groups overlap, so the data show there is no effect at all.",
                "Because the mean of one group is lower, no statistics are needed.",
            ],
            "correct": 1,
            "explanation": "Means can differ by chance, so we compare the difference with how much shuffling the labels could produce. Overlap does not prove 'no effect', "
                           "and a single small fictional dataset can never establish a fact about real biology.",
        },
    },
    "cell_growth": {
        "title": "2 · Cell growth under two culture conditions",
        "design": "independent",
        "unit": "relative cell density (arbitrary units)",
        "question": "Do cells reach a different density after 48 hours in culture condition B than in condition A?",
        "hypothesis": "Cells in condition B will reach a higher density than cells in condition A.",
        "independent": "Culture condition (A vs B)",
        "dependent": "Relative cell density after 48 hours",
        "control": "Condition A (standard condition used for comparison)",
        "quiz": {
            "prompt": "Each point is one culture well. Why does it matter that we can see every well, not only the mean?",
            "options": [
                "Individual points show the spread and overlap, which a mean alone hides.",
                "Individual points make the experiment more expensive.",
                "Means are always wrong.",
                "Individual points prove causation.",
            ],
            "correct": 0,
            "explanation": "A bar of means hides how variable the wells are. Seeing every point lets you judge overlap and spot odd values. "
                           "It does not by itself show causation; that needs good experimental design, such as a fair comparison and controls.",
        },
    },
    "paired_feature": {
        "title": "3 · A developmental feature at two time points",
        "design": "paired",
        "unit": "feature length (arbitrary units)",
        "question": "Does a developmental feature become longer between 24 h and 48 h in the same specimens?",
        "hypothesis": "The feature will be longer at 48 h than at 24 h.",
        "independent": "Time of observation (24 h vs 48 h)",
        "dependent": "Feature length (arbitrary units)",
        "control": "The 24 h measurement of each specimen acts as its own comparison (a paired design)",
        "quiz": {
            "prompt": "Why are lines drawn between the 24 h and 48 h points of each specimen?",
            "options": [
                "To show that each specimen was measured twice, so we can see the change within each specimen.",
                "Because the specimens are different animals at each time.",
                "Because lines are required in every graph.",
                "To prove growth is caused by the gene.",
            ],
            "correct": 0,
            "explanation": "The same specimens were measured twice, so the useful quantity is each specimen's change. This removes some of the variation between specimens. "
                           "It shows that length differs over time here, not why.",
        },
    },
}


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
def strip_chart(subset, unit: str):
    """Individual points (jittered sideways) plus a bar for each group's mean."""
    from matplotlib.figure import Figure
    import random

    rng = random.Random(0)
    fig = Figure(figsize=(5.5, 3.6))
    ax = fig.subplots()
    for x, group in enumerate(subset["group"].unique()):
        vals = group_values(subset, group)
        ax.scatter([x + rng.uniform(-0.12, 0.12) for _ in vals], vals, alpha=0.75, zorder=3)
        ax.hlines(mean(vals), x - 0.25, x + 0.25, color="black", linewidth=2, zorder=4)
    groups = list(subset["group"].unique())
    ax.set_xticks(range(len(groups)), groups)
    ax.set_ylabel(unit)
    ax.set_title("Each dot = one observation; black line = group mean (SIMULATED)")
    ax.title.set_fontsize(9)
    fig.tight_layout()
    return fig


def paired_chart(subset, unit: str):
    """One line per specimen connecting its two measurements."""
    from matplotlib.figure import Figure

    groups = list(subset["group"].unique())
    before, after = paired_values(subset, groups[0], groups[1])
    fig = Figure(figsize=(5.5, 3.6))
    ax = fig.subplots()
    for early, late in zip(before, after):
        ax.plot([0, 1], [early, late], marker="o", alpha=0.6)
    ax.set_xticks([0, 1], groups)
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylabel(unit)
    ax.set_title("Each line = one specimen measured twice (SIMULATED)")
    ax.title.set_fontsize(9)
    fig.tight_layout()
    return fig


def interpret_result(result: dict, design: str) -> str:
    """Plain-language, cautious summary of an analysis (never claims proof)."""
    p = result["p_value"]
    n = result.get("n_pairs") or ""
    direction = "higher" if result["observed_difference"] > 0 else "lower"
    if design == "paired":
        base = f"The average change was {result['observed_difference']:.1f} units across {n} specimens."
    else:
        base = (f"The mean of '{result['groups'][0]}' was {abs(result['observed_difference']):.1f} units "
                f"{direction} than '{result['groups'][1]}'." if result["observed_difference"] != 0 else "The group means were identical.")
    p_text = "p < 0.001" if p < 0.001 else f"p ≈ {p:.3f}"
    shuffle = "Randomly flipping the direction of each specimen's change" if design == "paired" else "Shuffling the group labels"
    if p < 0.05:
        strength = f"{shuffle} rarely gave a difference this large ({p_text}), so chance alone is a less comfortable explanation."
    else:
        strength = f"{shuffle} often gave differences this large ({p_text}), so these data do not rule out chance."
    return (base + " " + strength + " This is a tiny, fictional dataset: it illustrates reasoning but is not evidence about real biology.")


# ---------------------------------------------------------------------------
# Streamlit page
# ---------------------------------------------------------------------------
def render() -> None:
    import pandas as pd
    import streamlit as st

    from modules.ui_helpers import check_question, simulated_notice

    st.title("Virtual research laboratory")
    simulated_notice("Practise the *reasoning* scientists use, not real conclusions.")
    try:
        df = load_datasets()
    except (FileNotFoundError, ValueError) as exc:
        st.error(f"Could not load the datasets: {exc}")
        return

    key = st.selectbox("Choose a scenario", list(SCENARIOS), format_func=lambda k: SCENARIOS[k]["title"], key="lab_scenario")
    sc = SCENARIOS[key]
    subset = get_scenario_data(df, key)

    st.subheader(sc["title"])
    left, right = st.columns(2)
    left.markdown(f"**Research question:** {sc['question']}\n\n**Hypothesis:** {sc['hypothesis']}")
    right.markdown(
        f"**Independent variable:** {sc['independent']}\n\n**Dependent variable:** {sc['dependent']}\n\n"
        f"**Control / comparison:** {sc['control']}"
    )

    st.markdown("#### Dataset and chart")
    st.dataframe(pd.DataFrame(summarise(subset)), hide_index=True)
    st.pyplot(paired_chart(subset, sc["unit"]) if sc["design"] == "paired" else strip_chart(subset, sc["unit"]))
    with st.expander("Show every observation"):
        st.dataframe(subset, hide_index=True)

    st.markdown("#### Analysis")
    st.write(
        "Choose to run a statistical analysis. It uses a **permutation test** (no bell-curve assumption). "
        "It assumes independent observations and that group labels could be shuffled if there were no real difference."
    )
    if st.button("Run analysis", key=f"lab_run_{key}"):
        result = analyse_scenario(subset, sc["design"])
        st.write(f"**Test:** {result['test']}")
        cols = st.columns(3)
        cols[0].metric("Observed difference", f"{result['observed_difference']:.1f}")
        cols[1].metric("p-value (permutation)", f"{result['p_value']:.4f}")
        if "cohens_d" in result:
            cols[2].metric("Effect size (Cohen's d)", f"{result['cohens_d']:.2f}")
        st.info(interpret_result(result, sc["design"]))

    st.markdown("#### Interpretation activity")
    q = sc["quiz"]
    check_question(f"lab_{key}", q["prompt"], q["options"], q["correct"], q["explanation"])

    with st.expander("Ideas to keep separate when reading data"):
        st.markdown(
            "- **Observation vs interpretation:** 'Group B is higher' is an observation; 'B causes growth' is an interpretation.\n"
            "- **Correlation vs causation:** things that change together are not necessarily causing each other.\n"
            "- **Experimental results vs established facts:** one experiment is a piece of evidence; facts are supported by many independent studies.\n"
            "- **Hypothesis vs conclusion:** a hypothesis is a testable idea; a conclusion should follow from the evidence and mention limitations.\n"
            "- **Biological variation vs measurement error:** individuals genuinely differ; measurements also have imperfections."
        )

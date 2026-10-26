"""Zebrafish research subsection, including a fully SIMULATED case study.

The case study teaches experimental reasoning. It contains no instructions for genetic
modification or animal work, and its numbers are invented.
"""
from __future__ import annotations

# Approximate standard staging at about 28 °C (development is temperature dependent).
DEVELOPMENT_TIMELINE = [
    ("Within the first hours", "Rapid cell divisions begin on top of the yolk"),
    ("About 5–10 hours", "Gastrulation: cells move to form the main layers of the embryo"),
    ("About 10–24 hours", "Body segments (somites) form; early brain and eyes take shape"),
    ("About 1 day", "The heart begins to beat"),
    ("About 2–3 days", "Embryos hatch; many organs are recognisable"),
]

REASONS = [
    ("External development", "Fertilised eggs develop outside the mother, so embryos can be watched without disturbing a pregnancy."),
    ("Early transparency", "Early embryos are see-through, so cells and tissues can be seen with a microscope, especially with fluorescent labels."),
    ("Genetic tools", "Researchers can alter gene activity and label cell types with fluorescent proteins, then watch the consequences in a living embryo."),
    ("Many embryos, fast development", "A mating pair can produce many eggs, and major organs form within days, which helps with repeating experiments."),
    ("Tissue and organ development", "Heart, blood vessels, nervous system and other tissues can be followed as they form."),
    ("Selected disease mechanisms", "Some genes linked to human conditions have counterparts in zebrafish, so their roles can be investigated."),
    ("Regeneration", "Zebrafish can regrow parts such as fins and repair damaged heart tissue, making them useful for studying how regeneration works."),
]


def render() -> None:
    import pandas as pd
    import streamlit as st

    from modules.ui_helpers import background_notice, check_question, simulated_notice
    from modules.virtual_lab import analyse_scenario, get_scenario_data, load_datasets, strip_chart, summarise

    st.header("Zebrafish (Danio rerio) in research")
    tab_why, tab_case, tab_limits = st.tabs(["Why use zebrafish?", "Case study (simulated)", "What this model can and cannot tell us"])

    with tab_why:
        background_notice("General reasons zebrafish are used; check the Sources page for primary information.")
        for title, text in REASONS:
            st.markdown(f"**{title}.** {text}")
        st.markdown("**Rough timeline of early development**")
        st.dataframe(pd.DataFrame(DEVELOPMENT_TIMELINE, columns=["Approximate time after fertilisation", "What is happening"]), hide_index=True)
        st.caption("Timings are approximate and depend on temperature.")
        st.warning(
            "Zebrafish are **not** identical to humans, and a result in zebrafish does not automatically become a human treatment. "
            "Zebrafish findings are best seen as evidence that suggests ideas to test in other systems."
        )

    with tab_case:
        simulated_notice("This is a made-up example of how such an experiment could be reasoned about; it was not performed in a laboratory.")
        st.markdown("**Fictional research question:** How might changing the activity of a developmental gene affect the formation of a tissue?")

        st.markdown("#### Steps 1–4: Planning")
        st.markdown(
            "1. **Research question:** Does reducing the activity of a (fictional) developmental gene change the size of a developing tissue?\n"
            "2. **Testable hypothesis:** Embryos with reduced activity of this gene will have a smaller tissue than control embryos at the same stage.\n"
            "3. **Groups:** a *control group* (normal gene activity) and an *experimental group* (reduced gene activity). Both groups are raised in the same conditions.\n"
            "4. **Observable outcome:** the size of the tissue, measured from microscope images in arbitrary units."
        )

        st.markdown("#### Steps 5–6: Fictional measurements and comparison")
        try:
            subset = get_scenario_data(load_datasets(), "zebrafish_case")
        except (FileNotFoundError, ValueError) as exc:
            st.error(f"Could not load the case-study data: {exc}")
            return
        if st.button("Show the fictional measurements", key="zf_show"):
            st.session_state["zf_revealed"] = True
        if st.session_state.get("zf_revealed"):
            st.dataframe(pd.DataFrame(summarise(subset)), hide_index=True)
            st.pyplot(strip_chart(subset, "tissue size (arbitrary units)"))
            if st.button("Run a statistical analysis", key="zf_stats"):
                result = analyse_scenario(subset, "independent")
                st.write(
                    f"Observed difference in means: **{result['observed_difference']:.1f}** units; permutation-test p ≈ "
                    f"**{'<0.001' if result['p_value'] < 0.001 else format(result['p_value'], '.3f')}**; effect size d = {result['cohens_d']:.2f}."
                )
                st.caption(
                    "A permutation test asks how often shuffling the group labels gives a difference this big. It assumes independent embryos "
                    "and fair allocation. It cannot tell us whether the difference is biologically important, and it cannot rescue a poor design."
                )
        else:
            st.info("Press the button to reveal the fictional data.")

        st.markdown("#### Step 7: Interpret the evidence")
        check_question("zf_q1", "What is the control group for?",
                       ["To provide a baseline so the effect of changing the gene's activity can be judged.",
                        "To make sure every embryo is the same size.",
                        "To prove the hypothesis is true.", "To increase the number of embryos."], 0,
                       "Without a comparison group raised under the same conditions we could not tell whether any difference came from the gene change or from something else.")
        check_question("zf_q2", "Which variable is being changed by the researchers?",
                       ["Tissue size", "The activity of the gene", "The time of day", "The microscope used"], 1,
                       "The independent variable is the one the researcher changes: gene activity. Tissue size is the outcome that is measured.")
        check_question("zf_q3", "What outcome is being measured?",
                       ["The gene's activity", "The number of embryos", "The size of the tissue", "The hypothesis"], 2,
                       "The dependent variable (outcome) is tissue size.")
        check_question("zf_q4", "Does the data support the hypothesis?",
                       ["Yes, this proves the gene controls the tissue in all animals.",
                        "The fictional data are consistent with the hypothesis, but one small simulated experiment cannot prove it.",
                        "No, because the groups overlap at all.", "It cannot be judged without a graph."], 1,
                       "Evidence can support or fail to support a hypothesis; it rarely 'proves' anything. Here the pattern is consistent with the hypothesis, and the data are invented.")
        check_question("zf_q5", "Which additional evidence would most strengthen the conclusion?",
                       ["Repeating with new, independent groups, using a second independent way to reduce the gene's activity, and checking the gene's activity was actually reduced.",
                        "Measuring the same embryos many more times.", "Removing the embryos that do not fit the pattern.",
                        "Repeating the same single batch and calling it independent."], 0,
                       "Independent repeats, a different method that should give the same result, and a check that the intended change really happened all reduce the chance of being misled by chance or by side-effects.")
        check_question("zf_q6", "Why might the result differ in another species?",
                       ["Other species could have different gene copies, other genes that compensate, or different tissue structure.",
                        "All species always behave identically.", "Because experiments never repeat.", "Only because of measurement error."], 0,
                       "Species differ in anatomy, in how many copies of a gene they have, and in how backup pathways work, so each finding must be tested rather than assumed.")

        st.markdown("#### Step 8: Alternative interpretations and limitations")
        st.markdown(
            "- The difference could be due to chance, especially with small groups.\n"
            "- The gene change might have **side-effects** other than the intended one.\n"
            "- Embryos may differ for reasons unrelated to the treatment (e.g. different parents or tanks) — one reason for random allocation.\n"
            "- A smaller tissue could reflect delayed overall development rather than a specific role for the gene.\n"
            "- Measurement methods (image quality, who measures) can add error — measuring 'blind' to group helps."
        )

    with tab_limits:
        st.subheader("What this model can and cannot tell us")
        c1, c2 = st.columns(2)
        c1.success(
            "**Can help with**\n\n- Watching how tissues form in a living vertebrate\n- Testing whether a gene is *needed* for a developmental process\n"
            "- Generating hypotheses about disease mechanisms\n- Screening many embryos quickly"
        )
        c2.error(
            "**Cannot show by itself**\n\n- That a human will respond the same way\n- Whether a treatment is safe or effective in people\n"
            "- How mammal-specific organs (e.g. the placenta) work\n- A person's medical outcome"
        )

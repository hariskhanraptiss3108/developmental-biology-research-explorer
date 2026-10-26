"""Small reusable pieces of interface.

Streamlit is imported *inside* each function so that the scientific logic in the
other modules can be tested on a computer that does not have Streamlit installed.
"""


def simulated_notice(extra: str = "") -> None:
    """Banner that clearly marks data as invented for teaching."""
    import streamlit as st

    st.warning(
        "**SIMULATED / FICTIONAL DATA.** These numbers were generated for teaching. "
        "They are not results from a real laboratory. " + extra
    )


def background_notice(extra: str = "") -> None:
    """Banner marking text as general scientific background (not new findings)."""
    import streamlit as st

    st.info("**Established background (simplified).** " + extra)


def check_question(key: str, prompt: str, options: list, correct_index: int, explanation: str) -> None:
    """Multiple-choice question whose answer is only revealed after pressing the button."""
    import streamlit as st

    choice = st.radio(prompt, options, index=None, key=f"{key}_radio")
    if st.button("Check my answer", key=f"{key}_button"):
        if choice is None:
            st.warning("Choose an answer first.")
        elif options.index(choice) == correct_index:
            st.success("Good reasoning. " + explanation)
        else:
            st.error("Not quite. " + explanation)

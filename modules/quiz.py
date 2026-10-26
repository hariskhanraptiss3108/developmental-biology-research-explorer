"""Module H: Knowledge check. Questions are plain data; scoring is a plain function."""
from __future__ import annotations

QUESTIONS = [
    {"topic": "Cell differentiation",
     "question": "A neuron and a muscle cell from the same person look and behave very differently. What is the best explanation?",
     "options": ["They contain completely different DNA.", "They use different subsets of the same genome, so different genes are active.",
                 "Muscle cells have more genes than neurons.", "Neurons have no genes."],
     "answer": 1, "explanation": "Specialised cells in one individual have broadly the same genome; differentiation involves different patterns of gene expression."},
    {"topic": "Cell differentiation",
     "question": "A cell increases in volume but does not divide or change type. Which term describes this?",
     "options": ["Cell division", "Cell differentiation", "Cell growth", "Apoptosis"],
     "answer": 2, "explanation": "Growth means increase in size or content. Division changes cell number; differentiation changes cell type."},
    {"topic": "DNA and gene expression",
     "question": "A coding-strand DNA sequence reads 5'-ATGGCT-3'. What is the matching mRNA sequence?",
     "options": ["5'-UACCGA-3'", "5'-AUGGCU-3'", "5'-TACCGA-3'", "5'-AUGGCT-3'"],
     "answer": 1, "explanation": "mRNA matches the coding strand but contains U instead of T."},
    {"topic": "Genetic variation",
     "question": "A single base substitution changes the codon GAA to GAG, and both code for glutamic acid. What kind of change is this?",
     "options": ["Missense", "Nonsense (premature stop)", "Synonymous (silent)", "Frameshift"],
     "answer": 2, "explanation": "The codon changes but the amino acid does not, so the protein sequence is unchanged."},
    {"topic": "Genetic variation",
     "question": "One base is deleted inside a protein-coding region. What is the most likely consequence?",
     "options": ["Only one amino acid changes.", "A frameshift that can alter many downstream amino acids.", "Nothing, because the genetic code is flexible.", "The cell stops using DNA."],
     "answer": 1, "explanation": "Removing one base shifts the reading frame of every following codon."},
    {"topic": "Zebrafish as a model organism",
     "question": "Which feature makes zebrafish especially useful for watching early heart formation?",
     "options": ["Embryos are transparent and develop outside the mother.", "Zebrafish hearts are identical to human hearts.", "They develop only inside a uterus.", "They cannot be genetically studied."],
     "answer": 0, "explanation": "Transparency and external development allow live imaging. The fish heart is not identical to a human heart."},
    {"topic": "Zebrafish as a model organism",
     "question": "A gene change disrupts fin formation in zebrafish. Which conclusion is NOT justified by this alone?",
     "options": ["The gene may be needed for normal fin development in zebrafish.", "The same change will definitely cause the same effect in humans.",
                 "More experiments could test the idea.", "The result generates a hypothesis for other species."],
     "answer": 1, "explanation": "Zebrafish findings suggest hypotheses; they do not guarantee identical effects in humans."},
    {"topic": "Differences between model systems",
     "question": "Which system is usually best for studying basic cell-cycle machinery quickly and cheaply?",
     "options": ["Mouse", "Yeast", "Zebrafish adults", "Whole human bodies"],
     "answer": 1, "explanation": "Yeast divides quickly and is genetically simple, and the core cell-cycle machinery is shared by eukaryotes."},
    {"topic": "Differences between model systems",
     "question": "What is a common limitation of organoids?",
     "options": ["They contain no human cells.", "They usually lack the blood supply and whole-body interactions of a real organ.", "They cannot be studied by microscopy.", "They are identical to full organs."],
     "answer": 1, "explanation": "Organoids model some features of tissues but are simplified and often immature."},
    {"topic": "Experimental controls",
     "question": "What is the main purpose of a control group?",
     "options": ["To make the experiment bigger.", "To give a baseline so the effect of the changed variable can be judged.", "To guarantee the hypothesis is correct.", "To hide variation."],
     "answer": 1, "explanation": "Comparing with a group treated identically except for the variable of interest helps separate its effect from other influences."},
    {"topic": "Interpreting graphs",
     "question": "Two groups of 4 have different means, but their individual points overlap heavily. What is the most reasonable response?",
     "options": ["Declare a proven effect.", "Treat the evidence as weak and consider more data and an appropriate analysis.", "Delete the overlapping points.", "Conclude there is exactly no effect."],
     "answer": 1, "explanation": "Small groups and overlap mean chance could easily explain the difference; neither 'proof' nor 'no effect' is justified."},
    {"topic": "Interpreting graphs",
     "question": "Why is it useful to plot every individual observation rather than only the mean?",
     "options": ["It shows spread and overlap that a mean hides.", "It always proves causation.", "Means are never useful.", "It makes graphs simpler."],
     "answer": 0, "explanation": "Showing individual data points reveals variability, outliers and sample size."},
    {"topic": "Experimental controls",
     "question": "Measuring the same embryo three times gives slightly different lengths because the image is blurry. This is mainly...",
     "options": ["Biological variation between individuals", "Measurement error", "A genetic mutation", "Differentiation"],
     "answer": 1, "explanation": "Repeat measurements of the same specimen differ because of the measuring process; differences between individuals are biological variation."},
    {"topic": "Scientific limitations",
     "question": "Cells in fast-growing tissue also show high activity of gene X. What can you conclude?",
     "options": ["Gene X causes the growth.", "Gene X activity and growth are associated; causation needs further evidence.", "Gene X has no role.", "Fast-growing tissue lacks other genes."],
     "answer": 1, "explanation": "Correlation does not show causation. Experiments that change gene X activity would help test it."},
    {"topic": "Disease research",
     "question": "A genetic variant is found in a person with a condition. What does this alone show?",
     "options": ["The variant definitely causes the condition.", "It may be relevant, but more evidence (e.g. other families, population data, functional tests) is needed.", "Everyone with the variant will have the condition.", "The condition is not genetic."],
     "answer": 1, "explanation": "Association is not proof of cause. Variants are judged using several kinds of evidence, and effects can vary between people."},
    {"topic": "Disease research",
     "question": "Zebrafish can regenerate heart tissue. What is the most appropriate conclusion?",
     "options": ["Humans can regenerate hearts equally well.", "It offers clues about regeneration mechanisms, but human regeneration is much more limited, so findings need testing.",
                 "Zebrafish hearts are useless for research.", "A treatment for humans is guaranteed."],
     "answer": 1, "explanation": "Findings can suggest hypotheses and mechanisms, but they do not automatically translate to human treatments."},
    {"topic": "Scientific limitations",
     "question": "A virtual-lab dataset in this app shows a clear difference between two groups. What is its status?",
     "options": ["Evidence from a real experiment.", "Fictional teaching data that illustrates reasoning but says nothing about real biology.", "Proof of the hypothesis.", "A published result."],
     "answer": 1, "explanation": "The data were invented for teaching; they are not evidence about the real world."},
    {"topic": "Cell differentiation",
     "question": "Which statement about stem cells is most accurate?",
     "options": ["All stem cells can form every cell type.", "Stem cells can self-renew and give rise to more specialised cells, but the range of cell types depends on the kind of stem cell.",
                 "Stem cells never divide.", "Stem cells are the same as differentiated cells."],
     "answer": 1, "explanation": "Pluripotent stem cells can form all body cell types, whereas multipotent tissue stem cells produce a more limited range."},
    {"topic": "DNA and gene expression",
     "question": "Gene G is highly expressed in neurons but at low levels in blood cells. What is the best interpretation?",
     "options": ["Blood cells lack gene G in their genome.", "Gene G is used more in neurons than in blood cells, though the DNA sequence is broadly the same.", "Gene G is a mutation.", "Neurons have extra chromosomes."],
     "answer": 1, "explanation": "Gene expression differs between cell types, even though the genome is broadly the same."},
    {"topic": "Developmental biology",
     "question": "Which statement about development is best?",
     "options": ["Development is a single straight line with no overlap.", "Many processes (division, signalling, movement, differentiation, cell death) interact and overlap, and details differ between species.",
                 "All organisms develop identically.", "Gene expression plays no role."],
     "answer": 1, "explanation": "Development involves many interacting processes, and species differ in details."},
]


def _spread_answers(questions: list[dict]) -> None:
    """Rotate each question's options so the correct answer is not always in the same position.

    The rotation is deterministic (no randomness), so the quiz is the same every run and is easy to test.
    """
    for number, q in enumerate(questions):
        count = len(q["options"])
        target = (number * 3 + 1) % count
        shift = (target - q["answer"]) % count
        rotated = [None] * count
        for position, option in enumerate(q["options"]):
            rotated[(position + shift) % count] = option
        q["options"] = rotated
        q["answer"] = (q["answer"] + shift) % count


_spread_answers(QUESTIONS)


def check_answer(question: dict, selected_index) -> bool:
    """True only if ``selected_index`` is the correct option. None/invalid -> False."""
    if selected_index is None:
        return False
    return selected_index == question["answer"]


def score_quiz(questions: list[dict], selected_indices: list) -> tuple[int, int]:
    """Return (score, total). ``selected_indices`` holds one choice (or None) per question."""
    if len(selected_indices) != len(questions):
        raise ValueError("Provide exactly one answer (or None) for each question.")
    score = sum(check_answer(q, s) for q, s in zip(questions, selected_indices))
    return score, len(questions)


def validate_questions(questions: list[dict]) -> list[str]:
    """Return a list of problems found in the question data (empty list = fine)."""
    problems = []
    for number, q in enumerate(questions, 1):
        for field in ("topic", "question", "options", "answer", "explanation"):
            if field not in q:
                problems.append(f"Q{number}: missing '{field}'")
        if "options" in q and ("answer" in q):
            if len(q["options"]) < 2:
                problems.append(f"Q{number}: needs at least 2 options")
            if len(set(q["options"])) != len(q["options"]):
                problems.append(f"Q{number}: duplicate options")
            if not isinstance(q["answer"], int) or not 0 <= q["answer"] < len(q["options"]):
                problems.append(f"Q{number}: answer index out of range")
    return problems


def render() -> None:
    import streamlit as st

    st.title("Knowledge check")
    st.write(f"{len(QUESTIONS)} questions. Answers and explanations appear only after you submit.")
    run = st.session_state.setdefault("quiz_run", 0)
    submitted_key = f"quiz_submitted_{run}"

    with st.form(f"quiz_form_{run}"):
        choices = []
        for i, q in enumerate(QUESTIONS):
            choice = st.radio(f"**{i + 1}.** {q['question']}", q["options"], index=None, key=f"quiz_{run}_{i}")
            choices.append(None if choice is None else q["options"].index(choice))
        if st.form_submit_button("Submit answers"):
            st.session_state[submitted_key] = choices

    if submitted_key in st.session_state:
        answers = st.session_state[submitted_key]
        score, total = score_quiz(QUESTIONS, answers)
        st.header(f"Score: {score} / {total}")
        unanswered = sum(a is None for a in answers)
        if unanswered:
            st.caption(f"{unanswered} question(s) were left unanswered and count as incorrect.")
        for i, (q, a) in enumerate(zip(QUESTIONS, answers), 1):
            if check_answer(q, a):
                st.success(f"**{i}. Correct.** {q['explanation']}")
            else:
                given = "no answer" if a is None else q["options"][a]
                st.error(f"**{i}. Not quite** (your answer: {given}). Correct answer: {q['options'][q['answer']]}. {q['explanation']}")
        if st.button("Try again"):
            st.session_state["quiz_run"] = run + 1
            st.rerun()

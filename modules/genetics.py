"""Module B: Genetics and molecular biology.

The top half of this file is plain Python "logic" (easy to test).
The bottom half, ``render()``, draws the Streamlit page.

Conventions used throughout (stated on the page too):
* A DNA sequence typed by the user is the CODING strand, written 5' -> 3'.
* The coding strand has the same sequence as the mRNA (with T in place of U).
* The TEMPLATE strand is the complement of the coding strand and is read by
  RNA polymerase in its own 3' -> 5' direction.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

VALID_BASES = "ATCG"
_COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

# ---------------------------------------------------------------------------
# The standard genetic code
# ---------------------------------------------------------------------------
# The 64 codons are listed in the conventional T, C, A, G order for each of the
# three positions. "*" marks a stop codon.
_ORDER = "TCAG"
_AMINO_ACIDS_IN_ORDER = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"

CODON_TABLE: dict[str, str] = {}
_i = 0
for _first in _ORDER:
    for _second in _ORDER:
        for _third in _ORDER:
            CODON_TABLE[_first + _second + _third] = _AMINO_ACIDS_IN_ORDER[_i]
            _i += 1

AMINO_ACID_NAMES = {
    "A": ("Ala", "Alanine"), "R": ("Arg", "Arginine"), "N": ("Asn", "Asparagine"),
    "D": ("Asp", "Aspartic acid"), "C": ("Cys", "Cysteine"), "E": ("Glu", "Glutamic acid"),
    "Q": ("Gln", "Glutamine"), "G": ("Gly", "Glycine"), "H": ("His", "Histidine"),
    "I": ("Ile", "Isoleucine"), "L": ("Leu", "Leucine"), "K": ("Lys", "Lysine"),
    "M": ("Met", "Methionine"), "F": ("Phe", "Phenylalanine"), "P": ("Pro", "Proline"),
    "S": ("Ser", "Serine"), "T": ("Thr", "Threonine"), "W": ("Trp", "Tryptophan"),
    "Y": ("Tyr", "Tyrosine"), "V": ("Val", "Valine"), "*": ("Stop", "Stop codon"),
}

# Fictional teaching sequences. They are NOT real genes.
EXAMPLE_SEQUENCES = {
    "Fictional sequence 1 (9 codons + stop)": "ATGGCTAAAGAATTCGGTCTGACCTGGTAA",
    "Fictional sequence 2 (11 codons + stop)": "ATGAGCGATCCGCTGAAAGTTCAGCATTGCGGCTAA",
    "Fictional sequence 3 (10 codons + stop)": "ATGACCGAAGGTCGTATTAACCTGTGGAAATAA",
}


# ---------------------------------------------------------------------------
# Validation and basic sequence statistics
# ---------------------------------------------------------------------------
def clean_sequence(raw: str | None) -> str:
    """Remove spaces/new lines and convert to upper case."""
    return "".join((raw or "").split()).upper()


def validate_dna(raw: str | None) -> tuple[bool, str, str]:
    """Check a user-entered DNA string.

    Returns (is_valid, cleaned_sequence, message). ``message`` explains any problem.
    """
    cleaned = clean_sequence(raw)
    if not cleaned:
        return False, "", "The sequence is empty. Type or paste a sequence using only A, T, C and G."
    bad = sorted(set(cleaned) - set(VALID_BASES))
    if bad:
        shown = ", ".join(repr(b) for b in bad)
        hint = " (Note: U belongs in RNA, not DNA.)" if "U" in bad else ""
        return False, cleaned, f"Invalid character(s) found: {shown}. Only A, T, C and G are allowed.{hint}"
    return True, cleaned, ""


def _require_valid(sequence: str) -> str:
    """Return the cleaned sequence or raise ValueError with a clear message."""
    ok, cleaned, message = validate_dna(sequence)
    if not ok:
        raise ValueError(message)
    return cleaned


def count_nucleotides(sequence: str) -> dict[str, int]:
    seq = _require_valid(sequence)
    return {base: seq.count(base) for base in VALID_BASES}


def nucleotide_percentages(sequence: str) -> dict[str, float]:
    seq = _require_valid(sequence)
    return {base: 100 * seq.count(base) / len(seq) for base in VALID_BASES}


def gc_content(sequence: str) -> float:
    """Percentage of bases that are G or C."""
    seq = _require_valid(sequence)
    return 100 * (seq.count("G") + seq.count("C")) / len(seq)


def complement(sequence: str) -> str:
    """Base-by-base complement, in the SAME left-to-right order as the input."""
    seq = _require_valid(sequence)
    return "".join(_COMPLEMENT[b] for b in seq)


def reverse_complement(sequence: str) -> str:
    """Complement, then reversed, so it reads 5' -> 3' on the opposite strand."""
    return complement(sequence)[::-1]


# ---------------------------------------------------------------------------
# Transcription and translation
# ---------------------------------------------------------------------------
def transcribe_coding_strand(coding_dna: str) -> str:
    """mRNA has the coding-strand sequence with U instead of T (5' -> 3')."""
    return _require_valid(coding_dna).replace("T", "U")


def template_strand(coding_dna: str) -> str:
    """Template strand written 3' -> 5', aligned under the coding strand."""
    return complement(coding_dna)


def split_codons(sequence: str, start: int = 0) -> list[str]:
    """Full codons from ``start`` (0-based). Incomplete trailing bases are dropped."""
    seq = _require_valid(sequence)
    return [seq[i:i + 3] for i in range(start, len(seq) - 2, 3)]


def find_start_codon(sequence: str) -> int:
    """0-based index of the first ATG, or -1 if there is none."""
    return _require_valid(sequence).find("ATG")


def translate_coding(sequence: str, start: int = 0, to_stop: bool = True) -> tuple[str, bool, int]:
    """Translate a coding-strand sequence using the standard genetic code.

    Returns (protein, stop_found, leftover_bases).
    * protein: one-letter amino-acid string (the stop symbol is not included when
      ``to_stop`` is True; when False, stops appear as '*').
    * stop_found: whether a stop codon was reached.
    * leftover_bases: bases not read - those after the stop codon, or an incomplete final codon.
    """
    seq = _require_valid(sequence)
    protein = []
    stop_found = False
    position = start
    while position + 3 <= len(seq):
        amino_acid = CODON_TABLE[seq[position:position + 3]]
        position += 3
        if amino_acid == "*":
            stop_found = True
            if to_stop:
                break
        protein.append(amino_acid)
    leftover = len(seq) - position  # bases not read (after a stop codon, or an incomplete last codon)
    return "".join(protein), stop_found, leftover


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------
def apply_substitution(sequence: str, position: int, new_base: str) -> str:
    """Replace the base at ``position`` (1-based) with ``new_base``."""
    seq = _require_valid(sequence)
    new_base = clean_sequence(new_base)
    if new_base not in set(VALID_BASES) or len(new_base) != 1:
        raise ValueError("The new base must be a single A, T, C or G.")
    if not 1 <= position <= len(seq):
        raise ValueError(f"Position must be between 1 and {len(seq)}.")
    return seq[:position - 1] + new_base + seq[position:]


def apply_insertion(sequence: str, after_position: int, bases: str) -> str:
    """Insert ``bases`` after ``after_position`` (1-based; must be >= 1 so the start codon stays first)."""
    seq = _require_valid(sequence)
    ok, inserted, message = validate_dna(bases)
    if not ok:
        raise ValueError("Inserted bases: " + message)
    if not 1 <= after_position <= len(seq):
        raise ValueError(f"Insert after a position between 1 and {len(seq)}.")
    return seq[:after_position] + inserted + seq[after_position:]


def apply_deletion(sequence: str, position: int, length: int = 1) -> str:
    """Delete ``length`` bases starting at ``position`` (1-based)."""
    seq = _require_valid(sequence)
    if length < 1:
        raise ValueError("Deletion length must be at least 1.")
    if not 1 <= position <= len(seq) - length + 1:
        raise ValueError(f"With a deletion of {length}, start position must be between 1 and {len(seq) - length + 1}.")
    return seq[:position - 1] + seq[position - 1 + length:]


@dataclass
class MutationResult:
    category: str
    explanation: str
    reference_protein: str
    mutated_protein: str


def classify_change(reference: str, mutated: str, kind: str, edit_index: int) -> MutationResult:
    """Classify the effect of a change on a coding sequence.

    Only classifies when the reference really is a coding sequence in frame 1:
    it must start with ATG. (Arbitrary DNA is not assumed to be a gene.)

    ``kind`` is 'substitution', 'insertion' or 'deletion'.
    ``edit_index`` is the 0-based index in the REFERENCE where the change begins
    (for an insertion: the number of reference bases before the inserted bases).
    """
    ref = _require_valid(reference)
    mut = _require_valid(mutated)
    if kind not in ("substitution", "insertion", "deletion"):
        raise ValueError("kind must be 'substitution', 'insertion' or 'deletion'.")
    if not ref.startswith("ATG"):
        raise ValueError("The reference must begin with a start codon (ATG) to be read as a coding sequence.")

    ref_protein, ref_stop, _ = translate_coding(ref)
    mut_protein, mut_stop, _ = translate_coding(mut)
    # End of the coding region in the reference (including its stop codon, if any).
    coding_end = 3 * (len(ref_protein) + 1) if ref_stop else 3 * len(ref_protein)

    def result(category: str, text: str) -> MutationResult:
        return MutationResult(category, text, ref_protein, mut_protein)

    if mut == ref:
        return result("No change", "The sequence is identical to the reference.")
    if edit_index >= coding_end:
        return result(
            "Outside the translated region",
            "The change is after the stop codon, so the protein made from this reading frame is unchanged. "
            "(In real genes, regions outside the protein-coding sequence can still matter, e.g. for regulation.)",
        )
    if not mut.startswith("ATG"):
        return result(
            "Start codon altered",
            "The first codon is no longer ATG. Real cells may then use a different start site or make little or no protein; "
            "that is not modelled here, so no protein effect is predicted beyond this warning.",
        )

    length_change = len(mut) - len(ref)
    if kind in ("insertion", "deletion") and length_change % 3 != 0:
        if mut_stop and len(mut_protein) < len(ref_protein):
            tail = "and the shifted frame runs into an early stop codon, giving a shorter protein."
        elif mut_stop:
            tail = "and the shifted frame reaches a stop codon at a different place."
        else:
            tail = "and no stop codon is reached in the shifted frame within this sequence."
        return result(
            "Frameshift",
            f"The change adds/removes {abs(length_change)} base(s), which is not a multiple of 3. "
            f"Every codon after the change is read in a shifted frame, so the amino acids downstream are usually altered, {tail}",
        )
    if kind in ("insertion", "deletion"):
        expected_length = len(ref_protein) + length_change // 3
        if mut_stop and len(mut_protein) < expected_length:
            return result(
                "Premature stop codon (after an in-frame change)",
                "The reading frame is kept, but the change creates a stop codon earlier than expected.",
            )
        if ref_stop and not mut_stop:
            return result("Stop codon lost", "The change removes the stop codon, so translation would continue past the original end.")
        word = "insertion" if kind == "insertion" else "deletion"
        return result(
            f"In-frame {word}",
            f"A multiple of 3 bases was {'added' if kind == 'insertion' else 'removed'}, so the reading frame is kept "
            f"but the protein has {abs(length_change) // 3} amino acid(s) {'more' if kind == 'insertion' else 'fewer'} "
            "(and neighbouring amino acids may also change).",
        )

    # Substitutions
    if mut_protein == ref_protein and mut_stop == ref_stop:
        return result(
            "Synonymous (silent) change",
            "The codon changed, but it still codes for the same amino acid (or is still a stop codon), "
            "so the amino-acid sequence is unchanged. Silent changes can occasionally still matter in real cells, but that is beyond this model.",
        )
    if mut_stop and len(mut_protein) < len(ref_protein):
        return result(
            "Premature stop codon (nonsense change)",
            "A codon became a stop codon, so translation would end early and give a shorter protein.",
        )
    if ref_stop and not mut_stop:
        return result("Stop codon lost", "The stop codon changed into an amino-acid codon, so translation would continue past the original end.")
    return result(
        "Missense change",
        "One amino acid is different. The effect (none, mild or severe) depends on which amino acid changed, "
        "where it sits in the protein, and the biological context.",
    )


def analyse_mutation(reference: str, kind: str, position: int, detail) -> tuple[str, MutationResult]:
    """Apply a change and classify it. ``detail`` = new base, inserted bases, or deletion length."""
    if kind == "substitution":
        mutated = apply_substitution(reference, position, detail)
        edit_index = position - 1
    elif kind == "insertion":
        mutated = apply_insertion(reference, position, detail)
        edit_index = position
    elif kind == "deletion":
        mutated = apply_deletion(reference, position, int(detail))
        edit_index = position - 1
    else:
        raise ValueError("kind must be 'substitution', 'insertion' or 'deletion'.")
    return mutated, classify_change(reference, mutated, kind, edit_index)


# ---------------------------------------------------------------------------
# Simulated gene expression
# ---------------------------------------------------------------------------
# Fictional genes and fictional average expression levels (arbitrary units).
FICTIONAL_GENES = {
    "Gene H1 (always-on, 'housekeeping-like')": {"Neuron-like": 50, "Muscle-like": 52, "Epithelial-like": 48, "Blood-like": 51},
    "Gene N1 (neuron-biased)": {"Neuron-like": 90, "Muscle-like": 6, "Epithelial-like": 4, "Blood-like": 3},
    "Gene M1 (muscle-biased)": {"Neuron-like": 5, "Muscle-like": 85, "Epithelial-like": 8, "Blood-like": 4},
    "Gene E1 (epithelial-biased)": {"Neuron-like": 7, "Muscle-like": 9, "Epithelial-like": 80, "Blood-like": 6},
    "Gene B1 (blood-biased)": {"Neuron-like": 4, "Muscle-like": 5, "Epithelial-like": 6, "Blood-like": 88},
}
FICTIONAL_STAGES = {
    "Gene S1 (early-stage gene)": {"Stage 1": 80, "Stage 2": 55, "Stage 3": 20, "Stage 4": 8},
    "Gene S2 (mid-stage gene)": {"Stage 1": 5, "Stage 2": 40, "Stage 3": 85, "Stage 4": 30},
    "Gene S3 (late-stage gene)": {"Stage 1": 3, "Stage 2": 6, "Stage 3": 30, "Stage 4": 82},
    "Gene H1 (always-on, 'housekeeping-like')": {"Stage 1": 50, "Stage 2": 52, "Stage 3": 49, "Stage 4": 51},
}


def simulate_expression(gene_means: dict, replicates: int = 4, noise: float = 0.15, seed: int = 1):
    """Make fictional expression values: mean x (1 + random noise), never below zero.

    Returns a pandas DataFrame with columns gene, group, replicate, expression.
    """
    import pandas as pd

    if replicates < 1:
        raise ValueError("replicates must be at least 1")
    if noise < 0:
        raise ValueError("noise cannot be negative")
    rng = random.Random(seed)
    rows = []
    for gene, groups in gene_means.items():
        for group, mean in groups.items():
            for rep in range(1, replicates + 1):
                value = max(0.0, rng.gauss(mean, noise * mean))
                rows.append({"gene": gene, "group": group, "replicate": rep, "expression": round(value, 1)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Streamlit page
# ---------------------------------------------------------------------------
def render() -> None:
    import pandas as pd
    import streamlit as st
    from matplotlib.figure import Figure

    from modules.ui_helpers import background_notice, simulated_notice

    st.title("Genetics & molecular biology")
    st.write("How does information in DNA relate to the proteins that cells make — and what can go wrong when it changes?")
    tab_dna, tab_central, tab_mut, tab_expr = st.tabs(
        ["DNA analyser", "Transcription & translation", "Mutation explorer", "Gene expression"]
    )

    # ---- DNA analyser ----------------------------------------------------
    with tab_dna:
        st.subheader("DNA sequence analyser")
        st.caption("Enter the sequence 5' → 3'. Spaces and line breaks are ignored; letters are case-insensitive.")
        raw = st.text_area("DNA sequence", value="ATGGCTAAAGAATTCGGTCTGACCTGGTAA", key="gen_dna_input")
        ok, seq, message = validate_dna(raw)
        if not ok:
            st.error(message)
        else:
            counts = count_nucleotides(seq)
            percents = nucleotide_percentages(seq)
            c1, c2 = st.columns(2)
            c1.metric("Length (bases)", len(seq))
            c2.metric("GC content", f"{gc_content(seq):.1f}%")
            table = pd.DataFrame(
                {"Count": counts, "Percentage": {b: round(p, 1) for b, p in percents.items()}}
            )
            table.index.name = "Base"
            st.dataframe(table)
            st.bar_chart(table["Percentage"])
            st.markdown("**Complementary strands**")
            st.code(
                f"Input (5'→3')       : {seq}\n"
                f"Complement (3'→5')  : {complement(seq)}   <- written under the input, base by base\n"
                f"Reverse complement  : {reverse_complement(seq)}   <- same strand written 5'→3'",
                language=None,
            )
            st.info(
                "**What these statistics cannot tell you:** length, base counts and GC content do not identify a gene, "
                "predict a disease or establish what a sequence does. They are simple descriptions of a string of letters."
            )

    # ---- Central dogma ---------------------------------------------------
    with tab_central:
        st.subheader("From DNA to protein")
        background_notice(
            "DNA holds genetic information → transcription makes RNA from a DNA template → "
            "messenger RNA codons (3 bases each) are translated into amino acids → the amino-acid sequence contributes to "
            "protein structure and function."
        )
        st.markdown(
            "**Which strand is which?** Here you enter the **coding strand** (5'→3'). Its sequence matches the mRNA "
            "(with U instead of T). RNA polymerase actually reads the **template strand**, which is the complementary "
            "strand, and builds the RNA 5'→3'. Ribosomes read mRNA codons in the 5'→3' direction."
        )
        raw2 = st.text_area("Coding-strand DNA (5'→3')", value=EXAMPLE_SEQUENCES["Fictional sequence 1 (9 codons + stop)"], key="gen_central_input")
        start_mode = st.radio(
            "Where should translation begin?", ["First base of the sequence", "First ATG start codon"], key="gen_start_mode"
        )
        ok2, seq2, msg2 = validate_dna(raw2)
        if not ok2:
            st.error(msg2)
        else:
            start = 0
            if start_mode == "First ATG start codon":
                start = find_start_codon(seq2)
                if start == -1:
                    st.error("No ATG start codon was found in this sequence, so there is nothing to translate from a start codon.")
            if start != -1:
                st.code(
                    f"Coding strand (5'→3')   : {seq2}\n"
                    f"Template strand (3'→5') : {template_strand(seq2)}\n"
                    f"mRNA (5'→3')            : {transcribe_coding_strand(seq2)}",
                    language=None,
                )
                protein, stop_found, leftover = translate_coding(seq2, start=start, to_stop=False)
                codons = split_codons(seq2, start)
                rows = [
                    {"Codon (mRNA)": c.replace("T", "U"), "Amino acid": AMINO_ACID_NAMES[CODON_TABLE[c]][1],
                     "Symbol": AMINO_ACID_NAMES[CODON_TABLE[c]][0]}
                    for c in codons
                ]
                st.dataframe(pd.DataFrame(rows), hide_index=True)
                if "*" in protein:
                    st.write("Protein (one-letter code, up to the first stop): **" + protein.split("*")[0] + "**")
                else:
                    st.write("Protein (one-letter code): **" + protein + "**  — no stop codon reached.")
                if leftover % 3 and not stop_found:
                    st.caption(f"{len(seq2) - start - 3 * len(codons)} leftover base(s) at the end do not form a full codon.")
                st.warning(
                    "This tool translates whatever you type. A real gene also has regulatory regions, and in many organisms "
                    "its coding sequence is split by introns. An arbitrary sequence is **not** automatically a gene."
                )
        with st.expander("Show the full standard genetic code (64 codons)"):
            code_rows = [
                {"mRNA codon": c.replace("T", "U"), "Symbol": AMINO_ACID_NAMES[a][0], "Amino acid": AMINO_ACID_NAMES[a][1]}
                for c, a in CODON_TABLE.items()
            ]
            st.dataframe(pd.DataFrame(code_rows), hide_index=True)

    # ---- Mutation explorer ----------------------------------------------
    with tab_mut:
        st.subheader("Mutation explorer")
        st.write("Pick a **fictional** coding sequence and introduce one change. Positions count from 1.")
        name = st.selectbox("Example sequence", list(EXAMPLE_SEQUENCES), key="gen_mut_example")
        reference = EXAMPLE_SEQUENCES[name]
        ref_codons = " ".join(split_codons(reference))
        st.code(f"Reference codons: {ref_codons}\nReference protein: {translate_coding(reference)[0]}", language=None)
        kind = st.radio("Type of change", ["substitution", "insertion", "deletion"], horizontal=True, key="gen_mut_kind")
        error = None
        try:
            if kind == "substitution":
                position = st.number_input("Position to change", 1, len(reference), 4, key="gen_mut_pos_s")
                new_base = st.selectbox("New base", list(VALID_BASES), key="gen_mut_base")
                mutated, res = analyse_mutation(reference, kind, int(position), new_base)
            elif kind == "insertion":
                position = st.number_input("Insert after position", 1, len(reference), 6, key="gen_mut_pos_i")
                bases = st.text_input("Bases to insert (A/T/C/G)", value="G", key="gen_mut_ins")
                mutated, res = analyse_mutation(reference, kind, int(position), bases)
            else:
                position = st.number_input("Start deleting at position", 1, len(reference), 7, key="gen_mut_pos_d")
                length = st.number_input("Number of bases to delete", 1, 9, 1, key="gen_mut_len")
                mutated, res = analyse_mutation(reference, kind, int(position), int(length))
        except ValueError as exc:
            error = str(exc)
        if error:
            st.error(error)
        else:
            st.code(
                f"Mutated codons : {' '.join(split_codons(mutated))}"
                f"{'  (+ ' + str(len(mutated) % 3) + ' leftover base(s))' if len(mutated) % 3 else ''}\n"
                f"Mutated protein: {res.mutated_protein or '(none)'}",
                language=None,
            )
            st.success(f"**{res.category}** — {res.explanation}")
        st.info(
            "Not every mutation is harmful. Effects depend on the sequence, where the change sits, the cell type and "
            "environment, and other genes. This tool only reads the sequence you see; it does not predict a real organism's health."
        )

    # ---- Gene expression -------------------------------------------------
    with tab_expr:
        st.subheader("Gene expression explorer")
        simulated_notice()
        st.write(
            "Cells in one body share broadly the same genome but use different subsets of genes. "
            "Compare fictional expression across cell types or developmental stages."
        )
        mode = st.radio("Compare across", ["Cell types", "Developmental stages"], horizontal=True, key="gen_expr_mode")
        gene_means = FICTIONAL_GENES if mode == "Cell types" else FICTIONAL_STAGES
        noise = st.slider("Biological variation between replicates", 0.0, 0.4, 0.15, 0.05, key="gen_expr_noise")
        df = simulate_expression(gene_means, replicates=4, noise=noise, seed=7)
        means = df.pivot_table(index="gene", columns="group", values="expression", aggfunc="mean")
        means = means[list(next(iter(gene_means.values())))]  # keep the original column order
        fig = Figure(figsize=(6, 3))
        ax = fig.subplots()
        image = ax.imshow(means.values, aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(means.columns)), means.columns, rotation=20)
        ax.set_yticks(range(len(means.index)), [g.split(" (")[0] for g in means.index])
        fig.colorbar(image, ax=ax, label="Mean expression (simulated, arbitrary units)")
        ax.set_title("Simulated expression heat map")
        fig.tight_layout()
        st.pyplot(fig)
        gene = st.selectbox("Look at one gene in detail", list(gene_means), key="gen_expr_gene")
        sub = df[df["gene"] == gene]
        st.bar_chart(sub.groupby("group", sort=False)["expression"].mean())
        st.dataframe(sub[["group", "replicate", "expression"]], hide_index=True)
        st.caption(
            "Low expression of a gene in one cell type does not mean the gene is missing from that cell's genome — "
            "it means it is used less there."
        )

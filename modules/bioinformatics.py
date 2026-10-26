"""Module G: Beginner bioinformatics.

Small, honest demonstrations. Nothing here searches a real database - real tools
such as BLAST compare a sequence against millions of stored sequences using far
more sophisticated algorithms than the ones shown here.
"""
from __future__ import annotations

from modules.genetics import (
    CODON_TABLE,
    count_nucleotides,
    gc_content,
    reverse_complement,
    validate_dna,
)


# ---------------------------------------------------------------------------
# Reading several sequences at once
# ---------------------------------------------------------------------------
def parse_sequences(text: str | None) -> list[tuple[str, str]]:
    """Turn pasted text into a list of (name, sequence) pairs.

    * If the text contains FASTA headers (lines starting with '>'), each header starts a
      new record and the following lines are joined into one sequence.
    * Otherwise every non-empty line is treated as its own sequence ("Seq1", "Seq2", ...).
    Sequences are returned upper-case with spaces removed; they are NOT validated here.
    """
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    if not lines:
        return []
    records: list[tuple[str, str]] = []
    if any(line.startswith(">") for line in lines):
        name, chunks = None, []
        for line in lines:
            if line.startswith(">"):
                if name is not None:
                    records.append((name, "".join(chunks).upper().replace(" ", "")))
                name, chunks = line[1:].strip() or f"Seq{len(records) + 1}", []
            elif name is not None:
                chunks.append(line)
        if name is not None:
            records.append((name, "".join(chunks).upper().replace(" ", "")))
    else:
        records = [(f"Seq{i}", line.upper().replace(" ", "")) for i, line in enumerate(lines, 1)]
    return records


def summarise_records(records: list[tuple[str, str]]) -> list[dict]:
    """One summary row per sequence; invalid sequences are reported, not hidden."""
    rows = []
    for name, seq in records:
        ok, cleaned, message = validate_dna(seq)
        if ok:
            counts = count_nucleotides(cleaned)
            rows.append({"Name": name, "Valid": True, "Length": len(cleaned),
                         "GC %": round(gc_content(cleaned), 1), "A": counts["A"], "T": counts["T"],
                         "C": counts["C"], "G": counts["G"], "Problem": ""})
        else:
            rows.append({"Name": name, "Valid": False, "Length": len(cleaned), "GC %": None,
                         "A": None, "T": None, "C": None, "G": None, "Problem": message})
    return rows


# ---------------------------------------------------------------------------
# Comparing two short sequences
# ---------------------------------------------------------------------------
def percent_identity(seq_a: str, seq_b: str) -> float:
    """Percentage of matching positions between two sequences of EQUAL length."""
    ok_a, a, msg_a = validate_dna(seq_a)
    ok_b, b, msg_b = validate_dna(seq_b)
    if not ok_a:
        raise ValueError("Sequence A: " + msg_a)
    if not ok_b:
        raise ValueError("Sequence B: " + msg_b)
    if len(a) != len(b):
        raise ValueError("Sequences must be the same length for a position-by-position comparison.")
    matches = sum(x == y for x, y in zip(a, b))
    return 100 * matches / len(a)


def best_ungapped_match(seq_a: str, seq_b: str) -> dict:
    """Slide the shorter sequence along the longer one (no gaps allowed).

    Returns the offset (0-based, in the longer sequence) with the most matching bases.
    This is a toy version of alignment: real alignment also allows insertions/deletions (gaps)
    and uses scoring systems.
    """
    ok_a, a, msg_a = validate_dna(seq_a)
    ok_b, b, msg_b = validate_dna(seq_b)
    if not ok_a:
        raise ValueError("Sequence A: " + msg_a)
    if not ok_b:
        raise ValueError("Sequence B: " + msg_b)
    longer, shorter = (a, b) if len(a) >= len(b) else (b, a)
    best = {"offset": 0, "matches": -1}
    for offset in range(len(longer) - len(shorter) + 1):
        window = longer[offset:offset + len(shorter)]
        matches = sum(x == y for x, y in zip(window, shorter))
        if matches > best["matches"]:  # first best offset wins on ties
            best = {"offset": offset, "matches": matches}
    best["length_compared"] = len(shorter)
    best["identity_percent"] = 100 * best["matches"] / len(shorter)
    best["longer_is"] = "A" if len(a) >= len(b) else "B"
    return best


def kmer_set(sequence: str, k: int) -> set[str]:
    """All overlapping words of length k in the sequence."""
    ok, seq, message = validate_dna(sequence)
    if not ok:
        raise ValueError(message)
    if k < 1:
        raise ValueError("k must be at least 1.")
    return {seq[i:i + k] for i in range(len(seq) - k + 1)}


def kmer_similarity(seq_a: str, seq_b: str, k: int = 3) -> float:
    """Shared k-mers divided by all distinct k-mers in either sequence (0 to 1)."""
    a, b = kmer_set(seq_a, k), kmer_set(seq_b, k)
    union = a | b
    return len(a & b) / len(union) if union else 0.0


# ---------------------------------------------------------------------------
# Open reading frames (a simple demonstration)
# ---------------------------------------------------------------------------
def find_orfs(sequence: str, min_codons: int = 3) -> list[dict]:
    """Find simple open reading frames on the FORWARD strand: ATG ... stop codon.

    An ORF is only a stretch with no stop codon in one frame. Random DNA contains
    many short ORFs by chance, so finding one does not show that a real gene is present.
    """
    ok, seq, message = validate_dna(sequence)
    if not ok:
        raise ValueError(message)
    found = []
    for frame in range(3):
        i = frame
        while i + 3 <= len(seq):
            if seq[i:i + 3] == "ATG":
                j, protein = i, []
                while j + 3 <= len(seq):
                    aa = CODON_TABLE[seq[j:j + 3]]
                    j += 3
                    if aa == "*":
                        if len(protein) >= min_codons:
                            found.append({"frame": frame + 1, "start": i + 1, "end": j,
                                          "codons": len(protein), "protein": "".join(protein)})
                        break
                    protein.append(aa)
                    # (an ORF with no stop codon before the sequence ends is not reported)
                i = j  # continue scanning after this ORF (or after the failed attempt)
            else:
                i += 3
    return sorted(found, key=lambda orf: orf["codons"], reverse=True)


# ---------------------------------------------------------------------------
# Streamlit page
# ---------------------------------------------------------------------------
def render() -> None:
    import pandas as pd
    import streamlit as st

    from modules.ui_helpers import background_notice

    st.title("Beginner bioinformatics")
    st.write("Bioinformatics uses computing to store, compare and interpret biological data such as DNA sequences.")
    background_notice(
        "Real analyses use specialised software and large public databases. The tools below are small teaching demonstrations "
        "that run offline. They do **not** search any database."
    )
    tab_batch, tab_compare, tab_orf, tab_real = st.tabs(
        ["Check several sequences", "Compare two sequences", "Open reading frames", "What real tools do"]
    )

    with tab_batch:
        st.write("Paste one sequence per line, or several FASTA-style records (lines starting with `>` are names).")
        text = st.text_area(
            "Sequences", value=">fictional_A\nATGGCTAAAGAATTCGGTCTGACCTGGTAA\n>fictional_B\nATGGCTAAGGAATTCGGTCTGACGTGGTAA\n>typo_example\nATGCCXTAA",
            height=160, key="bio_batch_input",
        )
        records = parse_sequences(text)
        if not records:
            st.info("Enter at least one sequence.")
        else:
            table = pd.DataFrame(summarise_records(records))
            st.dataframe(table, hide_index=True)
            if (~table["Valid"]).any():
                st.warning("Some sequences were not valid DNA. See the 'Problem' column; they were left out of calculations.")

    with tab_compare:
        st.write("Compare two short sequences. Equal-length sequences are compared base by base; otherwise the shorter one is slid along the longer one.")
        col1, col2 = st.columns(2)
        seq_a = col1.text_input("Sequence A", "ATGGCTAAAGAATTCGGTCTGACCTGGTAA", key="bio_cmp_a")
        seq_b = col2.text_input("Sequence B", "ATGGCTAAGGAATTCGGTCTGACGTGGTAA", key="bio_cmp_b")
        k = st.slider("Word size k for k-mer similarity", 2, 6, 3, key="bio_cmp_k")
        try:
            a_clean, b_clean = validate_dna(seq_a)[1], validate_dna(seq_b)[1]
            if len(a_clean) == len(b_clean):
                identity = percent_identity(seq_a, seq_b)
                st.metric("Percent identity (position by position)", f"{identity:.1f}%")
                diffs = [i + 1 for i, (x, y) in enumerate(zip(a_clean, b_clean)) if x != y]
                st.write("Differences at positions: " + (", ".join(map(str, diffs)) if diffs else "none"))
            else:
                best = best_ungapped_match(seq_a, seq_b)
                st.metric(
                    "Best ungapped match",
                    f"{best['identity_percent']:.1f}%",
                    help=f"Shorter sequence compared at offset {best['offset']} of the longer sequence (sequence {best['longer_is']}).",
                )
            st.metric(f"Shared {k}-mers (0–100%)", f"{100 * kmer_similarity(seq_a, seq_b, k):.1f}%")
            st.write("Reverse complement of A (5'→3'): `" + reverse_complement(seq_a) + "`")
        except ValueError as exc:
            st.error(str(exc))
        st.info(
            "**Limits of sequence similarity:** similar sequences *may* share an evolutionary origin or function, but similarity "
            "depends on length, the method and chance. Short sequences can match by accident. Very different sequences can still "
            "give proteins with similar roles, and a single change can alter function even when 99% of bases match."
        )

    with tab_orf:
        st.write("An **open reading frame (ORF)** here means ATG followed by codons with no stop until a stop codon, on the forward strand.")
        orf_seq = st.text_area("DNA sequence", "CCATGGCTAAAGAATTCGGTCTGACCTGGTAAGGATGAAATTTTGACC", key="bio_orf_input")
        min_codons = st.slider("Minimum number of amino acids to report", 1, 20, 3, key="bio_orf_min")
        try:
            orfs = find_orfs(orf_seq, min_codons)
            if orfs:
                st.dataframe(pd.DataFrame(orfs), hide_index=True)
            else:
                st.write("No ORFs of that length were found on the forward strand.")
        except ValueError as exc:
            st.error(str(exc))
        st.warning(
            "Finding an ORF is **not** gene identification. Random sequences contain short ORFs by chance, the reverse strand "
            "is not searched here, and real genes are often split by introns."
        )

    with tab_real:
        st.markdown(
            "- **Alignment** algorithms allow gaps and use scoring rules, so they can line up sequences that differ by insertions or deletions.\n"
            "- **Database searches** (for example BLAST, run on public servers) compare your sequence with huge collections of known sequences and report how unlikely the match is by chance. This app does not connect to any database.\n"
            "- **Gene prediction** combines many signals (regulatory sequences, splice sites, evidence from RNA data), not just ORFs.\n"
            "- **Interpretation** still needs experiments: a computational prediction is a hypothesis, not a result."
        )

# Scientific background notes

These notes explain, in brief and in the author's own words, the main ideas behind each module. They are
**simplified teaching summaries**, not a literature review. Always check details against textbooks and the
sources listed at the bottom, and add proper citations (author, year, title) to your own notes as you read.

## Central question
How do scientists investigate the relationship between **genes, cells, development and disease**?

## Cell biology and development
- **Cell growth** = a cell increases in size/content. **Cell division** = one cell becomes two. **Cell differentiation** = a cell becomes specialised. They are different processes.
- Specialised cells in one body share broadly the same genome but use different subsets of genes (gene expression). Exceptions exist (e.g. mature mammalian red blood cells lose their nucleus).
- Development involves overlapping processes: division, cell signalling, movement, differentiation, tissue organisation and programmed cell death. Details differ between species.
- Stem cells can self-renew and produce more specialised cells; pluripotent cells can form all body cell types, multipotent cells a narrower range.

## Genetics and molecular biology
- The **coding strand** has the same sequence as the mRNA (T replaced by U). RNA polymerase reads the **template strand**.
- The **standard genetic code** maps 61 codons to 20 amino acids and 3 codons to "stop". ATG codes for methionine and is the usual start codon.
- Mutation effects, when a sequence really is coding and in frame: **synonymous** (same amino acid), **missense** (different amino acid), **nonsense** (premature stop), **frameshift** (insertion/deletion not a multiple of 3). Many changes are harmless; effects depend on context.
- The app's example sequences are **fictional**.

## Model systems
Each model trades off speed, cost, genetic tools, ability to observe living tissue, similarity to human biology and ethical considerations. No model is correct for every question. Generation times and similar figures in the app are approximate.

## Zebrafish
Embryos develop outside the mother and are transparent early, which allows live imaging of development. Genetic tools allow gene activity to be altered and cells to be labelled. Zebrafish can regenerate some tissues (e.g. fin, heart muscle after injury). They are vertebrates but are not small humans: results need to be tested in other systems.

## Statistics used in the virtual lab
A **permutation test** compares the observed difference with the differences obtained when group labels are shuffled many times. A **paired sign-flip test** does the equivalent for repeated measurements on the same subjects. Neither assumes a normal distribution; both assume independent subjects and a fair design. A small p-value does not show a difference is biologically important, and the datasets are fictional.

## Claims you should verify yourself before repeating them
- The age at which zebrafish become regulated research animals in the UK (the app says "around five days after fertilisation").
- Approximate generation times in the comparison table.
- The role of specific transcription factors named in the Cell Differentiation Explorer (NEUROD1, MYOD1, GATA1) and the sickle-cell example.

## Sources
See `modules/sources.py` (also shown on the *Sources & limitations* page). The links were supplied as starting points and were **not opened or verified** when this project was created.

# Analysis: Attention Is All You Need


## Methods

- Methods used:
  - Neural Machine Translation (NMT)
  - Attention Mechanism in NMT
  - Self-attention in NMT (Layer 5 of 6)
  - Deep Recurrent Models with Fast-Forward Connections for NMT (mentioned but not detailed)

- Architectures:
  - Google's Neural Machine Translation System (not detailed)
  - Sparse-gated Mixture-of-Experts Layer (mentioned but not detailed)

- Datasets:
  - Not explicitly stated in the excerpts provided

- Training Setup:
  - Optimizer: Not explicitly stated
  - Learning Rate (lr): Not explicitly stated
  - Training Steps: Not explicitly stated

- Evaluation Metrics:
  - Not explicitly stated in the excerpts provided

## Key Results

- Attention heads in the encoder self-attention layer 5 of 6 exhibit behavior related to sentence structure and task performance.
- Two attention heads in layer 5 appear to be involved in anaphora resolution.
- The attention mechanism follows long-distance dependencies in the encoder self-attention in layer 5, completing phrases such as 'making...more difficult'.
- A majority of American governments have passed new laws since 2009 making the registration or voting process more difficult.

## Limitations

LIMITATIONS:
- The study is based on Google's neural machine translation system, which may not be representative of all machine translation systems.
- The analysis is limited to the behavior of attention heads in a specific layer (layer 5 of 6) of the system.
- The study assumes that the observed behavior of the attention heads is related to the structure of the sentence and specific tasks.
- The study does not provide a comprehensive explanation for the observed behavior of the attention heads.

OPEN QUESTIONS:
- How do the attention heads in other layers of the system behave?
- Are the observed behaviors of the attention heads consistent across different types of sentences and tasks?
- What are the underlying mechanisms that cause the attention heads to perform different tasks?
- How can the observed behaviors of the attention heads be used to improve the performance of the machine translation system?
- What are the failure modes of the attention mechanism in the machine translation system?
- What assumptions are made in the analysis of the attention heads' behavior?
- What is the scope of the study in terms of the types of sentences and tasks it covers?
- How does the machine translation system handle long-distance dependencies in sentences?
- How can the machine translation system be improved to better handle anaphora resolution?
- How can the machine translation system be improved to better handle the registration or voting process in American governments?
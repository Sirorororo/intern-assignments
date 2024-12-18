## Answers to Transformer Questions Based on "Attention Is All You Need" Paper

### 1. How does the transformer architecture improve upon traditional seq2seq models?
The Transformer improves upon traditional seq2seq models (RNNs or LSTMs) by eliminating recurrence and convolutions. Instead, it relies entirely on self-attention mechanisms to process input sequences in parallel.
The key improvements include:
- **Parallelization**: Since the model processes the input all at once, it trains faster and efficiently leverages GPUs/TPUs.
- **Long-range dependencies**: Self-attention captures relationships between distant words more effectively.
- **Scalability**: Transformer architecture provides better scalability on large datasets.

### 2. What are the key differences between global and local attention mechanisms?

In global attention mechanism, every token attends to every other token in the sequence, providing full context. However, it is computationally expensive.

In local attention, each token attends to a limited window of neighboring tokens, reducing computational costs but sacrificing some context.

### 3. How does the attention mechanism help in processing long-distance dependencies?
Self-attention allows each token to attend to every other token in the sequence, regardless of their position. This avoids the vanishing gradient issues seen in RNNs/LSTMs and directly captures long-range dependencies in a single computation step. Then, positional encodings ensure that the model understands the order of tokens.

### 4. Why was the name "Transformer" chosen for the model?
The Transformer model is named as such because of its unique architecture that relies solely on self-attention mechanisms, which allow it to transform input sequences into output sequences.

### 5. How does the parallelizability of the Transformer contribute to its efficiency?
Transformers process input sequences in parallel rather than sequentially (as in RNNs). This allows:
- Faster training times due to parallel computation.
- Efficient use of hardware resources like GPUs and TPUs.
- Scalability to larger datasets and longer sequences.

### 6. What are 'multi-head attention' mechanisms, and why are they beneficial?
Multi-head attention splits the input into multiple subspaces and applies self-attention independently on each subspace. Outputs are concatenated and linearly transformed.

The benefits of multi-head attention are:
- It aptures different types of relationships (e.g., syntactic and semantic) between tokens simultaneously.
- It improves representation learning by combining multiple perspectives from different heads.

### 7. How does multi-head attention differ from single-head attention?
Single head attention applies one attention function, limiting the capacity to capture diverse relationships.

Whereas, multi-head attention uses multiple attention heads to process the input from different subspaces. The results are concatenated and transformed, enhancing the model's ability to learn richer representations.

### 8. What is the role of positional encoding in the Transformer, and why is it necessary?
Transformers lack recurrence and convolution, so they cannot inherently understand the order of tokens.

Positional encoding is added to the input embeddings to inject information about token positions. This ensures that the model understands the order and relative positions of tokens.

### 9. Explain the concept of "self-attention" and how it is used in the Transformer model.
Self-attention allows each token in the input to attend to all other tokens (including itself) to compute its representation. It is the backbone of the Transformer model.

Steps of self-attention:
1. Input tokens are projected into Query **(Q)**, Key **(K)**, and Value **(V)** matrices.
2. The attention score is computed using scaled dot-product attention:
   $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
3. The result is a weighted sum of the value vectors, where the weights are derived from the attention scores.

Self-attention enables the model to relate each word to all other words in a sequence simultaneously.

### 10. Why is self-attention a crucial component for parallelizing computations?
Self-attention computes relationships between all tokens simultaneously using matrix operations, which can be parallelized efficiently on GPUs/TPUs.

Unlike RNNs, which process input sequentially, self-attention allows the Transformer to process the entire input in parallel, significantly reducing training time and enabling scalability.

### 11. How are Transformers usually trained (Encoder and Decoder)?
Encoder processes the input sequence and produces context-rich representations.
Decoder generates the output sequence step-by-step, attending to the encoder's outputs and previous tokens.

Training uses teacher forcing, where ground-truth tokens are fed into the decoder during training to predict the next token.

### 12. Define BLEU score and other metrics (Perplexity, ROUGE).
- **BLEU (Bilingual Evaluation Understudy)**: It measures the similarity between predicted and reference translations using n-gram overlaps.
- **Perplexity**: It evaluates language model performance. Lower perplexity indicates better predictions.
- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**: It measures overlap between predicted and reference text summaries (recall-based).

### 13. How does layer normalization differ from other normalization, and how does it help?
Layer Normalization normalizes inputs across the features (not batch dimension). It stabilizes training and improves convergence for Transformers. Unlike batch normalization, layer normalization does not depend on batch size and works well for non-recurrent architectures.

### 14. Is Transformer a parallel computing machine (model)?
Yes, the Transformer is designed for parallel computation. It processes input tokens simultaneously using matrix operations and self-attention.

### 15. Do you think attention is good for low-resource tasks?
Simpler models might perform adequately for very small datasets. However attention mechanisms can still benefit low-resource tasks by:
- Capturing important relationships in the data.
- Allowing models to focus on relevant tokens.

### 16. What things are learned inside the Transformer?
Transformers learn contextual relationships between tokens through attention mechanisms.Positional information are learned through positional encodings and rich representations of input data is learned via multi-head attention and feedforward layers.

### 17. Can we use other than softmax in (QVT)?
Softmax is typically used to compute attention scores because it produces a probability distribution. Alternatives like sparsemax or entmax can also be used to create sparser distributions.

### 18. What is auto-regressive, when auto-regressive is used in Encoder or in Decoder, and why?
Auto-regressive refers to generating one token at a time, conditioning on previously generated tokens.
In Transformers, the decoder is auto-regressive during inference to ensure tokens are generated sequentially.

This approach prevents the model from seeing future tokens when predicting the current token.

### 19. 512-2048-512, why? Is this block really important?
This refers to the feedforward network dimensions:
- Input and output have 512 dimensions.
- The hidden layer expands to 2048 dimensions.

This expansion increases the model's capacity to learn complex representations and is crucial for performance.

### 20. Key difference in encoder vs decoder; can we use decoder for all tasks?
Encoder processes input sequences into contextual representations.
Whereas, decoder generates output sequences based on encoder outputs and previous tokens.

While the decoder could theoretically be adapted for other tasks, the encoder is better suited for tasks like classification or encoding-only tasks.

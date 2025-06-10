# Mathematical Document Test

This document tests various mathematical expressions and their rendering.

## Inline Math Examples

The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$ which is fundamental in algebra.

Einstein's mass-energy equivalence: \(E = mc^2\) changed our understanding of physics.

The area of a circle is $A = \pi r^2$ where $r$ is the radius.

## Block Math Examples

### Basic Equations

$$
f(x) = ax^2 + bx + c
$$

### Integrals

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

### Matrix Operations

\[
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
\begin{pmatrix}
x \\
y
\end{pmatrix}
=
\begin{pmatrix}
ax + by \\
cx + dy
\end{pmatrix}
\]

### Summations and Series

$$
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
$$

### Complex Equations

$$
\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u
$$

### Greek Letters and Sets

Let $\alpha, \beta, \gamma \in \mathbb{R}$ and $f: \mathbb{N} \rightarrow \mathbb{Z}$.

$$
\forall x \in \mathbb{R}, \exists y \in \mathbb{C} : |y|^2 = x^2 + 1
$$

### Trigonometric Functions

$$
\sin^2(x) + \cos^2(x) = 1
$$

$$
e^{i\theta} = \cos(\theta) + i\sin(\theta)
$$

### Limits

$$
\lim_{x \to 0} \frac{\sin(x)}{x} = 1
$$

### Fractions and Roots

The golden ratio: $\phi = \frac{1 + \sqrt{5}}{2}$

$$
\sqrt[n]{x^n} = |x| \text{ for } x \in \mathbb{R}
$$

## Mixed Content

Here we have some regular text, then some inline math like $\log_2(8) = 3$, followed by a code block:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

And then a mermaid diagram:

```mermaid
graph TD
    A[Start] --> B{Is n ≤ 1?}
    B -->|Yes| C[Return n]
    B -->|No| D[Calculate fib(n-1) + fib(n-2)]
    D --> E[Return result]
    C --> F[End]
    E --> F
```

Finally, another block equation:

$$
F_n = F_{n-1} + F_{n-2}
$$

Where $F_n$ represents the $n$-th Fibonacci number.

## Error Testing

This should work: $x^2 + y^2 = z^2$

This might cause issues (intentionally malformed): $\frac{incomplete

This should still work after the error: \(\alpha + \beta = \gamma\)
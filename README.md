# md2pdf

A lightweight command-line tool to convert Markdown files to PDF with minimal dependencies.

## Features

- **Simple CLI**: Just run `md2pdf input.md` to convert
- **Mermaid Support**: Automatically converts mermaid diagrams to images via mermaid.ink
- **MathJax Support**: Renders LaTeX math expressions to SVG images
- **Minimal Dependencies**: Uses only essential Python libraries
- **Error Handling**: Shows placeholders for failed images/diagrams/math
- **Pure Python**: No external system dependencies required

## Installation

### From Source

1. Clone or download this repository
2. Navigate to the project directory
3. Install in editable mode:

```bash
pip install -e .
```

### From PyPI (when published)

```bash
pip install md2pdf
```

## Usage

### Basic Usage

Convert a markdown file to PDF:

```bash
md2pdf example.md
```

This will create `example.pdf` in the same directory.

### Specify Output File

```bash
md2pdf input.md -o output.pdf
```

### Verbose Mode

```bash
md2pdf input.md -v
```

## Supported Markdown Features

- **Headings** (H1-H6)
- **Paragraphs** and line breaks
- **Bold** and *italic* text
- **Code blocks** and `inline code`
- **Lists** (ordered and unordered)
- **Tables**
- **Images** (local files and URLs)
- **Blockquotes**
- **Links**
- **Mermaid diagrams** (converted to images)
- **Mathematical expressions** (LaTeX syntax)

## Mathematical Expressions

The tool supports LaTeX mathematical expressions in multiple formats:

### Inline Math

Use `$...# md2pdf

A lightweight command-line tool to convert Markdown files to PDF with minimal dependencies.

## Features

- **Simple CLI**: Just run `md2pdf input.md` to convert
- **Mermaid Support**: Automatically converts mermaid diagrams to images via mermaid.ink
- **MathJax Support**: Renders LaTeX math expressions to SVG images
- **Minimal Dependencies**: Uses only essential Python libraries
- **Error Handling**: Shows placeholders for failed images/diagrams/math
- **Pure Python**: No external system dependencies required

## Installation

### From Source

1. Clone or download this repository
2. Navigate to the project directory
3. Install in editable mode:

```bash
pip install -e .
```

### From PyPI (when published)

```bash
pip install md2pdf
```

## Usage

### Basic Usage

Convert a markdown file to PDF:

```bash
md2pdf example.md
```

This will create `example.pdf` in the same directory.

### Specify Output File

```bash
md2pdf input.md -o output.pdf
```

### Verbose Mode

```bash
md2pdf input.md -v
```

## Supported Markdown Features

- **Headings** (H1-H6)
- **Paragraphs** and line breaks
- **Bold** and *italic* text
- **Code blocks** and `inline code`
- **Lists** (ordered and unordered)
- **Tables**
- **Images** (local files and URLs)
- **Blockquotes**
- **Links**
- **Mermaid diagrams** (converted to images)
- **Mathematical expressions** (LaTeX syntax)

 or `\(...\)` for inline expressions:

```markdown
The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$ which solves quadratic equations.

Alternatively: \(E = mc^2\) is Einstein's famous equation.
```

### Block Math

Use `$...$` or `\[...\]` for display equations:

```markdown
$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$

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
```

### Advanced Features Supported

- **Fractions**: `\frac{numerator}{denominator}`
- **Superscripts/Subscripts**: `x^2`, `H_2O`
- **Greek letters**: `\alpha`, `\beta`, `\gamma`, etc.
- **Integrals**: `\int`, `\oint`, `\iint`
- **Matrices**: `\begin{pmatrix}...\end{pmatrix}`
- **Summations**: `\sum_{i=1}^{n}`
- **Square roots**: `\sqrt{x}`, `\sqrt[n]{x}`
- **Trigonometric functions**: `\sin`, `\cos`, `\tan`
- **Logarithms**: `\log`, `\ln`
- **Sets**: `\mathbb{R}`, `\mathbb{N}`, `\mathbb{Z}`
- **Arrows**: `\rightarrow`, `\Leftarrow`, `\leftrightarrow`
- **And much more!**

If math expression rendering fails, a placeholder will be shown with the original LaTeX code.

## Dependencies

- `markdown` - Markdown parsing
- `reportlab` - PDF generation
- `Pillow` - Image processing
- `requests` - Downloading images and mermaid diagrams

## Requirements

- Python 3.12+

## License

MIT License

## Development

### Project Structure

```
md2pdf/
├── pyproject.toml
├── src/
│   └── md2pdf/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── converter.py        # Main converter class
│       ├── parser.py           # Markdown parser with mermaid support
│       ├── mathjax_processor.py # MathJax LaTeX processing
│       └── pdf_generator.py    # PDF generation logic
└── README.md
```

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Known Limitations

- Table rendering is simplified
- Limited CSS styling support
- Mermaid diagrams require internet connection
- Math expressions require internet connection
- Complex nested math structures may need manual formatting

## Troubleshooting

### Common Issues

1. **"Command not found" error**: Make sure the package is installed with `pip install -e .`
2. **Mermaid diagrams not showing**: Check your internet connection
3. **Images not loading**: Verify image URLs are accessible

### Getting Help

If you encounter issues:

1. Run with verbose mode (`-v`) to see detailed output
2. Check that all dependencies are installed
3. Verify your input markdown file is valid
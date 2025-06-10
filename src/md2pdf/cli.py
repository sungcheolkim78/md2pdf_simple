#!/usr/bin/env python3
"""
Command-line interface for md2pdf converter.
"""

import argparse
import sys
from pathlib import Path
from .converter import MarkdownToPDFConverter


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to PDF",
        prog="md2pdf"
    )
    
    parser.add_argument(
        "input_file",
        help="Input Markdown file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path (default: input file with .pdf extension)",
        default=None
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"Error: '{input_path}' is not a file.", file=sys.stderr)
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.pdf')
    
    # Convert markdown to PDF
    converter = MarkdownToPDFConverter(verbose=args.verbose)
    converter.convert(input_path, output_path)
    print(f"Successfully converted '{input_path}' to '{output_path}'")


if __name__ == "__main__":
    main()
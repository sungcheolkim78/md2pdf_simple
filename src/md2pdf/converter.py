"""
Main converter class that orchestrates markdown to PDF conversion.
"""

from pathlib import Path
from .parser import MarkdownParser
from .pdf_generator import HTMLToPDFConverter


class MarkdownToPDFConverter:
    """Main converter class."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.parser = MarkdownParser(verbose=verbose)
        self.pdf_generator = HTMLToPDFConverter(verbose=verbose)
    
    def convert(self, input_path: Path, output_path: Path):
        """
        Convert markdown file to PDF.
        
        Args:
            input_path: Path to input markdown file
            output_path: Path to output PDF file
        """
        if self.verbose:
            print(f"Reading markdown file: {input_path}")
        
        # Read markdown content
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            raise Exception(f"Failed to read input file: {e}")
        
        if self.verbose:
            print("Parsing markdown content...")
        
        # Parse markdown to HTML
        html_content = self.parser.parse(markdown_content)
        
        if self.verbose:
            print(f"Generating PDF: {output_path}")
        
        # Convert HTML to PDF
        try:
            self.pdf_generator.convert_to_pdf(html_content, output_path)
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {e}")
        
        if self.verbose:
            print("Conversion completed successfully!")
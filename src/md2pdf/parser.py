"""
Markdown parser with mermaid diagram and MathJax support.
"""

import re
import base64
import requests
from urllib.parse import quote
from typing import List, Tuple, Optional
import markdown
from markdown.extensions import tables, codehilite, fenced_code
from .mathjax_processor import MathJaxProcessor


class MermaidProcessor:
    """Handles mermaid diagram processing."""
    
    MERMAID_INK_BASE = "https://mermaid.ink/img/"
    
    @staticmethod
    def extract_mermaid_blocks(text: str) -> List[Tuple[str, str]]:
        """
        Extract mermaid code blocks from markdown text.
        Returns list of (full_block, mermaid_code) tuples.
        """
        pattern = r'```mermaid\n(.*?)\n```'
        matches = []
        
        for match in re.finditer(pattern, text, re.DOTALL):
            full_block = match.group(0)
            mermaid_code = match.group(1).strip()
            matches.append((full_block, mermaid_code))
        
        return matches
    
    @staticmethod
    def generate_mermaid_url(mermaid_code: str) -> str:
        """Generate mermaid.ink URL for the given mermaid code."""
        # Encode the mermaid code
        encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
        return f"{MermaidProcessor.MERMAID_INK_BASE}{encoded}"
    
    @staticmethod
    def replace_mermaid_with_images(text: str, verbose: bool = False) -> str:
        """
        Replace mermaid code blocks with image links.
        """
        mermaid_blocks = MermaidProcessor.extract_mermaid_blocks(text)
        
        for full_block, mermaid_code in mermaid_blocks:
            try:
                # Generate image URL
                image_url = MermaidProcessor.generate_mermaid_url(mermaid_code)
                
                # Test if the URL is accessible
                response = requests.head(image_url, timeout=10)
                if response.status_code == 200:
                    # Replace with markdown image syntax
                    image_markdown = f"![Mermaid Diagram]({image_url})"
                    text = text.replace(full_block, image_markdown)
                    if verbose:
                        print(f"Generated mermaid diagram: {image_url}")
                else:
                    # Replace with placeholder
                    placeholder = "![Mermaid Diagram - Failed to Generate](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2YwZjBmMCIgc3Ryb2tlPSIjY2NjIi8+PHRleHQgeD0iMTAwIiB5PSI1NSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5NZXJtYWlkIERpYWdyYW08L3RleHQ+PC9zdmc+)"
                    text = text.replace(full_block, placeholder)
                    if verbose:
                        print(f"Failed to generate mermaid diagram, using placeholder")
            
            except Exception as e:
                # Replace with placeholder on any error
                placeholder = "![Mermaid Diagram - Error](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2ZmZWVlZSIgc3Ryb2tlPSIjZmY2NjY2Ii8+PHRleHQgeD0iMTAwIiB5PSI1NSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5FcnJvcjogTWVybWFpZDwvdGV4dD48L3N2Zz4=)"
                text = text.replace(full_block, placeholder)
                if verbose:
                    print(f"Error processing mermaid diagram: {e}")
        
        return text


class MarkdownParser:
    """Enhanced markdown parser with mermaid and MathJax support."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.md = markdown.Markdown(
            extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'toc',
                'nl2br'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': False  # Use simple highlighting
                }
            }
        )
    
    def parse(self, markdown_text: str) -> str:
        """
        Parse markdown text to HTML, processing mermaid diagrams and math expressions first.
        """
        # Process math expressions first (before mermaid to avoid conflicts)
        if self.verbose:
            print("Processing math expressions...")
        processed_text = MathJaxProcessor.replace_math_with_images(
            markdown_text, 
            verbose=self.verbose
        )
        
        # Process mermaid diagrams
        if self.verbose:
            print("Processing mermaid diagrams...")
        processed_text = MermaidProcessor.replace_mermaid_with_images(
            processed_text, 
            verbose=self.verbose
        )
        
        # Convert to HTML
        if self.verbose:
            print("Converting to HTML...")
        html = self.md.convert(processed_text)
        
        return html
    
    def get_toc(self) -> str:
        """Get table of contents if available."""
        return getattr(self.md, 'toc', '')
"""
MathJax processor for converting LaTeX math to SVG images.
"""

import re
import base64
import requests
import json
from typing import List, Tuple, Optional
from urllib.parse import quote


class MathJaxProcessor:
    """Handles MathJax math expression processing."""
    
    # MathJax SVG rendering service
    MATHJAX_API_BASE = "https://math.vercel.app"
    
    # Math patterns for different formats
    PATTERNS = {
        'inline_dollar': r'\$([^$\n]+)\$',  # $...$
        'block_dollar': r'\$\$\n?(.*?)\n?\$\$',  # $$...$$
        'inline_paren': r'\\\(([^)]+)\\\)',  # \(...\)
        'block_bracket': r'\\\[\n?(.*?)\n?\\\]',  # \[...\]
    }
    
    @staticmethod
    def extract_math_expressions(text: str) -> List[Tuple[str, str, str]]:
        """
        Extract math expressions from text.
        Returns list of (full_match, latex_code, math_type) tuples.
        math_type is either 'inline' or 'block'
        """
        expressions = []
        
        # Block math first (to avoid conflicts with inline)
        for pattern_name, pattern in [
            ('block_dollar', MathJaxProcessor.PATTERNS['block_dollar']),
            ('block_bracket', MathJaxProcessor.PATTERNS['block_bracket'])
        ]:
            for match in re.finditer(pattern, text, re.DOTALL):
                full_match = match.group(0)
                latex_code = match.group(1).strip()
                expressions.append((full_match, latex_code, 'block'))
        
        # Remove found block expressions to avoid conflicts
        temp_text = text
        for full_match, _, _ in expressions:
            temp_text = temp_text.replace(full_match, '')
        
        # Inline math
        for pattern_name, pattern in [
            ('inline_dollar', MathJaxProcessor.PATTERNS['inline_dollar']),
            ('inline_paren', MathJaxProcessor.PATTERNS['inline_paren'])
        ]:
            for match in re.finditer(pattern, temp_text):
                full_match = match.group(0)
                latex_code = match.group(1).strip()
                expressions.append((full_match, latex_code, 'inline'))
        
        return expressions
    
    @staticmethod
    def generate_math_svg_url(latex_code: str, is_inline: bool = False) -> str:
        """
        Generate MathJax API URL for the given LaTeX code.
        Uses math.vercel.app service which provides SVG rendering.
        """
        # Clean up the LaTeX code
        latex_code = latex_code.strip()
        
        # For block math, ensure it's properly formatted
        if not is_inline and not latex_code.startswith('\\begin') and not latex_code.startswith('\\['):
            # Wrap in display math if not already
            if not latex_code.startswith('$$'):
                latex_code = f"\\displaystyle {latex_code}"
        
        # URL encode the LaTeX
        encoded_latex = quote(latex_code)
        
        # Build the API URL
        # The service expects: https://math.vercel.app/?from=latex&to=svg&input=...
        return f"{MathJaxProcessor.MATHJAX_API_BASE}/?from=latex&to=svg&input={encoded_latex}"
    
    @staticmethod
    def render_math_to_svg(latex_code: str, is_inline: bool = False, verbose: bool = False) -> Optional[str]:
        """
        Render LaTeX math to SVG using MathJax service.
        Returns SVG data URL or None if failed.
        """
        try:
            # Try the Vercel math service first
            api_url = MathJaxProcessor.generate_math_svg_url(latex_code, is_inline)
            
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200 and response.content:
                # Check if it's valid SVG
                svg_content = response.text
                if svg_content.strip().startswith('<svg') and '</svg>' in svg_content:
                    # Convert to data URL
                    svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                    return f"data:image/svg+xml;base64,{svg_b64}"
            
            # Fallback: try alternative MathJax service
            return MathJaxProcessor._try_alternative_service(latex_code, is_inline, verbose)
            
        except Exception as e:
            if verbose:
                print(f"Error rendering math '{latex_code[:50]}...': {e}")
            return MathJaxProcessor._try_alternative_service(latex_code, is_inline, verbose)
    
    @staticmethod
    def _try_alternative_service(latex_code: str, is_inline: bool = False, verbose: bool = False) -> Optional[str]:
        """Try alternative math rendering service."""
        try:
            # Alternative: use QuickLaTeX service
            quicklatex_url = "https://quicklatex.com/latex3.f"
            
            # Prepare the formula
            formula = latex_code
            if not is_inline:
                formula = f"\\displaystyle {formula}"
            
            data = {
                'formula': formula,
                'fsize': '17px' if is_inline else '20px',
                'fcolor': '000000',
                'mode': '0',  # SVG mode
                'out': '1',   # SVG output
                'remhost': 'quicklatex.com'
            }
            
            response = requests.post(quicklatex_url, data=data, timeout=15)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                if len(lines) >= 2 and lines[0].strip() == '0':  # Success
                    svg_url = lines[1].strip()
                    # Download the SVG
                    svg_response = requests.get(svg_url, timeout=10)
                    if svg_response.status_code == 200:
                        svg_content = svg_response.text
                        svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                        return f"data:image/svg+xml;base64,{svg_b64}"
            
        except Exception as e:
            if verbose:
                print(f"Alternative service also failed for '{latex_code[:50]}...': {e}")
        
        return None
    
    @staticmethod
    def create_math_placeholder(latex_code: str, is_inline: bool = False) -> str:
        """Create a placeholder for failed math rendering."""
        if is_inline:
            # Simple placeholder for inline math
            placeholder_svg = f"""<svg width="80" height="20" xmlns="http://www.w3.org/2000/svg">
                <rect width="80" height="20" fill="#f0f0f0" stroke="#ccc"/>
                <text x="40" y="15" text-anchor="middle" font-family="Arial" font-size="10" fill="#666">Math</text>
            </svg>"""
        else:
            # Larger placeholder for block math
            placeholder_svg = f"""<svg width="200" height="60" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="60" fill="#fff0f0" stroke="#ffcccc"/>
                <text x="100" y="25" text-anchor="middle" font-family="Arial" font-size="12" fill="#666">Math Expression</text>
                <text x="100" y="45" text-anchor="middle" font-family="monospace" font-size="10" fill="#999">{latex_code[:30]}...</text>
            </svg>"""
        
        # Convert to data URL
        svg_b64 = base64.b64encode(placeholder_svg.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{svg_b64}"
    
    @staticmethod
    def replace_math_with_images(text: str, verbose: bool = False) -> str:
        """
        Replace math expressions with image links.
        """
        math_expressions = MathJaxProcessor.extract_math_expressions(text)
        
        # Sort by position (reverse order to avoid position shifts)
        math_expressions.sort(key=lambda x: text.find(x[0]), reverse=True)
        
        for full_match, latex_code, math_type in math_expressions:
            try:
                is_inline = (math_type == 'inline')
                
                # Try to render the math
                svg_data_url = MathJaxProcessor.render_math_to_svg(
                    latex_code, 
                    is_inline=is_inline, 
                    verbose=verbose
                )
                
                if svg_data_url:
                    # Create markdown image
                    alt_text = f"Math: {latex_code[:50]}..." if len(latex_code) > 50 else f"Math: {latex_code}"
                    image_markdown = f"![{alt_text}]({svg_data_url})"
                    
                    if verbose:
                        print(f"Rendered math: {latex_code[:50]}...")
                else:
                    # Use placeholder
                    placeholder_url = MathJaxProcessor.create_math_placeholder(latex_code, is_inline)
                    alt_text = f"Math (failed): {latex_code[:30]}..."
                    image_markdown = f"![{alt_text}]({placeholder_url})"
                    
                    if verbose:
                        print(f"Failed to render math, using placeholder: {latex_code[:50]}...")
                
                # Replace in text
                text = text.replace(full_match, image_markdown)
                
            except Exception as e:
                # Use placeholder on any error
                placeholder_url = MathJaxProcessor.create_math_placeholder(latex_code, math_type == 'inline')
                alt_text = f"Math (error): {latex_code[:30]}..."
                image_markdown = f"![{alt_text}]({placeholder_url})"
                text = text.replace(full_match, image_markdown)
                
                if verbose:
                    print(f"Error processing math '{latex_code[:50]}...': {e}")
        
        return text
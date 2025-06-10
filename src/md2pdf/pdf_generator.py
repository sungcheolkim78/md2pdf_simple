"""
PDF generator using ReportLab.
"""

import re
import io
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import requests
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, red, green
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class HTMLToPDFConverter:
    """Convert HTML to PDF using ReportLab."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
        self.image_cache = {}
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=12,
            textColor=black
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=10,
            spaceBefore=10,
            textColor=black
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=8,
            textColor=black
        ))
        
        # Code style
        self.styles.add(ParagraphStyle(
            name='MarkdownCode',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=10,
            backgroundColor='#f5f5f5',
            borderWidth=1,
            borderColor='#cccccc',
            leftIndent=10,
            rightIndent=10,
            spaceAfter=6,
            spaceBefore=6
        ))
        
        # Language-specific code styles
        self.styles.add(ParagraphStyle(
            name='MarkdownCodePython',
            parent=self.styles['MarkdownCode'],
            textColor='#0000FF'  # Blue for Python
        ))
        
        self.styles.add(ParagraphStyle(
            name='MarkdownCodeJavaScript',
            parent=self.styles['MarkdownCode'],
            textColor='#008000'  # Green for JavaScript
        ))
        
        self.styles.add(ParagraphStyle(
            name='MarkdownCodeShell',
            parent=self.styles['MarkdownCode'],
            textColor='#800000'  # Maroon for Shell
        ))
        
        # Blockquote style
        self.styles.add(ParagraphStyle(
            name='BlockQuote',
            parent=self.styles['Normal'],
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor='#cccccc',
            spaceBefore=6,
            spaceAfter=6
        ))
    
    def _download_image(self, url: str) -> Optional[io.BytesIO]:
        """Download image from URL and return as BytesIO."""
        try:
            if url in self.image_cache:
                return self.image_cache[url]
            
            if url.startswith('data:'):
                # Handle data URLs
                header, data = url.split(',', 1)
                image_data = base64.b64decode(data)
                image_io = io.BytesIO(image_data)
                self.image_cache[url] = image_io
                return image_io
            
            # Download from URL
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            image_io = io.BytesIO(response.content)
            self.image_cache[url] = image_io
            return image_io
            
        except Exception as e:
            if self.verbose:
                print(f"Failed to download image {url}: {e}")
            return None
    
    def _process_image(self, img_tag: str) -> Optional[RLImage]:
        """Process HTML img tag and return ReportLab Image."""
        # Extract src attribute
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        if not src_match:
            return None
        
        src = src_match.group(1)
        
        # Extract alt text
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag)
        alt_text = alt_match.group(1) if alt_match else "Image"
        
        # Download image
        image_io = self._download_image(src)
        if not image_io:
            if self.verbose:
                print(f"Failed to download image from {src}")
            return None
        
        try:
            # Create ReportLab image
            image_io.seek(0)
            
            # Verify image can be opened by PIL first
            try:
                Image.open(image_io).verify()
                image_io.seek(0)  # Reset position after verify
            except Exception as e:
                if self.verbose:
                    print(f"Invalid image format from {src}: {e}")
                return None
            
            img = RLImage(image_io)
            
            # Special handling for math images (typically smaller)
            is_math = "Math" in alt_text or "math" in alt_text.lower()
            
            # Resize if too large
            max_width = 6 * inch
            max_height = 4 * inch
            
            # For math expressions, use smaller max sizes
            if is_math:
                if "inline" in alt_text.lower() or img.drawHeight < 30:
                    # Inline math - keep smaller
                    max_height = 0.5 * inch
                    max_width = 4 * inch
                else:
                    # Block math
                    max_height = 2 * inch
                    max_width = 5 * inch
            
            if img.drawWidth > max_width:
                img.drawHeight = img.drawHeight * (max_width / img.drawWidth)
                img.drawWidth = max_width
            
            if img.drawHeight > max_height:
                img.drawWidth = img.drawWidth * (max_height / img.drawHeight)
                img.drawHeight = max_height
            
            return img
            
        except Exception as e:
            if self.verbose:
                print(f"Failed to process image from {src}: {e}")
            return None
    
    def _get_code_style(self, language: str) -> str:
        """Get the appropriate code style based on language."""
        language = language.lower() if language else ''
        if language == 'python':
            return 'MarkdownCodePython'
        elif language in ['javascript', 'js']:
            return 'MarkdownCodeJavaScript'
        elif language in ['shell', 'bash', 'sh']:
            return 'MarkdownCodeShell'
        return 'MarkdownCode'
    
    def _html_to_story(self, html: str):
        """Convert HTML to ReportLab story elements."""
        # Simple HTML parsing - split by major tags
        lines = html.split('\n')
        current_paragraph = []
        in_code_block = False
        current_code_block = []
        current_language = None
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Handle code blocks
            if '<code' in line or '<pre' in line:
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                # Check if this is the start of a code block
                if not in_code_block:
                    in_code_block = True
                    # Extract language class if present
                    lang_match = re.search(r'class=["\']language-([^"\']+)["\']', line)
                    current_language = lang_match.group(1) if lang_match else None
                    # Remove the opening tag and get initial content
                    line = re.sub(r'<[^>]+>', '', line)
                    if line.strip():
                        current_code_block.append(line)
                else:
                    # Inside code block, just add the line
                    current_code_block.append(line)
                continue
            
            # Check for end of code block
            if in_code_block and ('</code>' in line or '</pre>' in line):
                # Remove the closing tag and add any remaining content
                line = re.sub(r'</[^>]+>', '', line)
                if line.strip():
                    current_code_block.append(line)
                
                # Process the complete code block
                code_text = '\n'.join(current_code_block)
                code_text = self._clean_html_tags(code_text)
                print(code_text)
                
                # Use appropriate style based on language
                style_name = self._get_code_style(current_language)
                self.story.append(Paragraph(code_text, self.styles[style_name]))
                
                # Reset code block state
                in_code_block = False
                current_code_block = []
                current_language = None
                continue
            
            # If we're inside a code block, collect the lines
            if in_code_block:
                current_code_block.append(line)
                continue
            
            # Handle headings
            if line.startswith('<h1'):
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                # Extract heading text and ID if present
                heading_match = re.match(r'<h1(?:\s+id="([^"]+)")?>(.*?)</h1>', line)
                if heading_match:
                    heading_id, text = heading_match.groups()
                    # For now we just use the text, but we could use the ID for TOC or links
                    self.story.append(Paragraph(text, self.styles['CustomHeading1']))
                continue
            
            elif line.startswith('<h2'):
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                # Extract heading text and ID if present
                heading_match = re.match(r'<h2(?:\s+id="([^"]+)")?>(.*?)</h2>', line)
                if heading_match:
                    heading_id, text = heading_match.groups()
                    self.story.append(Paragraph(text, self.styles['CustomHeading2']))
                continue
            
            elif line.startswith('<h3'):
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                # Extract heading text and ID if present
                heading_match = re.match(r'<h3(?:\s+id="([^"]+)")?>(.*?)</h3>', line)
                if heading_match:
                    heading_id, text = heading_match.groups()
                    self.story.append(Paragraph(text, self.styles['CustomHeading3']))
                continue
            
            # Handle images
            elif '<img' in line:
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                img = self._process_image(line)
                if img:
                    self.story.append(img)
                continue
            
            # Handle blockquotes
            elif line.startswith('<blockquote>'):
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                
                text = re.sub(r'</?blockquote>', '', line)
                text = self._clean_html_tags(text)
                self.story.append(Paragraph(text, self.styles['BlockQuote']))
                continue
            
            # Handle tables (simplified)
            elif '<table>' in line:
                if current_paragraph:
                    self._add_paragraph('\n'.join(current_paragraph))
                    current_paragraph = []
                # Skip table processing for now
                continue
            
            # Regular paragraph content
            else:
                current_paragraph.append(line)
        
        # Add any remaining paragraph
        if current_paragraph:
            self._add_paragraph('\n'.join(current_paragraph))
    
    def _add_paragraph(self, text: str):
        """Add a paragraph to the story."""
        if not text.strip():
            return
        
        # Clean HTML tags
        clean_text = self._clean_html_tags(text)
        if clean_text.strip():
            self.story.append(Paragraph(clean_text, self.styles['Normal']))
    
    def _clean_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        # Handle common HTML entities
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        text = text.replace('&quot;', '"')
        text = text.replace('&nbsp;', ' ')
        
        # Remove HTML tags but keep content
        text = re.sub(r'<[^>]+>', '', text)
        
        return text
    
    def convert_to_pdf(self, html: str, output_path: Path):
        """Convert HTML to PDF file."""
        self.story = []
        
        # Convert HTML to story
        self._html_to_story(html)
        
        # Build PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            author="Sung-Cheol Kim",
        )
        
        doc.build(self.story)
"""
PDF Resume Parser using PyMuPDF (fitz)
Extracts and cleans text from PDF resumes.
"""
import fitz  # PyMuPDF
import re
from typing import Optional


class PDFParser:
    """Parse PDF resumes and extract clean text"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            full_text = "\n".join(text_parts)
            return PDFParser._clean_text(full_text)
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> Optional[str]:
        """
        Extract text from PDF bytes (for uploaded files).
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text_parts = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            full_text = "\n".join(text_parts)
            return PDFParser._clean_text(full_text)
            
        except Exception as e:
            print(f"Error extracting text from PDF bytes: {e}")
            return None



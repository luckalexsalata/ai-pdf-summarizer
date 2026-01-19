import io
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract


class PDFParser:
    """
    PDF parser that supports text extraction from PDFs with images and tables.
    Uses pdfplumber for text and tables, and OCR for images.
    """
    
    async def parse_pdf(self, pdf_bytes: bytes) -> str:
        """
        Parse PDF and extract all text content.
        Supports text, tables, and images (via OCR).
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Extracted text content as string
        """
        text_parts = []
        
        try:
            # First, try to extract text directly from PDF
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                # Check if PDF has pages
                if len(pdf.pages) == 0:
                    return "PDF file is empty (no pages found)"
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}\n")
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables, 1):
                        if table:
                            table_text = self._format_table(table)
                            text_parts.append(f"\n--- Table {table_num} on Page {page_num} ---\n{table_text}\n")
            
            # If we got good text content, return it
            full_text = "\n".join(text_parts)
            if len(full_text.strip()) > 100:
                return full_text
            
            # If text extraction was poor, try OCR on images (fallback)
            try:
                images = convert_from_bytes(pdf_bytes, dpi=200)
                ocr_text_parts = []
                
                for page_num, image in enumerate(images, 1):
                    try:
                        ocr_text = pytesseract.image_to_string(image, lang='eng')
                        if ocr_text.strip():
                            ocr_text_parts.append(f"--- Page {page_num} (OCR) ---\n{ocr_text}\n")
                    except Exception:
                        # Skip OCR for this page if it fails
                        continue
                
                if ocr_text_parts:
                    return "\n".join(ocr_text_parts)
            except Exception:
                # OCR not available or failed, return what we have
                pass
            
            return full_text if full_text else "Could not extract text from PDF"
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _format_table(self, table: list) -> str:
        """
        Format a table structure into readable text.
        
        Args:
            table: Table data as list of rows
            
        Returns:
            Formatted table as string with pipe separators
        """
        if not table:
            return ""
        
        formatted_rows = []
        for row in table:
            if row:
                clean_row = [str(cell) if cell is not None else "" for cell in row]
                formatted_rows.append(" | ".join(clean_row))
        
        return "\n".join(formatted_rows)

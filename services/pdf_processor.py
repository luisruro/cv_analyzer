import PyPDF2
from io import BytesIO

class PDFTextExtractor:
    def extract_text_df(self, pdf_file):
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            complete_text = ""
            
            for page_number, page in enumerate(pdf_reader.pages, start=1):
                text_page = page.extract_text()
                if text_page.strip():
                    complete_text += f"\n--- PAGE {page_number} ---\n"
                    complete_text += text_page + "\n"
            complete_text = complete_text.strip()
            
            if not complete_text:
                return "Error: PDF is empty or contains images"
            
            return complete_text
        except Exception as e:
            return f"Error to process PDF file: {str(e)}"
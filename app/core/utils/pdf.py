import fitz

def pdf_extract(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF: {e}")
        return None
    return text
	



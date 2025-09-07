import logging
import os
import re
from PyPDF2 import PdfReader
from src.utils.utils import logging, progress_bar

class DataExtractionInitialise:
    def __init__(self):
        self.datapath = "objects/data"
        self.start_page = 1
        self.end_page = -1

    def read_file_names(self) -> list:
        try:
            files = os.listdir(self.datapath)
            self.filenames = []
            for file in files:
                if file.split(".")[-1] == "pdf":
                    self.filenames.append(os.path.join(self.datapath, file))
            logging.info(f"Found {len(self.filenames)} pdfs.")
            logging.info(self.filenames)
            return self.filenames
        except Exception as e:
            logging.error(f"Error occured during reading filepath. {e}")


class DataExtraction:
    def extract_raw_text(self, filepath: str, page_limit: int = None) -> str:
        try:
            text = ""
            reader = PdfReader(filepath)
            total_pages = len(reader.pages)

            if page_limit is not None:
                total_pages = min(total_pages, page_limit)

            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text += " " + (page.extract_text() or "")
                progress_bar(
                    page_num + 1, total_pages,
                    prefix=f"Extracting {filepath}: ",
                    suffix="Complete" if page_num + 1 == total_pages else ""
                )

            return text
        except Exception as e:
            logging.error(f"Error occurred during reading file. {e}")
            return ""

    def filter_text(self, text) -> list[str]:
        try:
            formatted_text = list(text.replace("\n", " ").strip())
            final_text = []
            for char in formatted_text:
                if char.isalpha() or char.isdigit() or char == " ":
                    final_text.append(char)
            return final_text
        except Exception as e:
            logging.error(
                f"Error during filtering text by digits, special characters and alphabets: {e}"
            )

    def extract_english_text(self, text: str) -> str:
        try:
            if not text:
                raise ValueError("text cannot be None or empty.")

            english_matches = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]*\b", text)
            english_text = " ".join(english_matches)
            english_text = re.sub(r"\s+", " ", english_text).strip()

            logging.info(f"Extracted {len(english_matches)} English words")
            return english_text
        except Exception as e:
            logging.error(f"Error during extracting English text: {e}")
            raise

    def extract_hindi_text(self, text: str) -> str:
        try:
            if not text:
                raise ValueError("text cannot be None or empty.")

            hindi_matches = re.findall(r"[\u0900-\u097F]+", text)
            hindi_text = " ".join(hindi_matches)
            hindi_text = re.sub(r"\s+", " ", hindi_text).strip()

            logging.info(f"Extracted {len(hindi_matches)} Hindi words")
            return hindi_text
        except Exception as e:
            logging.error(f"Error during extracting Hindi text: {e}")
            raise

    def extract_both_languages(self, text: str) -> dict:
        try:
            if not text:
                raise ValueError("text cannot be None or empty.")

            english_text = self.extract_english_text(text)
            hindi_text = self.extract_hindi_text(text)

            result = {
                "english": english_text,
                "hindi": hindi_text,
                "english_word_count": len(english_text.split())
                if english_text
                else 0,
                "hindi_word_count": len(hindi_text.split()) if hindi_text else 0,
            }

            logging.info(
                f"Language extraction complete - EN: {result['english_word_count']} words, HI: {result['hindi_word_count']} words"
            )
            return result
        except Exception as e:
            logging.error(f"Error during extracting both languages: {e}")
            raise

    def filter_lang(self, text: str, language: str) -> str:
        try:
            if not text:
                raise ValueError("text cannot be None.")
            if not language:
                raise ValueError("language cannot be None.")

            if language == "en":
                text = re.findall(r"[a-zA-Z]+", text)
            elif language == "hi":
                text = re.findall(r"[\u0900-\u097F]+", text)

            return " ".join(text) if isinstance(text, list) else text
        except Exception as e:
            logging.error(f"Error during filtering raw text by language: {e}")
            raise


def extract_data() -> dict:
    """
    Extract raw text and return both English and Hindi content.
    Returns a dictionary with language-separated text.
    """
    try:
        data_extraction_init = DataExtractionInitialise()
        filenames = data_extraction_init.read_file_names()
        data_extraction = DataExtraction()
        data = []
        
        for filepath in filenames:
            logging.info(filepath)
            text = data_extraction.extract_raw_text(filepath).replace('  ', ' ')
            data.append(''.join(data_extraction.filter_text(text)))
                
        combined_text = '. '.join(data)
        language_data = data_extraction.extract_both_languages(combined_text)
        language_data['raw_text'] = combined_text
               	 
        return language_data
        
    except Exception as e:
        logging.error(f"Error during extracting raw text: {e}")
        raise

def extract_languages_from_text(text: str) -> dict:
    """
    Convenience function to extract languages from any text string.
    """
    try:
        data_extraction = DataExtraction()
        return data_extraction.extract_both_languages(text)
    except Exception as e:
        logging.error(f"Error during language extraction: {e}")
        raise

if __name__ == "__main__":
    # Example usage with PDF extraction
    language_data = extract_data()
    print("=== EXTRACTION RESULTS ===")
    print("\n=== ENGLISH TEXT ===")
    print(language_data['english'])
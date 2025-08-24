import logging
import os
from PyPDF2 import PdfReader
import glob

from src.utils.logger import logging

class DataExtractionInitialise:
	def __init__(self):
		self.datapath = 'objects/data'
		self.start_page = 1
		self.end_page = -1

	def read_file_names(self) -> list:
		try:
			# self.filenames = ["COI_2024.pdf"] #os.listdir(self.datapath)
			self.filenames = glob.glob(f"{self.datapath}/**/*.pdf", recursive=True)
			logging.info(f"Found {len(self.filenames)} pdfs.")
			logging.info(self.filenames)
			return self.filenames
		except Exception as e:
			logging.error(f"Error occured during reading filepath. {e}")


class DataExtraction:
	def extract_data(self, filepath) -> str:
		try:
			text = ""
			reader = PdfReader(filepath)
			for page_num in range(len(reader.pages)):
				if page_num <=5: # adding a temporary limit
					page = reader.pages[page_num]
					text += " " + page.extract_text()
					logging.info(f"Extracted page {page_num}")
			return text

		except Exception as e:
			logging.error(f"Error occured during reading file. {e}")


	def filter_text(self, text) -> list[str]:
		formatted_text = list(text.replace('\n', ' ').strip())
		final_text = []
		for char in formatted_text:
			if char.isalpha() or char.isdigit() or char == ' ':
				final_text.append(char)
		return final_text

	def filter_lang(self, text: str, language: str) -> str:
		if not text:
			return ValueError("text cannot be None.")
		if not language:
			return ValueError("language cannot be None.")

		if language == 'en':	
			text = re.findall(r"[a-zA-Z]+", text)
		if language == 'hi':
			text = re.findall(r'[\u0900-\u097F]+', text)

		return text

def main() -> str:
	data_extraction_init = DataExtractionInitialise()
	filenames = data_extraction_init.read_file_names()

	data_extraction = DataExtraction()
	data = []
	for filepath in filenames:
		logging.info(filepath)

		text = data_extraction.extract_data(filepath).replace('  ', '')
		data.append(''.join(data_extraction.filter_text(text)))

	text_data = '. '.join(data)

	# en_text = data_extraction.filter_lang(text=text_data,
	# 									  language='en')

	# hi_text = data_extraction.filter_lang(text=text_data,
	# 									  language='hi')

	return text_data


if __name__=="__main__":
	main()
	
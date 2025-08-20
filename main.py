from src.data_ingestion.data_extraction import Extraction
from src.vector_db import LegalVectorDB


# db = LegalVectorDB()

# # Run a query
# query = "What is a cognizable offence?"
# results = db.query(query)
# print(results)


data = Extraction()
print(data)
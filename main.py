from src.vector_db import LegalVectorDB


db = LegalVectorDB()

# Add documents (only once)
#db.add_documents(legal_data)

# Run a query
query = "What is a cognizable offence?"
results = db.query(query)
print(results)

# print("Search Results:\n")
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"Section {meta['section']} | {meta['title']}")
#     print(doc[:250], "...\n")
from src.vector_db import LegalVectorDB


db = LegalVectorDB()

# Add documents (only once)
#db.add_documents(legal_data)

# Run a query
query = "What is a cognizable offence?"
results = db.query(query)
reranked = db.rerank(query,results)
#print(reranked)
# print("Search Results:\n")
for id , doc , meta , score in reranked:
    print("ID:", id)
    print("Document:", doc[:100], "...")  
    print("Metadata:", meta)
    print("Score:", score)
    print("-" * 50)
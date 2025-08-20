import json
import re
from typing import Dict, Any
import chromadb
import logging
from src.utils.logger import logging
from sentence_transformers import SentenceTransformer


class LegalVectorDB:
    _client = None 
    def __init__(self, db_path="objects/database/chroma_db", model_name="all-MiniLM-L6-v2"):
        """Initialize ChromaDB client and embedding model."""

        if LegalVectorDB._client is None:
            LegalVectorDB._client = chromadb.PersistentClient(path=db_path)  # init once
            
        self.client = LegalVectorDB._client
        self.model = SentenceTransformer(model_name)
        self.collection = self.client.get_or_create_collection(name="legal_docs")
        self.model_path = 'objects/tokenizer_model/all-MiniLM-L6-v2'

    def __post_init__(self):
        self.model.save(self.model_path)

    def preprocess_document(self, doc: Dict[str, Any]) -> Dict[str, str]:
        combined_text = f"Section Title : { doc['section_title']} , Section_description: {doc['section_desc']}"
        combined_text = ' '.join(combined_text.split())  # normalize whitespace

        return {
            "id": f"ch{doc['chapter']}_sec{doc['section']}",  # unique ID
            "text": combined_text,                            # clean text for embeddings
            "chapter": str(doc['chapter']),
            "section": str(doc['section']),
            "title": doc['section_title'],
            "description": doc['section_desc']
        }

    def add_documents(self, data: list):
        """Preprocess and insert documents into the vector DB."""
        for doc in data:
            clean_doc = self.preprocess_document(doc)
            embedding = self.model.encode(clean_doc["text"]).tolist()

            self.collection.add(
                ids=[clean_doc["id"]],
                embeddings=[embedding],
                documents=[clean_doc["text"]],
                metadatas=[{
                    "chapter": clean_doc["chapter"],
                    "section": clean_doc["section"],
                    "title": clean_doc["title"]
                }]
            )

    def query(self, query_text: str, n_results: int = 3):
        """Search documents using cosine similarity."""
        clean_query = ' '.join(query_text.split())  # clean query too
        query_embedding = self.model.encode(clean_query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results



if __name__ == "__main__":
    #with open("C:/Users/rajes/assistant/Legal-Assistant-AI/objects/data/crpc.json", "r", encoding="utf-8") as f:
        #legal_data = json.load(f)

    db = LegalVectorDB()

    # Add documents (only once)
    #db.add_documents(legal_data)

    # Run a query
    query = "What is a cognizable offence?"
    results = db.query(query)

    print("Search Results:\n")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"Section {meta['section']} | {meta['title']}")
        print(doc[:250], "...\n")

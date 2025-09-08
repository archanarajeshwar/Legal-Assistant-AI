from dataclasses import dataclass, field
from vector_db.create_vector_db import LegalVectorDB

import logging    
import csv

@dataclass
class TestRetrieval:
    db: LegalVectorDB = field(default_factory=LegalVectorDB)

    def test_retrieval(self, query: str):
        results = self.db.query(query)
        reranked_results = self.db.rerank(query, results)

        for id, doc, meta, score in reranked_results:
            print("ID:", id)
            print("Document:", doc[:100], "...")  # print first 100 chars
            print("Metadata:", meta)
            print("Score:", score)
            print("-" * 50)


if __name__ == "__main__":
    tester = TestRetrieval()
    test_queries = [
    # Basic Definition Queries
    "What is a cognizable offence?",
    "Define non-cognizable offence.",
    "What is a warrant case?",
    "What is a summons case?",
    "Who is considered a police officer in this Code?",

    # Procedural Queries
    "How is an investigation started by police?",
    "When can a magistrate take cognizance of an offence?",
    "What is the process for issuing a summons?",
    "What is the procedure for granting bail?",
    "When can a case be transferred to another court?",

    # Authority & Powers Queries
    "Who has the power to arrest without a warrant?",
    "When can a magistrate order an inquiry?",
    "What powers do Sessions Courts have under this Code?",
    "What is the power of police to search a place?",
    "Who can order the release of an accused on bail?",

    # Edge-case / Complex Queries
    "What happens if a complaint is made against a husband by his wife under section 376B?",
    "Can a private citizen make an arrest?",
    "When does a trial become invalid?",
    "What is the difference between inquiry and investigation?",
    "Explain the procedure for recording confessions by magistrate."
]

    with open("retrieval_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "id", "document_snippet", "metadata", "score"])
        for query in test_queries:
            reranked_results = tester.test_retrieval(query)
            if not reranked_results:
                writer.writerow([query, "NO_RESULTS", "", "", ""])
                continue

            for id, doc, meta, score in reranked_results:
                writer.writerow([query, id, doc[:100], meta, score])

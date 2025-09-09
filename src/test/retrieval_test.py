from dataclasses import dataclass, field
from vector_db import LegalVectorDB
import pandas
import logging    

@dataclass
class TestRetrieval:
    db: LegalVectorDB = field(default_factory=LegalVectorDB)

    def test_retrieval(self, query: str):
        results = self.db.query(query)
        reranked_results = self.db.rerank(query, results)
        logging.info(f"reranked_results: {reranked_results}")
        return reranked_results
        # for id, doc, meta, score in reranked_results:
        #     print("ID:", id)
        #     print("Document:", doc[:100], "...")  # print first 100 chars
        #     print("Metadata:", meta)
        #     print("Score:", score)
        #     print("-" * 50)


if __name__ == "__main__":
    tester = TestRetrieval()
    test_queries = [
    # Basic Definition Queries
    "What is a cognizable offence?",
    "Define non-cognizable offence.",
    "What is a warrant case?",
    "What is a summons case?",
    "Who is considered a police officer in this Code?",

    #Procedural Queries
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
    all_results = []

   
    for query in test_queries:
        reranked_results = tester.test_retrieval(query)
        
        if not reranked_results:
            all_results.append({
                "query": query,
                "id": "NO_RESULTS",
                "document_snippet": "",
                "metadata": "",
                "score": ""
            })
            continue

        for id, doc, meta, score in reranked_results:
            all_results.append({
                "query": query,
                "id": id,
                "document_snippet": doc[:200],  # first 200 chars
                "metadata": meta,
                "score": score
            })
    df = pandas.DataFrame(all_results)

    df.to_csv("retrieval_results.csv", index=False, encoding="utf-8")

#$env:PYTHONPATH="src"
#python src\test\retrieval_test.py
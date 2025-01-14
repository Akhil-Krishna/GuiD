# main/utils/rag_utils.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from pathlib import Path

class RAGProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.index = None
        self.documents = []
        self.questions = []
        self.initialize_knowledge_base()

    def initialize_knowledge_base(self):
        # Get the base directory
        base_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = base_dir / 'data'
        
        # CSV files to process
        csv_files = [
            'python_coding.csv',
            'Geeks_For_Geeks_Questions_Dataset.csv',
            'Dataset_Python_Question_Answer.csv'
        ]
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(data_dir / csv_file)
                
                # Find question and answer columns
                question_col = next((col for col in df.columns 
                                   if col.lower() in ['question', 'questions']), None)
                answer_col = next((col for col in df.columns 
                                 if col.lower() in ['answer', 'answers']), None)
                
                if question_col and answer_col:
                    for q, a in zip(df[question_col], df[answer_col]):
                        if pd.notna(q) and pd.notna(a):
                            self.questions.append(str(q).lower())
                            self.documents.append(f"Question: {q}\nAnswer: {a}")
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")
                continue

        if self.documents:
            # Create embeddings for questions
            self.question_embeddings = self.vectorizer.fit_transform(self.questions)
            
            # Initialize FAISS index
            embeddings = self.question_embeddings.toarray()
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings.astype('float32'))

    def find_similar_questions(self, query, threshold=0.5):
        """Find if query is similar to any existing questions."""
        if not self.documents:
            return False, None
            
        query_vec = self.vectorizer.transform([query.lower()])
        
        # Get similarity scores
        scores = (query_vec * self.question_embeddings.T).toarray()[0]
        
        # Find best match
        best_score = np.max(scores)
        
        if best_score >= threshold:
            # Get top 3 similar questions
            top_indices = np.argsort(scores)[-3:][::-1]
            context = "\n\n".join([self.documents[i] for i in top_indices])
            return True, context
        
        return False, None

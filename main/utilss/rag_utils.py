# main/utils/rag_utils.py changingggggggggggggggggggggggggggggg
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from pathlib import Path
import PyPDF2
import re

class RAGProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.index = None
        self.documents = []
        self.questions = []
        self.website_docs = []  # Store website-related documents
        self.initialize_knowledge_base()

    def process_pdf(self, pdf_path):
        """Process PDF and extract text with metadata"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from each page
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                # Clean and process the text
                cleaned_text = re.sub(r'\s+', ' ', text).strip()
                
                # Add to website documents with metadata
                doc_entry = {
                    'content': cleaned_text,
                    'source': pdf_path.name,
                    'type': 'website_info'
                }
                self.website_docs.append(doc_entry)
                
                # Create searchable chunks
                chunks = self.create_chunks(cleaned_text)
                for chunk in chunks:
                    self.questions.append(chunk.lower())
                    self.documents.append(f"Website Information:\n{chunk}")
                
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")

    def create_chunks(self, text, chunk_size=1000, overlap=200):
        """Split text into overlapping chunks for better search"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            if end > text_length:
                end = text_length
            
            # Find the last period or newline in the chunk to avoid cutting sentences
            last_period = max(text.rfind('.', start, end), text.rfind('\n', start, end))
            if last_period != -1 and last_period > start:
                end = last_period + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks

    def initialize_knowledge_base(self):
        # Get the base directory
        base_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = base_dir / 'data'
        
        # Process coding-related CSV files
        csv_files = [
            'python_coding.csv',
            'Geeks_For_Geeks_Questions_Dataset.csv',
            'Dataset_Python_Question_Answer.csv'
        ]
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(data_dir / csv_file)
                
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

        # Process website-related PDFs
        pdf_dir = data_dir / 'website_docs'
        if pdf_dir.exists():
            for pdf_file in pdf_dir.glob('*.pdf'):
                self.process_pdf(pdf_file)

        if self.documents:
            # Create embeddings for all questions and chunks
            self.question_embeddings = self.vectorizer.fit_transform(self.questions)
            
            # Initialize FAISS index
            embeddings = self.question_embeddings.toarray()
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings.astype('float32'))

    def find_similar_questions(self, query, threshold=0.5, top_k=3):
        """Find if query is similar to any existing questions or website content."""
        if not self.documents:
            return False, None
            
        query_vec = self.vectorizer.transform([query.lower()])
        
        # Get similarity scores
        scores = (query_vec * self.question_embeddings.T).toarray()[0]
        
        # Find best match
        best_score = np.max(scores)
        
        if best_score >= threshold:
            # Get top k similar documents
            top_indices = np.argsort(scores)[-top_k:][::-1]
            context = "\n\n".join([self.documents[i] for i in top_indices])
            return True, context
        
        return False, None
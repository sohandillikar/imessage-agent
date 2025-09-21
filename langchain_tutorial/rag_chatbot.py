import os
import glob
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

class RAGChatbot:
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(api_key=api_key, model_name=model_name, temperature=0.7)
        
        self.journal_entries = []
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.conversations = {}
        
        # Load and process journal entries
        self._load_journal_entries()
        self._create_vectorstore()
    
    def _load_journal_entries(self):
        """Load all journal entries from the journals directory."""
        journal_files = glob.glob(f"./journals/rosebud-entry-*.md")

        for file_path in journal_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract date from filename
            filename = os.path.basename(file_path)
            date_str = filename.replace("rosebud-entry-", "").replace(".md", "")
            entry_date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
            
            # Parse journal entry
            entry_data = self._parse_journal_entry(content, entry_date)
            self.journal_entries.append(entry_data)

        print(f"Loaded {len(self.journal_entries)} journal entries")
    
    # TODO: Remove "Rosebud:" and "Sohan Dillikar:" from the entry content
    def _parse_journal_entry(self, content: str, entry_date: datetime) -> Dict[str, Any]:
        """Parse a journal entry and extract key information."""
        lines = content.split('\n')
        
        title = None
        emotions = []
        topics = []
        people = []
        entry_content = ""
        
        for i, line in enumerate(lines):
            if line.startswith("##") and title is None:
                title = line.replace("##", "").strip()
            elif "**Emotions:**" in line:
                emotions = [e.strip() for e in line.replace("**Emotions:**", "").split(",") if e.strip()]
            elif "**Topics:**" in line:
                topics = [t.strip() for t in line.replace("**Topics:**", "").split(",") if t.strip()]
            elif "**People:**" in line:
                people = [p.strip() for p in line.replace("**People:**", "").split(",") if p.strip()]
            elif "#### Entry" in line:
                entry_content = "\n".join(lines[i+1:]).replace("*", "")
                break
        
        return {
            "date": entry_date,
            "title": title,
            "emotions": emotions,
            "topics": topics,
            "people": people,
            "content": entry_content,
            "full_content": content
        }
    
    def _create_vectorstore(self):
        """Create a vector store from journal entries."""
        if not self.journal_entries:
            print("No journal entries found!")
            return
        
        documents = [entry['content'] for entry in self.journal_entries]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.create_documents(documents)

        for chunk in chunks:
            for entry in self.journal_entries:
                if chunk.page_content in entry['content']:
                    chunk.metadata = {
                        "title": entry['title'],
                        "date": entry['date'].strftime('%Y-%m-%d %H:%M:%S'),
                        "emotions": entry['emotions'],
                        "topics": entry['topics'],
                        "people": entry['people']
                    }
                    break
        
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        print(f"Created vector store with {len(chunks)} chunks")
    
    def _get_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from journal entries."""
        if not self.vectorstore:
            print("No vector store found!")
            return
        
        # Search for relevant documents
        docs = self.vectorstore.similarity_search(query, k=k)

        for doc in docs:
            print(doc)
            exit()

def main():
    chatbot = RAGChatbot(api_key=os.getenv("OPENAI_API_KEY"))

    chatbot._get_relevant_context(query="What did I do today?")

if __name__ == "__main__":
    main()

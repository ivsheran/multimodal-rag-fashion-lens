
import ollama 
from datasets import load_dataset
from core.config_loader import ConfigLoader
from core.vector_store import VectorStore

class Ingestion:
    def __init__(self, config: ConfigLoader):
        # Load configuration
        self.config = config 
        self.vector_store = VectorStore(config)
    
        # Load dataset
    def load_dataset(self):
        dataset_name = self.config.dataset_name
        self.dataset = load_dataset(dataset_name, split='train')

        #Embed items and store in ChromaDB
    def embed_items(self, items):
        embedding_model = self.config.embedding_model
        # Ensure the embedding model is loaded
    
        for i, item in enumerate(items):
            if i % 100 == 0:
                print(f"Embedding item {i}/{len(items)}...")
            
            # Get text
            text = f"{item['gender']} {item['masterCategory']} {item['subCategory']} {item['articleType']} {item['baseColour']} {item['season']} {item['usage']}"
                        
            # Generate embedding using Ollama
            response = ollama.embeddings(
                model=embedding_model,
                prompt=text
            )
            vector=response['embedding']
        
            # Store in ChromaDB
            self.vector_store.add_items(
                ids=[str(item['id'])],
                documents=[text],
                embeddings=[vector],
                metadatas=[{"product_name": item['productDisplayName']}]
            )

    def run(self, limit=None):
        # Load dataset
        self.load_dataset()
        items=self.dataset
        if limit:
            items=self.dataset.select(range(limit))
        
        # Embed items and store in ChromaDB
        self.embed_items(items)
        print("Ingestion completed successfully.")
 
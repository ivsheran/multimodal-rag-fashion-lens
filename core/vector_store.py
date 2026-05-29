import chromadb

class VectorStore:
    def __init__(self, config):
        self.client = chromadb.PersistentClient(path=config.chroma_path)
        self.collection = self.client.get_or_create_collection(name=config.collection_name)
        

    def add_items(self, ids: list, documents: list, embeddings: list, metadatas: list):
         self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
         )

    def search(self, query_vector,top_k):
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            include=['documents', 'metadatas'])
        return results
    
    def __repr__(self):
        return (f"VectorStore(collection={self.collection.name})")
    
    def clear(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name
    )
        print("Collection cleared.")
    

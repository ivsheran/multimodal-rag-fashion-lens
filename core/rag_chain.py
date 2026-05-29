import ollama

from core.config_loader import ConfigLoader
from core.image_processor import ImageProcessor
from core.vector_store import VectorStore


class RAGChain:
    def __init__(self, vector_store: VectorStore, image_processor: ImageProcessor, config: ConfigLoader):
        self.vector_store = vector_store
        self.image_processor = image_processor
        self.config = config
        prompt_path = 'prompts/rag_prompt.txt'
        self.rag_prompt = self._load_prompt(prompt_path)

    # Load prompt from file
    def _load_prompt(self, prompt_path):
        with open(prompt_path, 'r') as f:
            prompt = f.read()
        return prompt

    # Analyse uploaded image
    def analyse_image(self, image):
        description = self.image_processor.describe_image(image)
        return description

    def retrieve_similar(self, description: str, top_k: int):
        # Retrive matching items from vector store (image + text)
        response =ollama.embeddings(
            model=self.config.embedding_model,
            prompt=description
        )
        vector=response['embedding']
        
        # Find similar items in the vector store based on the description
        results = self.vector_store.search(vector, top_k=top_k)

        # Format retrieved items into a context string for the LLM
        context = ""
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            context += f"- {meta['product_name']}: {doc}\n"
        return context

    def generate_response(self, description, context):
        # Generate response using LLM based on the prompt and retrieved items
        prompt_template = self.rag_prompt
        prompt = (prompt_template
                  .replace("{description}", description)
                  .replace("{context}", context)        
                )
        response = ollama.chat(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Generate a response describing the uploaded image and how it relates to the similar items."}
            ]
        )
        return response['message']['content']
       

    def run(self, image):
        # Analyse image
        description = self.analyse_image(image)
        # Retrieve similar items
        context = self.retrieve_similar(description, top_k=self.config.top_k)
        # Generate response
        response = self.generate_response(description, context)
        return response
    
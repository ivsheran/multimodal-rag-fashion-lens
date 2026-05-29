import os
from core.config_loader import ConfigLoader
from core.image_processor import ImageProcessor
from core.vector_store import VectorStore
from core.ingestion import Ingestion
from core.rag_chain import RAGChain
from layout import create_layout, build_similar_items_html

# Initialise
config = ConfigLoader()
image_processor = ImageProcessor(config)
vector_store = VectorStore(config)
rag_chain = RAGChain(vector_store, image_processor, config)

# Run ingestion if ChromaDB is empty
if vector_store.collection.count() == 0:
    print("ChromaDB is empty — running ingestion...")
    ingestion = Ingestion(config)
    ingestion.run()
    print("Ingestion complete!")

def analyse_fn(image_path):
    # call rag_chain.run()
    response, image_paths, metadatas = rag_chain.run(image_path)
    description = response
    
    # return description, html
    html = build_similar_items_html(image_paths, metadatas)
    return description, html

def clear_fn():
    # return empty values for all three outputs
    return None, "", ""

if __name__ == "__main__":
    demo = create_layout(analyse_fn, clear_fn)
    demo.launch(
        share=config.gradio_share,
        allowed_paths=[os.path.abspath("data/images")]
        )


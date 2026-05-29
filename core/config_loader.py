import os
import yaml
from dotenv import load_dotenv

load_dotenv()
hf_token=os.getenv("HF_TOKEN")


class ConfigLoader:
    def __init__(self, config_path="config.yaml"):
        self.load_from_yaml(config_path)

    def load_from_yaml(self, config_path="config.yaml"):
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            if not config:
                raise ValueError("Configuration file is empty.")
        except FileNotFoundError:
            raise FileNotFoundError("Configuration file not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

        self.vision_model = config['ollama']['vision_model']
        self.embedding_model = config['ollama']['embedding_model']  
        self.llm_model = config['ollama']['llm_model']

        self.ollama_base_url = config['ollama']['base_url']
        self.chroma_path = config['storage']['chroma_path']
        self.collection_name = config['storage']['collection_name']
        self.dataset_name = config['dataset']['name']
        self.top_k = config['search']['top_k']
        self.gradio_title = config['gradio']['title']   
        self.gradio_share = config['gradio']['share']


    
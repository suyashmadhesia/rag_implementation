from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter

class SentenceTransformerEmbeddings:
    def __init__(self, text: str, model_name: str = "all-MiniLM-L6-v2"):
        self._text = text
        self._model = SentenceTransformer(model_name)
        self._chunks = self._create_chunks()

    def _create_chunks(self):
        """Split text into optimal chunks for efficient embedding."""
        text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=100)
        return text_splitter.split_text(self._text)

    def generate_embeddings(self):
        """Generate embeddings for each text chunk."""
        return self._model.encode(self._chunks, batch_size=16, convert_to_tensor=True, normalize_embeddings=True)

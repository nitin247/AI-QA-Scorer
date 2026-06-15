from sentence_transformers import SentenceTransformer, util


class Similarity:
    similarity_score = 0
    
    def __init__(self):
        return

    def get_score(self, text1, text2):
        sentences = [text1, text2]
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        embeddings = model.encode(sentences)
        self.similarity_score = util.cos_sim(embeddings[0], embeddings[1])
        return self.similarity_score


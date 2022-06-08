from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

file = pd.read_csv("Articles.csv")
file = file[file['soup'].notna()]

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(file['soup'])
cosine_sim = cosine_similarity(count_matrix,count_matrix)

file = file.reset_index()
indices = pd.Series(file.index, index=file['title'])

def get_recommendations(contentId):
    idx = indices[contentId]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    article_indices = [i[0] for i in sim_scores]
    return file[['title', 'total_events', 'contentId']].iloc[article_indices].values.tolist()
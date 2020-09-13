import sys
sys.path.insert(0, './recommendation')

from normalization import normalize_corpus
from utils import build_feature_matrix
from bm25 import compute_corpus_term_idfs
from bm25 import compute_bm25_similarity
from semantic_similarity import sentence_similarity
import numpy as np
import pandas as pd
import os


def convert(s): 
  
    # initialization of string to "" 
    str1 = "" 
  
    # using join function join the list s by  
    # separating words by str1 
    return(str1.join(s)) 

def main():
	no_list = 5000
	dataframe = pd.read_csv('./data/final_questions_data.csv', names=['user', 'college', 'category', 'problems', 'problem_link'])

	answers=list(dataframe['problems'][1:no_list])
	answers = answers[1:no_list]

	if os.path.isfile('norm_corpus.csv'):
		pass
		read_df = pd.read_csv('norm_corpus.csv', names=['norm'], index_col=False)
		norm_corpus = read_df['norm'][1:].values.astype('U').tolist()
	else:
		norm_corpus = normalize_corpus(answers, lemmatize=True)
		write_df = pd.DataFrame(norm_corpus)
		write_df.to_csv('norm_corpus.csv', index = False, header = None)
	vectorizer, corpus_features = build_feature_matrix(norm_corpus,feature_type='tfidf')

	doc_lengths = [len(doc.split()) for doc in norm_corpus]   
	avg_dl = np.average(doc_lengths) 
	corpus_term_idfs = compute_corpus_term_idfs(corpus_features, norm_corpus)

	for answer in answers:
		answers=list(dataframe['problems'][1:no_list])

		answers.remove(convert(answer))
		model_answer = convert(answer)
		print (model_answer)
		# normalize answers
		norm_corpus = normalize_corpus(answers, lemmatize=True)

		# normalize model_answer
		norm_model_answer =  normalize_corpus(model_answer, lemmatize=True)            

		# extract features from model_answer
		model_answer_features = vectorizer.transform(norm_model_answer)

		for index, doc in enumerate(model_answer):
			doc_features = model_answer_features[index]
			bm25_scores = compute_bm25_similarity(doc_features,corpus_features,doc_lengths,avg_dl,corpus_term_idfs,k1=1.5, b=0.75)
			semantic_similarity_scores=[]
			for sentence in answers:
				score=(sentence_similarity(sentence,model_answer[0])+sentence_similarity(model_answer[0],sentence))/2
				semantic_similarity_scores.append(score)
			print ('Model Answer',':', doc)
			print ('-'*40 )
			doc_index=0
			sim_scores = []
			for score_tuple in zip(semantic_similarity_scores,bm25_scores):
				sim_score=((score_tuple[0]*10)+score_tuple[1])/2
				sim_scores.append(sim_score)
			#print (sim_scores)
			print(sorted(range(len(sim_score)), key=lambda i: sim_score[i])[-5:])
			break
			print ('Ans num: {} Score: {}\nAnswer: {}'.format(doc_index+1, sim_score, answers[doc_index]))
			print ('-'*40)
			doc_index=doc_index+1
			
		break

if __name__ == "__main__":
	main()
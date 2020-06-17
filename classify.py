import pandas as pd
import json
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF



nlp = spacy.load('en_core_web_sm')
list_data = []
list_data_only_reviews = []
list_data_reviewerid = []
result = []
l = []

for line in open('Automotive_5.json', 'r'):
    list_data.append(json.loads(line))

for item in list_data:
    list_data_only_reviews.append(item['reviewText'])
    list_data_reviewerid.append(item['reviewerID'])
    

# opening the csv file in 'w+' mode 
file = open('review_file.csv', 'w+') 
    
# writing the data into the file 
with file:     
    df = pd.DataFrame(list_data_only_reviews, columns=['Reviews'])
    df.to_csv(file,index=False)

npr = pd.read_csv('review_file.csv')


tfidf = TfidfVectorizer(max_df=0.8,min_df=5,stop_words='english')

dtm = tfidf.fit_transform(npr['Reviews'].values.astype('U'))

nmf_model = NMF(n_components=20,random_state=50)
nmf_model.fit(dtm)

#returns index positions that sort the array
#checking which word in the topic has high probability
for i,topic in enumerate(nmf_model.components_):
    print(f"THE TOP 30 WORDS FOR TOPIC #{i}")
    print([tfidf.get_feature_names()[i] for i in topic.argsort()[-30:] if len(tfidf.get_feature_names()[i]) > 5])
    print('\n')

#probability of a document belonging to a topic
topic_results = nmf_model.transform(dtm)


npr['Topic'] = topic_results.argmax(axis=1)

topic_label = {0:'plastic', 1:'winter batteries', 2:'engines', 3:'liquid', 4:'wind', 5:'shipping', 6:'light',
               7:'quality', 8:'instructions', 9:'worked', 10:'rubber', 11:'cleaning', 12:'pressure', 13:'washing',
               14:'recommendation', 15:'advertise', 16:'bucket', 17:'camp', 18:'brush', 19:'travel'}
npr['Topic Label'] = npr['Topic'].map(topic_label)

npr = npr.assign(Reviews=list_data_reviewerid)

npr.to_csv('classified_output.csv')



import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import bs4 as bs
import urllib.request
import requests
import pickle
from tmdbv3api import TMDb
from tmdbv3api import TV

tmdb = TMDb()
tmdb.api_key = '9d5b8821ec0d8d8a8a2edbede4934247'

filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl', 'rb'))


def create_cosine_similarity():
    df = pd.read_csv('data.csv')
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['combinaiton'])
    similarity = cosine_similarity(count_matrix)
    return df, similarity



def recommendation(ws):
    ws = ws.lower()
    df, similarity = create_cosine_similarity()
    if ws not in df['Series Title'].unique():
        return 'Sorry! Web Series you looking for is not in our database right now. Please check the spelling or try with some other Web Series'
    else:
        index = df.loc[df['Series Title'] == ws].index[0]
        ws_sim_score_list = list(enumerate(similarity[index]))
        ws_sim_score_list = sorted(ws_sim_score_list, key = lambda x:x[1], reverse=True)
        ws_sim_score_list = ws_sim_score_list[1:11]
        recommended_ws = []
        for i in range(len(ws_sim_score_list)):
            indx = ws_sim_score_list[i][0]
            recommended_ws.append(df['Series Title'][indx])
        return recommended_ws
    

def ListOfGenres(genre_json):
    if genre_json:
        genres = []
        genre_str = ", " 
        for i in range(0,len(genre_json)):
            genres.append(genre_json[i]['name'])
        return genre_str.join(genres)
    
    

def date_convert(s):
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December']
    y = s[:4]
    m = int(s[5:-3])
    d = s[8:]
    month_name = MONTHS[m-1]

    result= month_name + ' ' + d + ' '  + y
    return result




def get_suggestions():
    df = pd.read_csv('data.csv')
    return list(df['Series Title'].str.title())


app = Flask(__name__)


@app.route('/')
def home():
    suggestions = get_suggestions()
    return render_template('home.html', suggestions=suggestions)


@app.route('/recommend', methods=['GET'])
def recommend():
    web = str(request.args.get('web'))
    rcmd = recommendation(web)
    tmdb_webseries = TV()
    result = tmdb_webseries.search(web)
    
    web_id = result[0].id
    response = requests.get('http://api.themoviedb.org/3/tv/{}?api_key={}&append_to_response=external_ids'.format(web_id,tmdb.api_key))
    data_json = response.json()
    imdb_id = data_json['external_ids']['imdb_id']
    poster = result[0].poster_path
    img_path = 'https://image.tmdb.org/t/p/original{}'.format(poster)
    genre = ListOfGenres(data_json['genres'])
    
    cast_response = requests.get('https://api.themoviedb.org/3/tv/{}?api_key={}&append_to_response=credits'.format(web_id,tmdb.api_key))
    cast_data = cast_response.json()
    casts = {i:[cast_data['credits']['cast'][i]['name'], cast_data['credits']['cast'][i]['character'], 'https://image.tmdb.org/t/p/original/'+cast_data['credits']['cast'][i]['profile_path']] for i in range(len(cast_data['credits']['cast']))}
    
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ql_3'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})
    reviews_list = []
    reviews_status = []
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            web_review_list = np.array([reviews.string])
            web_vector = vectorizer.transform(web_review_list)
            pred = clf.predict(web_vector)
            reviews_status.append('Good' if pred else 'Bad')
            
    web_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))} 
    vote_count = "{:,}".format(result[0].vote_count)
    rd = date_convert(result[0].first_air_date)
    df = pd.read_csv('data.csv')
    seasons = df[df['Series Title']== web.lower()]['No of Seasons']
    seasons = seasons.iloc[0]
    overview = result[0].overview
    
    poster = []
    for web_title in rcmd:
        list_result = tmdb_webseries.search(web_title)
        web_id = list_result[0].id
        posterr = list_result[0].poster_path
        poster.append('https://image.tmdb.org/t/p/original{}'.format(posterr))
    web_cards = {poster[i]: rcmd[i] for i in range(len(rcmd))}
    

     
    suggestions = get_suggestions()
    
    return render_template('recommend.html', web=web, webtitle=rcmd, cards=web_cards,casts=casts, result=result[0],
                           reviews = web_reviews, img_path=img_path, genre=genre, vote_count=vote_count,
                           release_date=rd, seasons=seasons, overview=overview, t='l', suggestions=suggestions)
    



if __name__ == '__main__':
    app.run()
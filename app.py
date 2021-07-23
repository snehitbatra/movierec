from flask import Flask, request, render_template , jsonify
import json
from flask_mysqldb import MySQL
import os
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Classic@123'
app.config['MYSQL_DB']='flaskapp'
mysql=  MySQL(app)


def rec(movie_name):
    import imdb
    from imdb import IMDb
    movies_db=imdb.IMDb()

    movies=movies_db.search_movie(movie_name)

    #for movi in movies:
        #title=movi['title']
        #year=movi['year']
        #print(title,year)
    id=movies[0].getID()
    mov=movies_db.get_movie(id)
    title=mov['title']
    #year=mov['year']
    rating=mov['rating']
    print(title,rating)
    casting=mov['cast']
    xx=[]
    for i in range(5):
        xx.append(casting[i])

    xx.append(title)
    xx.append(rating)

    casting=xx
    return xx
def results(movie_name):
        import json
        import pandas as pd
        data=pd.read_csv('https://raw.githubusercontent.com/MahnoorJaved98/Movie-Recommendation-System/main/movie_dataset.csv')
        import numpy as np
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        features=['keywords','cast','genres','director']
        for feature in features:
            data[feature]=data[feature].fillna('')
        def combined_features(row):
            return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
        data["combined_features"] = data.apply(combined_features, axis =1)
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(data["combined_features"])

        cosine_sim = cosine_similarity(count_matrix)
        liked=movie_name

        def get(title):
            return data[data.title == title]["index"].values[0]
        x=cosine_sim[get(liked)]
        y=np.argsort(x)[-10:]
        ff=[]
        for i in range(0,10):
            u=data[data.index==y[i]]['original_title'].values

            ff.append(u)
        return ff

def freedom(listo):
    import numpy as np
    rr=np.concatenate((listo[0], listo[1], listo[2],listo[3],listo[4],listo[5],listo[6],listo[7],listo[8],listo[9]))
    rrr=[]
    rrr.append(rr[0])
    rrr.append(rr[1])
    rrr.append(rr[2])
    rrr.append(rr[3])
    rrr.append(rr[4])
    rrr.append(rr[5])
    rrr.append(rr[6])
    rrr.append(rr[7])
    rrr.append(rr[8])
    rrr.append(rr[9])

    return rrr

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])

def my_form_post():
    text = request.form['text']
    tot=rec(text)
    tota=results(tot[5])
    to=freedom(tota)
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO users (movie) VALUES (%s)",[text])
    mysql.connection.commit()
    cur.close()
    return render_template('sne.html',movie=tot,mo=to)
@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    user=cur.execute("SELECT movie,count(movie) from users GROUP BY movie")
    if(user>0):
        userd=cur.fetchall()
        return render_template('kk.html',user=userd)



if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port = port, debug = False)

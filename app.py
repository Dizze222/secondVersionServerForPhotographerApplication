from collections import defaultdict
import flask_sqlalchemy
from sqlalchemy.dialects.sqlite import BLOB
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    idPhotographer = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    like = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<Article %r' % self.id


testTwo = defaultdict(list)


@app.route('/posts', methods=['GET', 'POST'])
def getDataFromCLient():
    array = []
    authorOfComments = {0: ["Denis","Igor"],1:["Maria","Lena"]}

    if request.method == 'GET':
        articles = Article.query.order_by(Article.date).all()
        for i in articles:
            array.append(
                {
                    'idPhotographer': int(i.idPhotographer),
                    'author': str(i.author),
                    'url': str(i.url),
                    'theme': str(i.theme),
                    'like': int(i.like),
                    'comments': i.comments[f'{i.idPhotographer}'],
                    'authorOfComments': authorOfComments[i.idPhotographer]
                }
            )
        try:
            for i in range(len(array) - 1):
                x = array[i]
                for j in range(i + 1, len(array)):
                    y = array[j]
                    if not x or not y:
                        continue
                    if x['idPhotographer'] == y['idPhotographer']:
                        a = x['like'] + y['like']
                        b = x['comments']
                        c = y['comments']
                        if len(c) > len(b):
                            x['comments'] = c
                        if a > 0 or a == 0:
                            x['like'] = a
                        else:
                            print("лайков слишком мало")
                        y.clear()
            array = [x for x in array if x]
        except Exception as error:
            print(error)
        return jsonify(array)
    if request.method == 'POST':
        print("post")
        try:
            idPhotographer = int(request.form['idPhotographer'])
            author = str(request.form['author'])
            url = str(request.form['url'])
            theme = str(request.form['theme'])
            like = int(request.form['like'])
            comments = str(request.form['comments'])
            testTwo[idPhotographer].append(comments)
            article = Article(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                              comments=testTwo)
            db.session.add(article)
            db.session.commit()
        except Exception:
            return "Error"


@app.route('/', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":

        idPhotographer = int(request.form['idPhotographer'])
        author = str(request.form['author'])
        url = str(request.form['url'])
        theme = str(request.form['theme'])
        like = int(request.form['like'])
        comments = request.form['comments']
        testTwo[idPhotographer].append(comments)
        article = Article(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                          comments=testTwo)
        db.session.add(article)
        db.session.commit()
        return redirect('posts')
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)

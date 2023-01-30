from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# подключение базы через конфиг
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


# класс = таблица в бд
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # все записи из бд, отсортированные по полю date
    return render_template("posts.html", articles=articles)
    # передаем в шаблон спиок articles, в шаблоне имеем доступ к списку по ключ слову


@app.route('/posts/<int:id>')  # вставка в ссылку параметра
def post_detail(id):
    article = Article.query.get(id)  # запрос к id записи в бд, режим чтения
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete')  # вставка в ссылку параметра
def post_delete(id):
    article = Article.query.get_or_404(id)  # запрос к id записи, если запись будет не найдена то 404

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.commit()
            return redirect("/posts")  # после создания статьи редирект на страницу с постами
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")  # после создания статьи редирект на страницу с постами
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)

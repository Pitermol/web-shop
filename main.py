from loginform import LoginForm
from add_news import AddNewsForm
from db import DB
from usersmodel import UsersModel
from newsmodel import NewsModel
from registform import RegistForm
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global ind
    form = LoginForm()
    if form.validate_on_submit():
        f = open('admins', encoding="utf-8", mode='r+')
        data = f.read().split('\n')
        ff = open('users', encoding="utf-8", mode='r+')
        data1 = ff.read().split('\n')
        logins = {}
        login = []
        for i in data:
            i = i.split(':')
            logins[str(i[0])] = str(i[1])
            login.append(str(i[0]))
            user_name = str(form.username.data)
            password = str(form.password.data)
            if user_name in login:
                if str(logins[user_name]) == str(password):
                    user_model = UsersModel(db.get_connection())
                    user_model.insert(user_name, password)
                    exists = user_model.exists(user_name, password)
                    if (exists[0]):
                        session['username'] = user_name
                        session['user_id'] = exists[1]
                return redirect("/admin")
            else:
                for i in data1:
                    i = i.split(':')
                    logins[i[0]] = i[1]
                    login.append(i[0])
                    user_name = form.username.data
                    password = form.password.data
                    if user_name in login:
                        if str(logins[user_name]) == str(password):
                            user_model = UsersModel(db.get_connection())
                            user_model.insert(user_name, password)
                            exists = user_model.exists(user_name, password)
                            if (exists[0]):
                                session['username'] = user_name
                                session['user_id'] = exists[1]
                        return redirect("/user")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegistForm()
    if form.validate_on_submit():
        ind = ''
        f = open('users', encoding="utf-8", mode='r+')
        ff = open('admins', encoding="utf-8", mode='r+')
        datauser = f.read()
        dataadmin = ff.read()
        user_name = form.username.data
        password = form.password.data
        repeat = form.repeat.data
        mail = form.mail.data
        code = form.user_admin.data
        user_model = UsersModel(db.get_connection())
        user_model.insert(user_name, password)
        exists = user_model.exists(user_name, password)
        if str(code) == 'sell':
            ind = 'admin'
        else:
            ind = 'user'
        if password != repeat:
            return redirect('/register')
        if ind == 'admin':
            if user_name not in dataadmin:
                ff.write('\n')
                ff.write(user_name)
                ff.write(':')
                ff.write(password)
                ff.write(':')
                ff.write(mail)
            else:
                return redirect('/register')
        else:
            if user_name not in datauser:
                f.write('\n')
                f.write(user_name)
                f.write(':')
                f.write(password)
                f.write(':')
                f.write(mail)
            else:
                return redirect('/register')
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/index")
    return render_template('regist.html', title='Регистрация', form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' not in session:
        return redirect('/login')
    products = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('user.html', username=session['username'], prods=products)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect('/login')
    products = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'], prods=products)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/admin")
    return render_template('add_news.html', title='Добавление новости', form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    print(news_id, 'jj')
    nm.delete(news_id)
    return redirect("/admin")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
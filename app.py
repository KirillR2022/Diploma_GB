from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Person, Category, Note, Rank, Tag, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workbook.db'
app.config['SECRET_KEY'] = 'sdvckhwbevcuewrbvceurhv123e8238c734v'
db.init_app(app)



# Контактная книга
@app.route('/contact_book')
def contact_book():
    persons = Person.query.all()
    return render_template('contact_book/index.html', persons=persons)


@app.route('/contact_book/add', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        details = request.form['details']
        phone = request.form['phone']
        address = request.form['address']
        person = Person(name=name, birthday=birthday, details=details, phone=phone, address=address)
        db.session.add(person)
        db.session.commit()
        return redirect('/contact_book')
    return render_template('contact_book/add.html')


@app.route('/contact_book/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    person = Person.query.get_or_404(id)
    if request.method == 'POST':
        person.argument = request.form['name']
        person.birthday = request.form['birthday']
        person.details = float(request.form['details'])
        person.phone = float(request.form['phone'])
        person.address = request.form['address']
        db.session.commit()
        return redirect('/contact_book')
    return render_template('contact_book/edit.html', person=person)


@app.route('/contact_book/delete/<int:id>', methods=['POST'])
def delete_person(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect('/contact_book')


# Заметки
@app.route('/notes')
def notes():
    notes = Note.query.all()
    return render_template('notes/index.html', notes=notes)


@app.route('/notes/note/<int:note_id>')
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('notes/note.html', note=note)


@app.route('/notes/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('notes/rank.html', category=category)


@app.route('/notes/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        note = Note(title=title, content=content, category_id=category_id)
        db.session.add(note)
        db.session.commit()
        flash('Заметка успешно добавлена!')
        return redirect('/notes')
    categories = Category.query.all()
    return render_template('notes/add.html', categories=categories)


@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.category_id = request.form['category']
        db.session.commit()
        flash('Заметка успешно обновлена!')
        return redirect('/notes')
    categories = Category.query.all()
    return render_template('notes/edit.html', note=note, categories=categories)


@app.route('/notes/delete/<int:note_id>', methods=['GET', 'POST'])
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        db.session.delete(note)
        db.session.commit()
        flash('Заметка удалена')
        return redirect('/notes')
    return render_template('notes/delete.html', note=note)


# Ежедневник
@app.route('/')
@app.route('/index')
@app.route('/daily_planner')
def daily_planner():
    posts = Post.newest_first().all()
    return render_template('daily_planner/index.html', posts=posts)


@app.route('/daily_planner/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('daily_planner/post.html', post=post)


@app.route('/daily_planner/rank/<int:rank_id>')
def rank(rank_id):
    rank = Rank.query.get_or_404(rank_id)
    posts = Post.query.filter_by(rank_id=rank_id).order_by(Post.date.desc()).all()
    return render_template('daily_planner/rank.html', rank=rank, posts=posts)


@app.route('/daily_planner/tag/<int:tag_id>')
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.filter(Post.tags.any(id=tag_id)).order_by(Post.date.desc()).all()
    return render_template('daily_planner/tag.html', tag=tag, posts=posts)


@app.route('/daily_planner/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        rank_id = request.form['rank']
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        post = Post(title=title, content=content, rank_id=rank_id)
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Запись создана!', 'success')
        return redirect('/daily_planner')
    ranks = Rank.query.all()
    tags = Tag.query.all()
    return render_template('daily_planner/new_post.html', ranks=ranks, tags=tags)


@app.route('/daily_planner/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.rank_id = request.form['rank']
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        post.tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)
        db.session.commit()
        flash('Запись обновлена!', 'success')
        return redirect('/daily_planner')
    ranks = Rank.query.all()
    tags = Tag.query.all()
    return render_template('daily_planner/edit_post.html', post=post, ranks=ranks, tags=tags)


@app.route('/daily_planner/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Запись удалена!', 'success')
    return redirect('/daily_planner')


if __name__ == '__main__':
    app.run(debug=True)

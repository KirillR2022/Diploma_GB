from flask import Flask
from models import Person, Note, Category, Rank, Tag, Post, db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workbook.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Заметки
        category1 = Category(name='Работа')
        category2 = Category(name='Хобби')
        category3 = Category(name='Инвестиции')
        category4 = Category(name='Рецепты')
        category5 = Category(name='Авто')
        category6 = Category(name='Программирование')

        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.add(category4)
        db.session.add(category5)
        db.session.add(category6)

        # Ежедневник

        rank1 = Rank(name='Итог дня')
        rank2 = Rank(name='Анализ состояния')
        rank3 = Rank(name='Достижения')


        db.session.add(rank1)
        db.session.add(rank2)
        db.session.add(rank3)
        db.session.commit()

        tag1 = Tag(name='Успехи')
        tag2 = Tag(name='Неприятность')
        tag3 = Tag(name='Эмоции')
        tag4 = Tag(name='Вопросы')
        tag5 = Tag(name='Семья')
        tag6 = Tag(name='Учеба')
        tag7 = Tag(name='Друзья')

        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.commit()

        post1 = Post(title='Наконец-то я закончил диплом',
                     content='Спустя 3 месяца крополтивой работы, я наконец-то закончил писать диплом. Мой результат превзошел все ожидания',
                     date=datetime.now(), rank_id=rank3.id)
        post2 = Post(title='Неприятность на дороге',
                     content='Выезжая из Владимира я почувствовал, что задняя ось ведет. Не думал, что буду опаздывать на работу из-за замерзших колодок',
                     date=datetime.now(), rank_id=rank1.id)
        post3 = Post(title='На следующую неделю записался на диспансеризацию',
                     content='По совету моего врача, мне необходимо проверить свое состояние, пройдя общий список врачей, а также УЗИ',
                     date=datetime.now(), rank_id=rank3.id)

        # Добавляем теги к постам
        post1.tags.append(tag1)
        post2.tags.append(tag2)
        post3.tags.append(tag3)

        # Сохраняем посты в БД
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)

        db.session.commit()
        # print('Созданы категории заметок - Работа, Хобби и Инвестиции')
    print('Создана база данных')

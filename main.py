import sqlite3
from itertools import combinations


con = sqlite3.connect("netflix.sqlite")
cur = con.cursor()


def normalize():
    columns = ['show_id', 'director', 'country', 'date_added', 'release_year', 'rating', 'listed_in', 'description']
    for column in columns:
        cur.execute(f'ALTER TABLE `netflix_titles` DROP COLUMN {column}')


def longest_movie():
    """
    Функция ищет и возвращает самый продолжительный фильм
    """
    res = cur.execute(f"""SELECT title, duration FROM `netflix_titles` WHERE `type` = 'Movie'""").fetchall()
    res = list(map(lambda x: (x[0], int(x[1].split(' ')[0])), res))
    res = sorted(res, key=lambda x: x[1])
    return res[-1]


def longest_tv_show():
    """
    Функция ищет и возвращает самые продолжительные сериалы
    """
    res = cur.execute(f"""SELECT title, duration FROM `netflix_titles` WHERE `type` = 'TV Show'""")
    res = res.fetchall()
    res = list(map(lambda x: (x[0], int(x[1].split(' ')[0])), res))
    res = sorted(res, key=lambda x: x[1])
    return res[-1], res[-2]


def most_popular_actor():
    """
    Функция ищет и возвращает актёра, который чаще всего снимался в фильмах и сериалах
    """
    res = cur.execute(f"""SELECT `cast` FROM `netflix_titles` WHERE `cast` != ''""").fetchall()
    actors = {}
    for casts in res:
        acts = casts[0].split(',')
        for act in acts:
            act = act.strip()
            if act in actors:
                actors[act] += 1
            else:
                actors[act] = 1
    res = sorted(actors.items(), key=lambda x: x[1])
    return res[-1]


def most_popular_couple():
    """
    Функция ищет и возвращает пару, которая чаще всего снималась друг с другом
    """
    res = cur.execute(f"""SELECT `cast` FROM `netflix_titles` WHERE `cast` != ''""").fetchall()
    _pairs = {}
    for casts in res:
        casts = casts[0].split(',')
        casts = [i.strip() for i in casts]
        pairs = combinations(casts, 2)
        for pair in pairs:
            pair = sorted(pair)
            key = pair[0] + '+' + pair[1]
            if key in _pairs:
                _pairs[key] += 1
            else:
                _pairs[key] = 1
    res = sorted(_pairs.items(), key=lambda x: x[1])
    pair = res[-1]
    human1, human2 = pair[0].split('+')
    return human1, human2, pair[1]


if __name__ == '__main__':
    # normalize()

    title, minutes = longest_movie()
    print(f"Самый продолжительный фильм «{title}» длится {minutes} минут")

    (title, series), (title2, series2) = longest_tv_show()
    print(f"Самые популярные продолжительные сериалы «{title}» и «{title2}» идут {series} сезонов")

    actor, films = most_popular_actor()
    print(f"Самый популярный актёр ― {actor} ― снялся в {films} фильмах")

    human1, human2, collaborations = most_popular_couple()
    print(f"Наиболее часто работающая друг с другом пара актёров {human1} и {human2} снялись вместе {collaborations} раз")

import os#,sys#, datetime
import sqlite3 as sql
from time import time
from typing import List, Tuple
from pystardict import Dictionary
from lyp_util import load_or_execute
from config import IN_FILE_PATH, DB_FILE_PATH, DB_RESULT_PATH

start_time = time()

db_word = None
db_result = None
curs_word = None
curs_results = None
e_r_dict = None

#@dataclass
class User:
    idx:int
    name:str
    lw:int


def init_dbs():
    global curs_word, curs_results
    global db_word, db_result

    db_word = sql.connect(DB_FILE_PATH, timeout=1)
    curs_word = db_word.cursor()

    db_result = sql.connect(DB_RESULT_PATH, timeout=1)
    curs_results = db_result.cursor()

def finish():
    db_word.close()
    db_result.close()

def init_dicts():
    # os.path.join(os.path.dirname())
    dicts_dir = r"D:\_Data\Dict\StarDict"
    global e_r_dict
    e_r_dict = Dictionary(os.path.join(dicts_dir, 'stardict-quick_eng-rus-2.4.2',
                                          'quick_english-russian'))
    # quick_ru2en = Dictionary(os.path.join(dicts_dir, 'stardict-quick_rus-eng-2.4.2',
    #                                       'quick_russian-english'))
    # apresyan = Dictionary(os.path.join(dicts_dir, 'Apresyan',
    #                                    'Apresyan (En-Ru)'))

    # d_en = Dictionary(os.path.join(dicts_dir, 'Cambridge Advanced Learners',
    #                                 'Cambridge Advanced Learners Dictionary 3th Ed'))

    # d_en = Dictionary(os.path.join(dicts_dir, 'Korolev',
    #                                'comn_dictd03_korolew_en-ru'))

    # d_en = Dictionary(os.path.join(dicts_dir, 'Unk',
    #                                 'eng_rus_full'))

    # d_en2 = Dictionary(os.path.join(dicts_dir, 'Lingvistika_utf8',
    #                                'eng_rus_lingvistika_98_du_v01'))

def load_word_db():
    #print('1: load_word_db')
    with sql.connect(DB_FILE_PATH, timeout=1) as conn:
        cur_word = conn.cursor()
        # cur.execute("SELECT id from Word WHERE word=?", (lemma,))
        # data = cur.fetchall()
        # if data:
        #     cur.execute("INSERT INTO Word (word) VALUES (?);", (lemma,))
        #     w_id = cur.lastrowid
        # else:
        #     w_id = data[0][0]

def load_results():
    # print('2: load_results')
    curs_results.execute("SELECT name, last_word from Users WHERE id=?", (1,))
    data = curs_results.fetchone()
    # print(data[0], data[1])

def select_next(i:int):
    # print('3: select_next')
    #get word
    curs_word.execute("SELECT * FROM lemmas WHERE  lemmas.rank == ? ;", (i,))
    data = curs_word.fetchone()
    word = data[1]
    try:
        trans = e_r_dict[word]
    except KeyError:
        trans = '~'
    print(f'{data[2]} {word} {trans}')


if __name__ == '__main__':
    # demo()
    # load_word_db()
    init_dbs()
    init_dicts()
    load_results()
    select_next(9)
    # print('\n---')
    # print('4: show_translated')
    # print('5: check')
    # print('6: save_results')
    # print('7: goto <3>')
    finish()
    print(f'Time: {time() - start_time}')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3


def get_location(location_idx):
    locations = {
        1: '강원도', 2: '경기도', 3: '광주시', 4: '대구시', 5: '대전시',
        6: '부산시', 7: '서울시', 8: '세종시', 9: '울산시',
        10: '인천시', 11: '제주도', 12: '경상남도', 13: '경상북도',
        14: '전라남도', 15: '전라북도', 16: '충청남도', 17: '충청북도',
    }
    print(locations[location_idx])
    # TODO: 지역별 위도가 몇분 차이나므로 그 부분을 계산 할지 확인


def get_gender(gender_idx):
    gender = {
        1: '남자', 2: '여자'
    }
    print(gender[gender_idx])
    # TODO: 남녀 이름 구별


def get_birth_order(birth_order_idx):
    birth_order = {
        1: '첫째', 2: '둘째, 이후'
    }
    print(birth_order[birth_order_idx])
    # TODO: 불용한자 확인


def get_lastname(info):
    conn = sqlite3.connect('naming_korean.db')
    query = 'SELECT * FROM last_name where id=%d' % (info)
    c = conn.cursor()
    c.execute(query)
    row = c.fetchone()
    print(row)
    conn.close()
    return row


def get_new_korean_name(gender, birth_order,
                        location, last_name, birth_datetime):
    print('---------------------')
    print(location)
    print(gender)
    print(birth_order)
    print(birth_datetime)
    print(last_name)
    print('---------------------')
    get_location(location)
    get_gender(gender)
    get_birth_order(birth_order)
    get_lastname(last_name)
    print('---------------------')

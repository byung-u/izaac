#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from time import time
from random import randrange

# /usr/local/lib/python3.6/site-packages/hangul_utils
from hangul_utils import hangul_len, split_syllable_char
from block_list import BLOCK_LIST
from words_list import WORDS_LIST

SHINGANG = 1
SHINYACK = 0

# DBG
LAST_NAME_LIST = ['丁', '丕', '丘', '主', '乃', '于', '京', '仇', '付', '任', '伊', '伍', '余', '侯', '倉', '候', '傅', '元', '全', '兪', '公', '具', '初', '判', '剛', '劉', '包', '化', '千', '卓', '南', '卜', '卞', '占', '印', '叢', '史', '吉', '后', '吳', '呂', '周', '咸', '唐', '喬', '單', '嚴', '國', '堅', '增', '墨', '夏', '多', '夜', '大', '天', '太', '夫', '奇', '奈', '奉', '姚', '姜', '孔', '孟', '孫', '安', '宋', '宗', '宣', '寶', '尙', '尹', '山', '崔', '左', '平', '康', '庾', '廉', '延', '弓', '张', '張', '强', '弼', '彈', '彬', '彭', '影', '徐', '愼', '慈', '慶', '成', '戰', '房', '扈', '承', '文', '斤', '方', '施', '昇', '昌', '明', '昔', '星', '晋', '景', '智', '曲', '曺', '曾', '朱', '朴', '杉', '李', '杜', '杨', '松', '林', '柳', '柴', '桂', '梁', '梅', '森', '楊', '楔', '楚', '榮', '樊', '橋', '權', '欒', '武', '段', '殷', '毛', '水', '氷', '江', '池', '沈', '沙', '河', '洙', '洪', '浪', '海', '淳', '湯', '溫', '滕', '漢', '潘', '燕', '片', '牟', '玄', '玉', '王', '班', '琴', '甄', '甘', '田', '申', '畢', '異', '白', '皮', '盧', '眞', '睦', '石', '禹', '秋', '秦', '程', '章', '箕', '管', '簡', '米', '罗', '羅', '耿', '胡', '臧', '舍', '舜', '艾', '芮', '芸', '苑', '苗', '范', '荀', '莊', '菊', '萬', '葉', '葉', '葛', '董', '蔡', '蔣', '薛', '蘇', '衛', '表', '袁', '裵', '解', '許', '諸', '謝', '譚', '谷', '賀', '賈', '賓', '趙', '路', '車', '辛', '連', '道', '邊', '邕', '邢', '邦', '邱', '邵', '郝', '郭', '都', '鄒', '鄧', '鄭', '采', '釋', '金', '錢', '鍾', '鎬', '閔', '閻', '關', '阮', '阿', '陈', '陰', '陳', '陶', '陸', '隋', '雍', '雲', '雷', '鞠', '韋', '韓', '順', '頓', '顧', '馬', '馮', '高', '魏', '魚', '魯', '鳳', '鴌', '麻', '黃', '黎', '齊', '龍', '龐', ]


def get_last_name_info(conn, hanja):
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja where hanja="%s"' % hanja
    s.execute(query)
    row = s.fetchone()
    last_name = list(row)
    if last_name[1] == '리':
        last_name[1] = '이'
    elif last_name[1] == '로':
        last_name[1] = '노'
    elif last_name[1] == '금':
        last_name[1] = '김'
    elif last_name[1] == '림':
        last_name[1] = '임'

    return last_name


# 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
# 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
def check_five_type(name_type):
    # http://sajuplus.tistory.com/235
    if name_type == '木木水':  # 木
        return True
    elif name_type == '木木火':
        return True
    elif name_type == '木水木':
        return True
    elif name_type == '木水水':
        return True
    elif name_type == '木火木':
        return True
    elif name_type == '木火火':
        return True
    elif name_type == '木火土':
        return True
    elif name_type == '木水金':
        return True
    elif name_type == '木土火':
        return True
    elif name_type == '木火水':
        return True
    elif name_type == '木水火':
        return True
    elif name_type == '火木木':  # 火
        return True
    elif name_type == '火木水':
        return True
    elif name_type == '火木火':
        return True
    elif name_type == '火火木':
        return True
    elif name_type == '火火土':
        return True
    elif name_type == '火土金':
        return True
    elif name_type == '火土火':
        return True
    elif name_type == '火土土':
        return True
    elif name_type == '火金土':
        return True
    elif name_type == '火水木':
        return True
    elif name_type == '火木土':
        return True
    elif name_type == '土金金':  # 土
        return True
    elif name_type == '土金土':
        return True
    elif name_type == '土金水':
        return True
    elif name_type == '土火木':
        return True
    elif name_type == '土火火':
        return True
    elif name_type == '土火土':
        return True
    elif name_type == '土土金':
        return True
    elif name_type == '土土火':
        return True
    elif name_type == '土水金':
        return True
    elif name_type == '土金火':
        return True
    elif name_type == '土木火':
        return True
    elif name_type == '土火金':
        return True
    elif name_type == '土土土':
        return True
    elif name_type == '金金水':  # 金
        return True
    elif name_type == '金金土':
        return True
    elif name_type == '金水金':
        return True
    elif name_type == '金水木':
        return True
    elif name_type == '金水水':
        return True
    elif name_type == '金土金':
        return True
    elif name_type == '金土火':
        return True
    elif name_type == '金土土':
        return True
    elif name_type == '金木水':
        return True
    elif name_type == '金水土':
        return True
    elif name_type == '金火土':
        return True
    elif name_type == '金土水':
        return True
    elif name_type == '水金金':  # 水
        return True
    elif name_type == '水金水':
        return True
    elif name_type == '水金土':
        return True
    elif name_type == '水木木':
        return True
    elif name_type == '水木水':
        return True
    elif name_type == '水木火':
        return True
    elif name_type == '水水金':
        return True
    elif name_type == '水水木':
        return True
    elif name_type == '水火木':
        return True
    elif name_type == '水木金':
        return True
    elif name_type == '水土金':
        return True
    elif name_type == '水金木':
        return True
    elif name_type == '水水水':
        return True
    else:  # not in  水火土金木 rule
        return False


def check_81_suri(conn, total_strokes):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%s' % total_strokes
    for row in s.execute(query):
        if row[0].endswith('吉') is False:  # not 吉
            return False
    return True


def get_siju(iljin, hour):
    siju = [
        ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥"],
        ["丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥"],
        ["戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥"],
        ["庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥"],
        ["壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"],
    ]

    if iljin == '甲' or iljin == '己':
        x = 0
    elif iljin == '乙' or iljin == '庚':
        x = 1
    elif iljin == '丙' or iljin == '辛':
        x = 2
    elif iljin == '丁' or iljin == '壬':
        x = 3
    elif iljin == '戊' or iljin == '癸':
        x = 4
    else:
        print('[ERR] invalid iljin: ', iljin)
        return None

    if 23 <= hour or hour < 1:
        y = 0
    elif 1 <= hour < 3:
        y = 1
    elif 3 <= hour < 5:
        y = 2
    elif 5 <= hour < 7:
        y = 3
    elif 7 <= hour < 9:
        y = 4
    elif 9 <= hour < 11:
        y = 5
    elif 11 <= hour < 13:
        y = 6
    elif 13 <= hour < 15:
        y = 7
    elif 15 <= hour < 17:
        y = 8
    elif 17 <= hour < 19:
        y = 9
    elif 19 <= hour < 21:
        y = 10
    elif 21 <= hour < 23:
        y = 11
    else:
        print('[ERR] invalid hour: ', hour)
        return None
    return (siju[x][y])


def get_secha_wolgeon_iljin(conn, year, month, day):
    s = conn.cursor()
    query = '''
    SELECT lun_secha, lun_wolgeon, lun_iljin
    FROM gregorian_calendar
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    return row[0], row[1], row[2]


def get_h10gan_5types(h10gan):
    if h10gan == '甲' or h10gan == '乙':
        return '木'
    elif h10gan == '丙' or h10gan == '丁':
        return '火'
    elif h10gan == '戊' or h10gan == '己':
        return '土'
    elif h10gan == '庚' or h10gan == '辛':
        return '金'
    elif h10gan == '壬' or h10gan == '癸':
        return '水'
    else:
        return None


def get_h12ji_5types(h12ji):
    if h12ji == '子' or h12ji == '亥':
        return '水'
    elif h12ji == '寅' or h12ji == '卯':
        return '木'
    elif h12ji == '巳' or h12ji == '午':
        return '火'
    elif h12ji == '辰' or h12ji == '戌' or h12ji == '丑' or h12ji == '未':
        return '土'
    elif h12ji == '申' or h12ji == '酉':
        return '金'
    else:
        return None


def get_5types(h10gan, h12ji):
    res_h10gan = get_h10gan_5types(h10gan)
    if res_h10gan is None:
        return None
    res_h12ji = get_h12ji_5types(h12ji)
    if res_h12ji is None:
        return None

    return '%s%s' % (res_h10gan, res_h12ji)


def get_energy_saju(energy):
    return max(energy, key=energy.get)
    # last_two_weak = (sorted(energy.items(), key=lambda x: x[1])[:2])
    # return last_two_weak, max(energy, key=energy.get)


def count_5hang(siju_type, iljin_type, wolgeon_type, secha_type):
    energy = {
            '木': 0,
            '火': 0,
            '土': 0,
            '金': 0,
            '水': 0,
    }
    energy[siju_type[0]] += 1
    energy[siju_type[1]] += 1
    energy[iljin_type[0]] += 1
    energy[iljin_type[1]] += 1
    energy[wolgeon_type[0]] += 1
    energy[wolgeon_type[1]] += 1
    energy[secha_type[0]] += 1
    energy[secha_type[1]] += 1
    return energy


# 木火土金水
def strong_ilgan(ilgan_type):
    if ilgan_type == "木":
        return "火"
    elif ilgan_type == "火":
        return "土"
    elif ilgan_type == "土":
        return "金"
    elif ilgan_type == "金":
        return "水"
    elif ilgan_type == "水":
        return "木"
    else:
        return False


def weak_ilgan(ilgan_type):
    if ilgan_type == "土":
        return "木"
    elif ilgan_type == "木":
        return "金"
    elif ilgan_type == "金":
        return "火"
    elif ilgan_type == "火":
        return "水"
    elif ilgan_type == "水":
        return "土"
    else:
        return False


def check_ilgi_ilgan(ilgi_type, ilgan_type):
    # 일지가 일간을 지탱해줘야하기 때문에 일지가 일간을 강하게 해주는지 확인
    if ilgan_type == "木" and ilgi_type == "火":
        return True
    elif ilgan_type == "火" and ilgi_type == "土":
        return True
    elif ilgan_type == "土" and ilgi_type == "金":
        return True
    elif ilgan_type == "金" and ilgi_type == "水":
        return True
    elif ilgan_type == "水" and ilgi_type == "木":
        return True
    else:
        return False


def check_shin(iljin, iljin_type, energy):
    # 날씨가 추움, 더움, 건조, 습함에 대한 정확한 날짜 기준이 없으므로 미사용
    # 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
    # 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
    ilgan_type = iljin_type[0]

    # 일간을 강하게하거나 약하게 하는 오행을 확인해서 처리
    s = strong_ilgan(ilgan_type)
    w = weak_ilgan(ilgan_type)
    if energy[s] > 3:
        return SHINGANG  # 1
    elif energy[s] > energy[w]:
        return SHINGANG  # 1
    elif energy[s] < energy[w]:
        return SHINYACK  # 0

    # 일지를 강하게하거나 약하게 하는 오행을 확인해서 처리
    ilgi_type = iljin_type[1]
    s = strong_ilgan(ilgi_type)
    w = weak_ilgan(ilgi_type)
    if energy[s] > energy[w]:
        return SHINGANG  # 1
    elif energy[s] < energy[w]:
        return SHINYACK  # 0

    # 일지가 일간을 강하게 하는 오행인가?
    if check_ilgi_ilgan(ilgi_type, ilgan_type) is True:
        return SHINGANG  # 1
    else:
        return SHINYACK  # 0


def get_strong_ilgan_type(ilgan_type):
    return strong_ilgan(ilgan_type)


def get_weak_ilgan_type(ilgan_type):
    return weak_ilgan(ilgan_type)


def support_health(weak):
    if weak == "木":
        return "水"
    elif weak == "火":
        return "木"
    elif weak == "土":
        return "火"
    elif weak == "金":
        return "土"
    elif weak == "水":
        return "金"
    else:
        return None, None


def array_remove_duplicates(l):
    return list(set(l))


def get_saju(conn, birth):
    support_type = []

    year = birth[0:4]
    month = birth[4:6]
    day = birth[6:8]
    hour = birth[8:10]
    secha, wolgeon, iljin = get_secha_wolgeon_iljin(conn, year, month, day)
    siju = get_siju(iljin[0], int(hour))  # siju : hour

    siju_type = get_5types(siju[0], siju[1])
    if siju_type is None:
        return None
    iljin_type = get_5types(iljin[0], iljin[1])
    if iljin_type is None:
        return None
    wolgeon_type = get_5types(wolgeon[0], wolgeon[1])
    if wolgeon_type is None:
        return None
    secha_type = get_5types(secha[0], secha[1])
    if secha_type is None:
        return None
    print('[DBG] -----------')
    print('[DBG] 시 일 월 년')
    print('[DBG] -----------')
    print('[D간]', siju[0], iljin[0], wolgeon[0], secha[0])
    print('[D지]', siju[1], iljin[1], wolgeon[1], secha[1])
    print('[DBG] -----------')
    print('[DBG]', siju_type[0], iljin_type[0], wolgeon_type[0], secha_type[0])
    print('[DBG]', siju_type[1], iljin_type[1], wolgeon_type[1], secha_type[1])
    print('[DBG] -----------')

    energy = count_5hang(siju_type, iljin_type, wolgeon_type, secha_type)
    # 신강 or 신약
    shin = check_shin(iljin, iljin_type, energy)
    if shin == SHINGANG:
        # 일간을 약하게
        result_shin = get_weak_ilgan_type(iljin_type[0])
        print('신강 -> 약하게', result_shin)
    else:  # SHINYACK
        # 일간을 강하게
        result_shin = get_strong_ilgan_type(iljin_type[0])
        print('신약 -> 강하게', result_shin)

    # 1. 신약, 신강에 따른 보충
    support_type.append(result_shin)

    # 2-1. 기운이 없는 것을 보충
    # 2-2. 약한 기운에 따라 건강을 보충
    weak_type = sorted(energy.items(), key=lambda x: x[1])

    sh = support_health(weak_type[0][0])

    if weak_type[0][0] == result_shin and weak_type[0][1] == 0:
        # 기운이 없는 것과, 신강/신약의 결과가 같은 경우
        if sh is not None:
            support_type.append(sh)
        else:
            support_type.append(weak_type[0][0])
    else:
        # 기운이 없는 것과, 신강/신약의 결과가 다른 경우
        if weak_type[0][1] == 0:
            support_type.append(weak_type[0][0])
        else:
            if sh is not None:
                support_type.append(sh)
            else:
                support_type.append(weak_type[0][0])

    strong = get_energy_saju(energy)
    # print(weaks[0][0], weaks[1][0], strong)
    saju = {
            'year': year, 'month': month, 'strong': strong,
            'support_type': support_type,
            'siju': siju, 'siju_type': siju_type,
            'iljin': iljin, 'iljin_type': iljin_type,
            'wolgeon': wolgeon, 'wolgeon_type': wolgeon_type,
            'secha': secha, 'secha_type': secha_type,
    }
    return saju


def check_total_stroke(conn, n1, n2, n3):
    t1 = get_total_strokes(n1, n3, None)
    if t1 == 0:
        return False
    if check_81_suri(conn, t1) is False:  # (홍) 길 (동)
        return False

    t2 = get_total_strokes(n2, n3, None)
    if t2 == 0:
        return False
    if check_81_suri(conn, t2) is False:  # 홍 (길+동)
        return False

    t3 = get_total_strokes(n1, n2, n3)
    if t3 == 0:
        return False
    if check_81_suri(conn, t3) is False:  # (홍+길+동)
        return False

    return True


def get_hangul_len(s):
    hlen = 0
    for i in range(len(s)):
        hlen += hangul_len(s[i])
    return hlen


def check_positive_negative(conn, n1, n2, n3):
    # Hangul
    s1 = hangul_len(n1[1])
    s2 = hangul_len(n2[1])
    s3 = hangul_len(n3[1])
    if s1 % 2 == 0 and s2 % 2 == 0 and s3 % 2 == 0:
        return False
    if s1 % 2 == 1 and s2 % 2 == 1 and s3 % 2 == 1:
        return False
    return True


def check_two_words_hard_pronounce(n1, n2):

    s1 = split_syllable_char(n1)
    s2 = split_syllable_char(n2)

    if len(s1) == 3:
        if s1[2] == 'ㄹ' and s2[0] == 'ㅇ':  # 갈이무
            return False
        elif s1[2] == 'ㅁ' and s2[0] == 'ㅇ':  # 남유현
            return False
        elif s1[2] == 'ㄹ' and s2[0] == 'ㄴ':  # 갈나성
            return False
    if len(s1) == 3 and len(s2) == 3:
        if s1[1] == 'ㅕ' and s1[2] == 'ㅇ' and s2[1] == 'ㅡ' and s2[2] == 'ㅇ':  # 경흥원
            return False
        elif s1[1] == 'ㅏ' and s1[2] == 'ㅇ' and s2[1] == 'ㅏ' and s2[2] == 'ㅇ':  # 강항준
            return False
        elif s1[1] == 'ㅏ' and s1[2] == 'ㅇ' and s2[1] == 'ㅑ' and s2[2] == 'ㅇ':  # 강향준
            return False
    return True


def check_all_name_hard_pronounce(n1, n2, n3):
    s1 = split_syllable_char(n1[1])
    s2 = split_syllable_char(n2[1])
    s3 = split_syllable_char(n3[1])

    if (s1[0] == s2[0] == s3[0]):  # 김구관
        return False
    elif s2[0] == s3[0]:  # 신류려
            return False

    # if (s2[1] == 'ㅐ'):  # 김해선 -> 김혜선  신애라
    #    return False
    if (s3[1] == 'ㅔ'):  # 김지에 -> 김지애
        return False

    if (s2[0] == s3[0]):  # 이름의 자음이 같은 경우에 모음 확인
        if (s2[1] == 'ㅜ' and s3[1] == 'ㅜ'):  # 최준주
            return False
        elif (s2[1] == 'ㅜ' and s3[1] == 'ㅠ'):  # 김주쥬
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅗ'):  # 박곤고
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅛ'):  # 박포표
            return False

    if (s2[1] == 'ㅖ' and s3[1] == 'ㅖ'):  # 이계혜
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅐ'):  # 이혜애
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅔ'):  # 이혜에
            return False

    if len(s2) == 3 and len(s3) > 1:
        if s2[2] == s3[0]:  # 김열루
            return False

    if len(s2) == 3 and len(s3) == 3:
        if (s2[1] == 'ㅕ' and s2[2] == 'ㄴ' and s3[1] == 'ㅕ' and s3[2] == 'ㄴ'):  # 최현련
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅁ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최겸경
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최영경
            return False
        elif (s2[1] == 'ㅑ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅁ'):  # 최양념
            return False
        elif (s2[1] == 'ㅑ' and s2[2] == 'ㅇ' and s3[1] == 'ㅑ' and s3[2] == 'ㅇ'):  # 최양량
            return False
        elif (s2[2] == 'ㄱ' and s3[2] == 'ㄱ'):  # 이혁탁
            return False
        elif (s2[2] == 'ㄴ' and s3[2] == 'ㄴ'):  # 이완린
            return False
        #elif s2[1] == 'ㅜ' and s2[2] == 'ㅇ' and s3[1] == 'ㅡ' and s3[2] == 'ㅇ':  # 상중승
        #    return False
        #elif s2[1] == 'ㅡ' and s2[2] == 'ㅇ' and s3[1] == 'ㅜ' and s3[2] == 'ㅇ':  # 상승중
        #    return False
    elif len(s2) == 3 and len(s3) == 2:
        if (s2[2] == 'ㄹ' and s3[1] == 'ㅖ'):  # 김설혜
            return False

    return True


def support_weak_energy(middle_type, saju):
    if saju['weak1'] == middle_type:
        # print('[1] ', saju['weak1'], middle_type)
        return True
    elif saju['weak2'] == middle_type:
        # print('[2] ', saju['weak2'], middle_type)
        return True
    else:
        return False


def get_name_list(conn, n1, n2, saju):
    name_list = []
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,five_type
    FROM naming_hanja
    WHERE is_naming_hanja=1 AND reading
    NOT IN ('만', '병', '백', '장', '춘', '최', '충', '창', '치', '참', '천',
    '택', '탁', '태', '외', '사', '매', '읍', '소', '종', '순', '요', '자',
    '경', '옥')
    """
    for n3 in s.execute(query):
        if n1[0] == n3[0] or n2[0] == n3[0]:  # 김주김, 김소소
            continue

        n2n3 = '%s%s' % (n2[1], n3[1])
        if check_name(n2n3) is False:
            continue

        if check_positive_negative(conn, n1, n2, n3) is False:
            continue
        # check positive negative hanja strokes as well
        if check_total_stroke(conn, n1, n2, n3) is False:
            continue

        # name_type = '%s%s%s' % (n1[4], n2[4], n3[4])
        # print(name2, name_type)
        # if support_weak_energy(n2[4], saju) is False:
        #    continue
        # STEP 4: 오행의 배치 관계, 발음오행 (상생) 운혜본 채택 말이 안됨.
        # if check_five_type(name_type) is False:
        #    continue

        # STEP 2: 수리영동 조직관계
        # STEP 7: 수리 역상의 관계, 한자획수, 원형이정

        # STEP 3: 음양 배열 관계

        #   # total stroke 확인하는 로직과 중복되어 삭제
        # if check_plus_minus_hanja(conn, n1, n2, n3) is False:
        #    continue

        # STEP 6: 음령 오행의 역상 관계
        if check_all_name_hard_pronounce(n1, n2, n3) is False:
            continue

        temp_name = '%s%s%s' % (n1[1], n2[1], n3[1])
        name_list.append(temp_name)

    if len(name_list) == 0:
        return None

    return name_list


def get_total_strokes(n1, n2, n3=None):
    if n1[3] is None:
        n1_strk = int(n1[2])
    else:
        n1_strk = int(n1[2]) + int(n1[3])

    if n2[3] is None:
        n2_strk = int(n2[2])
    else:
        n2_strk = int(n2[2]) + int(n2[3])

    if n3 is None:
        total_strokes = n1_strk + n2_strk
        # print(n1[2], n1[3], n2[2], n2[3], '---> ', total_strokes)
    else:
        if n3[3] is None:
            n3_strk = int(n3[2])
        else:
            n3_strk = int(n3[2]) + int(n3[3])
        # 획수음양
        if n1_strk % 2 == 0 and n2_strk % 2 == 0 and n3_strk % 2 == 0:
            return 0  # 획수가 모두 짝수는 불가
        elif n1_strk % 2 == 1 and n2_strk % 2 == 1 and n3_strk % 2 == 1:
            return 0  # 획수가 모두 홀수는 불가

        total_strokes = n1_strk + n2_strk + n3_strk
        # print(n1[2], n1[3], n2[2], n2[3], n3[2], n3[3], '-> ', total_strokes)
    return total_strokes


"""
 사주에 ‘木’이 3개이상 있을때는 ‘火’ 또는 ‘金’에 해당하는 글자로 작명합니다.
 사주에 ‘土’가 3개이상 있을때는 ‘金’ 또는 ‘木’에 해당하는 글자로 작명합니다.
 사주에 ‘火’가 3개이상 있을때는 ‘土’ 또는 ‘水’에 해당하는 글자로 작명합니다.
 사주에 ‘金’이 3개이상 있을때는 ‘水’ 또는 ‘火’에 해당하는 글자로 작명합니다.
 사주에 ‘水’가 3개이상 있을때는 ‘木’ 또는 ‘土’에 해당하는 글자로 작명합니다.
"""


def type_check_with_strong_energy(strong, row):
    if strong == '木':
        if row[4] == '火' or row[4] == '金':
            return True
    elif strong == '土':
        if row[4] == '金' or row[4] == '木':
            return True
    elif strong == '火':
        if row[4] == '土' or row[4] == '水':
            return True
    elif strong == '金':
        if row[4] == '水' or row[4] == '火':
            return True
    elif strong == '水':
        if row[4] == '木' or row[4] == '土':
            return True
    return False


def type_check_with_month(saju, row):
    strong = saju['strong']
    month = saju['month']
    # 木火土金水
    if month == '01' or month == '02' or month == '03':
        if strong == '木' and row[4] == '木':
            return False
        elif strong == '木' and row[4] == '水':
            return False
        elif strong == '火' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '火':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '土' and row[4] == '木':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '金' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '金':
            return False
    elif month == '04' or month == '05' or month == '06':
        if strong == '木' and row[4] == '火':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '土':
            return False
        elif strong == '火' and row[4] == '木':
            return False
        elif strong == '土' and row[4] == '火':
            return False
        elif strong == '土' and row[4] == '土':
            return False
        elif strong == '金' and row[4] == '火':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '水' and row[4] == '火':
            return False
        elif strong == '水' and row[4] == '木':
            return False
    elif month == '07' or month == '08' or month == '09':
        if strong == '木' and row[4] == '金':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '金':
            return False
        elif strong == '火' and row[4] == '土':
            return False
        elif strong == '土' and row[4] == '金':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '金' and row[4] == '金':
            return False
        elif strong == '金' and row[4] == '土':
            return False
        elif strong == '水' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '金':
            return False
    elif month == '10' or month == '11' or month == '12':
        if strong == '木' and row[4] == '水':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '水':
            return False
        elif strong == '火' and row[4] == '金':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '土' and row[4] == '金':
            return False
        elif strong == '金' and row[4] == '水':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '水' and row[4] == '金':
            return False
        elif strong == '水' and row[4] == '水':
            return False

    return True


def check_support_type(support_type, middle_type):
    for i in range(len(support_type)):
        if middle_type == support_type[i]:
            return True
    return False


def check_name(temp_name):
    try:
        if BLOCK_LIST[temp_name] == 1:
            return False
    except:
        try:
            if WORDS_LIST[temp_name] == 1:
                return False
        except:
            return True
    return True


# DBG
def get_one_last_name():
    rd = randrange(len(LAST_NAME_LIST))
    return LAST_NAME_LIST[rd]


# DBG
def get_random_birth():
    # '200103010310'  # '200203011201'
    year = randrange(1990, 2017, 1)
    month = randrange(1, 12, 1)
    day = randrange(1, 28, 1)
    hour = randrange(1, 24, 1)
    minute = randrange(1, 60, 1)
    return '%d%02d%02d%02d%02d' % (year, month, day, hour, minute)


def print_men_women(temp):
    MEN_LAST_NAME = [
        '기', '관',
        '욱', 
        '승', '석',
        '준', 
        '찬',
        '혁' '훈', '학', 
    ]
    WOMEN_LAST_NAME = [
        '미',
        '희',
        '혜',
    ]

    men = []
    women = []
    both = []

    for i in range(len(temp)):
        done = 0
        for j in range(len(MEN_LAST_NAME)):
            if temp[i][2] == MEN_LAST_NAME[j]:
                men.append(temp[i])
                done = 1
                break
        for k in range(len(WOMEN_LAST_NAME)):
            if temp[i][2] == WOMEN_LAST_NAME[k]:
                women.append(temp[i])
                done = 1
                break
        if done == 0:
            both.append(temp[i])
    print("MEN  : ", men)
    print("WOMEN: ", women)
    print("BOTH : ", both)


def main():
    start_time = time()  # START
    conn = sqlite3.connect('naming_korean.db')

    # DBG TEST data
    birth = get_random_birth()  # '200103010310'  # '200203011201'
    ln = get_one_last_name()
    birth = '199611160347'
    ln = '尙'

    # LAST NAME
    n1 = get_last_name_info(conn, ln)

    # SAJU
    saju = get_saju(conn, birth)
    if saju is None:
        print('[ERR] get saju failed')
        return
    print('추가해야할 행: ', saju['support_type'])

    name_list = []
    cnt = 0
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,five_type
    FROM naming_hanja
    WHERE is_naming_hanja=1
    AND reading
    NOT IN ('각', '과', '국', '니', '렴', '렬', '린', '랑', '려', '령', '락',
    '량', '련', '목', '복', '해', '엄', '열', '오', '요', '왕', '욱', '읍',
    '빈', '표', '필', '탁', '회', '후', '흠',
    '균', '옥', '류', '료', '안')
    """
    for n2 in s.execute(query):
        if n1[1] == n2[1]:  # 장장호
            continue

        n1n2 = '%s%s' % (n1[1], n2[1])
        if check_name(n1n2) is False:
            continue

        ts = get_total_strokes(n1, n2, None)
        if ts == 0 or check_81_suri(conn, ts) is False:  # (홍+길) 동
            continue

        # TODO: check with SAJU

        names = get_name_list(conn, n1, n2, saju)
        if names is None:
            continue
        name_list.extend(names)
        cnt += 1
#        # 자원오행 (보완)
#        if type_check_with_month(saju, row) is False:
#            continue
#        # if type_check_with_strong_energy(saju['strong'], row) is False:
#        #    continue
#        if check_support_type(saju['support_type'], row[4]) is False:
#            continue
#        if check_two_words_hard_pronounce(last_name[1], row[1]) is False:
#            continue
    # DBG
    temp = array_remove_duplicates(name_list)
    print_men_women(temp)
    print(ln, birth)
    print("%.3f sec, Total: %d(%d) -> %d" % ((time() - start_time), len(name_list), cnt, len(temp)))

    conn.close()  # db close
    return


if __name__ == '__main__':
    main()

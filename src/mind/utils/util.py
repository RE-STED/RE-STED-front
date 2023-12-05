import os
import random
import json

def random_choice(a : list):
    
    # 선택한 파일이름이 .DS_Store이면 다시 선택
    while True:
        choice = random.choice(a)
        if choice != '.DS_Store':
            break
    return choice

def select_level(dict):
    '''
    dict에서 오늘 혹은 최근 날짜의 "Pattern" 수행 리스트를 받아서 레벨과 점수를 추출하여 시간순으로 나열
    최근 수행 기록이 5개 이하면 1을 반환하고, 5개 이상이면 최근 5개의 레벨이 모두 같고 점수가 100점이면 레벨+1을 반환
    '''
    level = []
    score = []
    dates = sorted(dict.keys(), reverse=True)

    for key in dates:
        for result in sorted(dict[key]['Pattern'], key=lambda x: x['Time'], reverse=True):
            level.append(result['Level'])
            score.append(result['Score'])
            if len(level) == 5:
                break

    if len(level) == 0:
        return 1
    
    elif len(level) < 5:
        return max(level)
    else:
        if len(set(level)) == 1 and sum(score) >= 480:
            return max(level) + 1 if max(level) <= 2 else 3
        else:
            return max(level)
        
        
if __name__ == '__main__':
            
    json2 = "src/mind/Result.json"

    with open(json2, 'r', encoding='utf-8') as f:
        dict = json.load(f)
    print(select_level(dict))
    
    
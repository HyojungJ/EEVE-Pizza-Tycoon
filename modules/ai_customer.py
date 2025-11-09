import ollama
import re

def customer_order(prompt):
    response = ollama.chat(
        model='EEVE-Korean-10.8B',
        messages=[
            {"role": "system", "content": f"{prompt} 응답은 100자 이내로 작성해 주세요."}, 
            {"role": "user", "content": "까다롭고 제대로 이해하기 힘든 주문을 만들어 주세요."}
        ]
    )
    return response['message']['content']  

def toppings_check(response):
    """
    AI 응답에서 주문 텍스트와 토핑 리스트를 추출
    """
    # 1. 딕셔너리 형식 체크 (예: {"주문": ['토핑']})
    dict_match = re.search(r'\{[^}]+\}', response)
    if dict_match:
        dict_str = dict_match.group(0)
        # 딕셔너리 앞의 텍스트를 주문으로 추출
        order = response[:dict_match.start()].strip()
        # 콜론 제거 (예: "두 가지 토핑 피자 주문하기:" -> "두 가지 토핑 피자 주문하기")
        order = order.rstrip(':').strip()
        
        # 리스트 부분 추출
        list_match = re.search(r'\[([^\]]+)\]', dict_str)
        if list_match:
            toppings_str = list_match.group(1)
            # 따옴표 제거하고 토핑 리스트 생성
            toppings = [t.strip().strip("'\"") for t in toppings_str.split(',')]
            return toppings, order
    
    # 2. "사용된 토핑:" 형식 체크
    toppings_match = re.search(r'사용된 토핑:\s*(.*)', response)
    if toppings_match:
        toppings = [t.strip() for t in toppings_match.group(1).split(',')]
        order = response.split('사용된 토핑:')[0].strip()
        return toppings, order
    
    # 3. 기본값: 전체를 주문으로, 빈 토핑 리스트
    return [], response.strip()

def customer_review(prompt, is_correct):
    
    if is_correct:
        user_message = "주문에 맞는 완벽한 피자를 받았습니다. 긍정적인 반응을 보여주세요."
    else:
        user_message = "주문과 다른 피자를 받았습니다. 부정적인 반응을 보여주세요."
    
    response = ollama.chat(
        model='lancard/korean-yanolja-eeve',
        messages=[
            {"role": "system", "content": f"{prompt} 응답은 100자 이내로 작성해 주세요."}, 
            {"role": "user", "content": user_message}
        ]
    )
    return response['message']['content']  
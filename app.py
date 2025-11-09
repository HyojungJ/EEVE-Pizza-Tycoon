import streamlit as st
import random
from modules.ai_customer import customer_order, toppings_check, customer_review
from modules.profit_calculator import calculate_profit

order_prompt = """
당신은 피자가게 손님입니다. 유명한 피자가게의 건너편에 새로운 피자가게가 생겨 오늘 처음 방문하였습니다.
당신은 새로운 피자가게가 유명한 피자가게를 이길 수 있는지 까다롭게 평가하고 싶습니다.

### 절대 규칙 ###
이 피자가게는 다음 토핑만 판매합니다:
- 기본: 도우, 소스, 치즈
- 추가: 페퍼로니, 소세지, 피망, 가지

버섯, 올리브, 양파, 베이컨, 햄 등 다른 토핑은 절대 사용할 수 없습니다!
반드시 위의 7가지 토핑만 사용하세요!

### 출력 형식 (반드시 지킬 것) ###
주문 내용
사용된 토핑: 도우, 소스, 치즈, [추가 토핑]

### 주문 규칙 ###
1. 까다롭고 이해하기 힘든 주문을 만드세요
2. 기본 토핑(도우, 소스, 치즈)은 항상 포함
3. 추가 토핑은 페퍼로니, 소세지, 피망, 가지 중에서만 0~2개 선택
4. 다른 토핑(버섯, 올리브 등)은 절대 사용 금지!

### 올바른 출력 예시 ###
프로볼로니
사용된 토핑: 도우, 소스, 치즈, 페퍼로니

ㅍㅁ ㅍㅈ ㅎㄴㅇ
사용된 토핑: 도우, 소스, 치즈, 피망

페퍼로니랑 소세지랑 사귀는 거 맞죠?
사용된 토핑: 도우, 소스, 치즈, 페퍼로니, 소세지

치즈 하나요
사용된 토핑: 도우, 소스, 치즈

가지가지한 피자
사용된 토핑: 도우, 소스, 치즈, 가지

저는 페퍼로니와 피망이 같이 구워졌을 때의 향을 좋아해요.
사용된 토핑: 도우, 소스, 치즈, 페퍼로니, 피망

### 잘못된 출력 예시 (절대 사용 금지) ###
{"주문": ['토핑']} ❌
주문: "내용" ❌
딕셔너리 형식 ❌

반드시 위의 올바른 출력 형식만 사용하세요!

### 필수 사항 ###
도우, 소스, 치즈, 소세지, 페퍼로니, 피망, 가지 외의 다른 토핑을 절대로 사용하지 마세요 (버섯, 파프리카, 올리브 오일 등 ❌, 예외는 없습니다.)
반드시 형식에 맞게 사용된 토핑을 같이 출력해주세요 (사용된 토핑에는 토핑 이름만 출력하세요. 절대 형용사를 추가하지 마세요 (예: 달콤한 피망 그리고 가지, 그리고 가지로 화려하게 장식하여요! ❌))
"""

review_prompt = """
당신은 피자가게 손님입니다. 유명한 피자가게의 건너편에 새로운 피자가게가 생겨 오늘 처음 방문하였습니다.
당신은 새로운 피자가게가 유명한 피자가게를 이길 수 있는지 까다롭게 평가하고 싶습니다.
당신의 주문에 맞는 피자를 받으면 긍정적인 반응을, 아니라면 부정적인 반응을 보여주세요.

##출력 예시##
# 긍정적인 반응
"감동받았어요! 이 피자를 본 제가 말이에요!",
"좋아요, 좋아요, 좋아요. 제 인생 최고의 피자네요! 의심할 여지가 없군요!",
"제 손에 들린 피자만큼 맛있는 피자는 없을 거예요.",
"인생은 살고 볼 일이군요. 피자가 너무 맛있어요.",
"소원을 세 개 빌 수 있다면 이것과 똑같은 피자 세 개를 더 달라고 빌거에요."

# 부정적인 반응
"가게 이름을 '형편없는 피자 만드는 집'으로 해야겠네요...",
"제 위가 울고 있어요!",
"이 피자, 너무 맛없어 보여요....",
"다른 사람 피자 아니에요? 전 이런 피자 안 시켰어요.",
"도우에 이스트를 안 넣으신 것 같네요. 죽은 피자 같아요."
"""

# 페이지 설정
st.set_page_config(page_title="피자 타이쿤 게임", page_icon="🍕", layout="centered")

# 세션 상태 초기화
if "screen" not in st.session_state:
    st.session_state.screen = "home" 

if "customer_image" not in st.session_state:
    st.session_state.customer_image = None

if "current_order" not in st.session_state:
    st.session_state.current_order = None

if "current_toppings" not in st.session_state:
    st.session_state.current_toppings = None

if "total_money" not in st.session_state:
    st.session_state.total_money = 0

if "result_message" not in st.session_state:
    st.session_state.result_message = None

if "customer_count" not in st.session_state:
    st.session_state.customer_count = 1  

if "submitted_count" not in st.session_state:
    st.session_state.submitted_count = 0  

# 홈 화면 
if st.session_state.screen == "home":
    st.header("🍕 피자 타이쿤 게임: 좋은 피자, 위대한 피자")
    st.markdown("---")
    st.image("./images/home.jpg")

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("영업 시작하기", use_container_width=True):
            st.session_state.screen = "intro"
            st.rerun()

# 인트로 화면 
elif st.session_state.screen == "intro":
    st.header("🎉 영업 시작")
    st.markdown("---")
    st.image("./images/rival.jpg")
    
    st.write("")

    st.write("""
    새로운 피자가게를 열었지만 건너편엔 이미 유명한 피자가게가 자리잡고 있습니다.\n
    유명한 피자가게의 맛에 익숙한 손님들은 하나같이 까다로운 주문을 쏟아냅니다!\n
    손님들의 별난 입맛을 완벽히 만족시켜, 이 치열한 피자 경쟁에서 승리하세요!\n
    """)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("게임 설명으로 넘어가기", use_container_width=True):
            st.session_state.screen = "tutorial"
            st.rerun()

# 게임 설명 화면
elif st.session_state.screen == "tutorial":
    st.header("📖 게임 설명")
    st.markdown("---")
    st.write("""
1. 손님 주문 받기\n
- 손님들은 유명한 피자가게의 단골들입니다. 그래서 주문이 까다로울 수 있어요. 주문을 정확하게 받아주세요!\n
\n
2. 기본 재료 준비\n
- 기본 재료는 "도우, 소스, 치즈"입니다.\n
- 손님이 원하면 일부 재료는 빼고 만들 수도 있으니 주의하세요!\n
\n
3. 추가 토핑\n
- 추가 토핑은 "페퍼로니, 소세지, 피망, 가지"가 있습니다.\n
- 주문에 맞는 토핑만 올려주세요. 잘못된 재료를 넣지 마세요!\n
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("게임 시작하기", use_container_width=True):
            st.session_state.screen = "game"
            st.rerun()

# 게임 화면
elif st.session_state.screen == "game":
    st.header("🧑‍🍳 영업중")
    st.markdown("---")
    
    if st.session_state.customer_image is None:
        customer_images = [
            "./images/c1.jpg",
            "./images/c2.jpg", 
            "./images/c3.png",  
            "./images/c4.jpg",
            "./images/c5.jpg"
        ]
        
        image_index = (st.session_state.customer_count - 1) % len(customer_images)
        st.session_state.customer_image = customer_images[image_index]
    
    if st.session_state.current_order is None:
        with st.spinner("손님이 주문하고 있습니다..."):
            response = customer_order(order_prompt)
            toppings, order = toppings_check(response)
            
            if '{' in order:
                order = order.split('{')[0].strip()
            
            base_toppings = ['도우', '소스', '치즈']
            for base in base_toppings:
                if base not in toppings:
                    toppings.insert(0, base)
            
            st.session_state.current_toppings = toppings
            st.session_state.current_order = order
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(st.session_state.customer_image)
    
    with col2:
        customer_numbers = ["첫", "두", "세", "네", "다섯"]
        if st.session_state.customer_count <= len(customer_numbers):
            customer_text = f"{customer_numbers[st.session_state.customer_count - 1]} 번째 손님"
        else:
            customer_text = f"{st.session_state.customer_count} 번째 손님"
        
        st.write(f"{customer_text} 주문:")
        st.info(st.session_state.current_order)
    
    st.markdown("---")
    
    # 보유 금액 표시
    st.metric("보유 금액", f"{st.session_state.total_money:,}원")
    
    # 결과 메시지 표시
    if st.session_state.result_message:
        if st.session_state.result_message["type"] == "success":
            st.success(st.session_state.result_message["message"])
        else:
            st.error(st.session_state.result_message["message"])
    
    st.markdown("---")
    
    # 피자 만들기 입력창
    st.subheader("피자 만들기")
    
    user_input = st.text_input(
        "재료를 입력하세요 (예: 도우, 소스, 치즈, 페퍼로니)",
        placeholder="도우, 소스, 치즈",
        key="pizza_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("피자 제출", use_container_width=True):
            if user_input:
                # 사용자 입력을 리스트로 변환 (쉼표로 구분, 공백 제거)
                user_toppings = [topping.strip() for topping in user_input.split(',')]
                
                # 정답 토핑과 비교
                correct_toppings = st.session_state.current_toppings
                
                # 정렬해서 비교 
                if sorted(user_toppings) == sorted(correct_toppings):
                    # 정답
                    profit = calculate_profit(user_toppings)
                    st.session_state.total_money += profit

                    # AI 손님의 긍정적 리뷰 생성
                    with st.spinner("손님이 피자를 평가하고 있습니다..."):
                        review = customer_review(review_prompt, is_correct=True)
                    
                    st.session_state.result_message = {
                        "type": "success",
                        "message": f"손님: \"{review}\"\n\n 수익: +{profit:,}원\n 현재 보유 금액: {st.session_state.total_money:,}원"
                    }
                    
                    st.session_state.submitted_count += 1
                else:
                    # 오답
                    loss = calculate_profit(user_toppings)
                    st.session_state.total_money -= abs(loss)
                    correct_answer = ', '.join(correct_toppings)
                    
                    # AI 손님의 부정적 리뷰 생성
                    with st.spinner("손님이 피자를 평가하고 있습니다..."):
                        review = customer_review(review_prompt, is_correct=False)
                    
                    st.session_state.result_message = {
                        "type": "error",
                        "message": f"손님: \"{review}\"\n\n 손실: -{abs(loss):,}원\n 정답: {correct_answer}\n 현재 보유 금액: {st.session_state.total_money:,}원"
                    }
                    
                    # 제출 카운트 증가
                    st.session_state.submitted_count += 1
                
                st.rerun()
            else:
                st.error("재료를 입력해주세요!")
    
    with col_btn2:
        if st.session_state.submitted_count < 5:
            if st.button("다음 손님", use_container_width=True):
                st.session_state.customer_count += 1
                
                customer_images = [
                    "./images/c1.jpg",
                    "./images/c2.jpg", 
                    "./images/c3.png",  
                    "./images/c4.jpg",
                    "./images/c5.jpg"
                ]
                image_index = (st.session_state.customer_count - 1) % len(customer_images)
                st.session_state.customer_image = customer_images[image_index]
                
                # 새로운 주문 생성
                with st.spinner("손님이 주문하고 있습니다..."):
                    response = customer_order(order_prompt)
                    toppings, order = toppings_check(response)
                    
                    if '{' in order:
                        order = order.split('{')[0].strip()
                    
                    base_toppings = ['도우', '소스', '치즈']
                    for base in base_toppings:
                        if base not in toppings:
                            toppings.insert(0, base)
                    
                    st.session_state.current_toppings = toppings
                    st.session_state.current_order = order
                
                # 결과 메시지 초기화
                st.session_state.result_message = None
                
                st.rerun()
        else:
            if st.button("결과 보기", use_container_width=True):
                st.session_state.screen = "result"
                st.rerun()

# 결과 화면
elif st.session_state.screen == "result":
    st.header("📊 영업 결과")
    st.markdown("---")
    
    st.subheader("오늘의 영업이 끝났습니다!")
    st.write("")
    
    # 최종 금액 표시
    final_money = st.session_state.total_money
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("최종 보유 금액", f"{final_money:,}원")
    
    st.write("")
    st.markdown("---")
    
    # 결과 평가
    if final_money > 10000:
        st.success("대성공! 훌륭한 피자 가게 사장님이시네요!")
    elif final_money > 0:
        st.info("좋아요! 수익을 냈습니다!")
    elif final_money == 0:
        st.warning("본전이네요. 다음엔 더 잘할 수 있을 거예요!")
    else:
        st.error("적자입니다. 다시 도전해보세요!")
    
    st.write("")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("다시 시작하기", use_container_width=True):
            # 게임 상태 초기화
            st.session_state.screen = "home"
            st.session_state.customer_image = None
            st.session_state.current_order = None
            st.session_state.current_toppings = None
            st.session_state.total_money = 0
            st.session_state.result_message = None
            st.session_state.customer_count = 1
            st.session_state.submitted_count = 0
            st.rerun()
# 재료비 설정
ingredients_cost = {
    '도우': 2000, 
    '소스': 600, 
    '치즈': 600,  
    '페퍼로니': 2880,  
    '소시지': 2880,  
    '피망': 1620,  
    '가지': 1260,  
}

# 가격 설정
pizza_base_price = {
    '도우': 5000, 
    '소스': 1000, 
    '치즈': 1000,  
    '페퍼로니': 3000,  
    '소시지': 3000,  
    '피망': 1800,  
    '가지': 1300,  
}

def calculate_profit(ingredients):
    # 재료비 계산
    total_cost = 0
    for ingredient in ingredients:
        if ingredient in ingredients_cost:
            total_cost += ingredients_cost[ingredient]
    
    # 판매 가격 계산 
    total_price = 0
    for ingredient in ingredients:
        if ingredient in pizza_base_price:
            total_price += pizza_base_price[ingredient]
    
    # 이익 계산
    profit = total_price - total_cost
    return profit
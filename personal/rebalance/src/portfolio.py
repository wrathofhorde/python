import numpy as np


def rebalance_portfolio(weights: np.ndarray, target_weights: np.ndarray, total_value: int, 
    prices: list, assets: list) -> list:
    """
    포트폴리오 비중 조절을 계산하여 매수/매도 수량을 반환합니다.
    
    Args:
        weights (np.ndarray): 현재 자산 비중
        target_weights (np.ndarray): 목표 자산 비중
        total_value (float): 포트폴리오 총 가치
        prices (list): 각 자산의 단위 가격
        assets (list): 자산 이름 목록
        
    Returns:
        list: 각 자산의 매수/매도 수량 및 액션
    """
    print("현재 비중:", [f"{w:.2f}" for w in weights])
    print("목표 비중:", [f"{tw:.2f}" for tw in target_weights])
    
    adjustments = target_weights - weights
    results = []
    
    for i, (asset, adjustment, price) in enumerate(zip(assets, adjustments, prices)):
        # 조정 금액 = 비중 차이 * 총 가치
        adjustment_value = adjustment * total_value
        # 수량 = 조정 금액 / 자산 가격 (정수로 반올림)
        quantity = round(adjustment_value / price)
        action = "매수" if quantity > 0 else "매도" if quantity < 0 else "유지"
        results.append({
            "asset": asset,
            "action": action,
            "quantity": abs(quantity),
            "adjustment_value": adjustment_value
        })
        print(f"{asset}: {action} {abs(quantity)}주 (조정 금액: {adjustment_value:.2f}원)")
    
    return results

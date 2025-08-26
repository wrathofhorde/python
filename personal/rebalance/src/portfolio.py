import numpy as np
from icecream import ic

def rebalance(total_value: int, target_weights: list, assets: list, prices: list, quantities: list):
    results = []
    buy = []

    for i, (asset, price, quantity, target_weight) in enumerate(zip(assets, prices, quantities, target_weights)):
        adjustment_value = int(target_weight * total_value)
        target_quantity = int(adjustment_value / price)
        adjustment_quantity = target_quantity - quantity
        action = "매수" if adjustment_quantity > 0 else "매도"
        buy.append(target_quantity * price)
        results.append({
            "종목": asset,
            "목표수량": target_quantity,
            "매수/매도": action,
            "추가수량": adjustment_quantity,
            "조정후매수금액": target_quantity * price
        })

    total_buy = sum(buy)
    results.append({
        "매수금액": total_buy,
        "현금": total_value - total_buy
    })

    ic(results)

    return results
    

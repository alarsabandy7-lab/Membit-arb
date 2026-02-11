import numpy as np

class QuantEngine:
    def __init__(self, alpha, f_safe):
        self.alpha = alpha   # Target 90% profit extraction
        self.f_safe = f_safe # Fractional Kelly multiplier (e.g., 0.2)

    def calculate_kl_divergence(self, mu, p):
        # Math: Measures the distance between target price and market price
        return np.sum(mu * np.log(mu / p))

    def get_position_size(self, p_market, mu_target, fw_gap, equity):
        # 1. Calculate Guaranteed Profit (Prop 4.1)
        divergence = self.calculate_kl_divergence(mu_target, p_market)
        guaranteed_profit = divergence - fw_gap

        # 2. Convergence Check (Stop & Trade Condition)
        if guaranteed_profit > 0 and fw_gap <= (1 - self.alpha) * divergence:
            # 3. Kelly Criterion: f* = (bp - q) / b
            # b = odds (1/price - 1), p = target probability (mu)
            b = (1 / p_market) - 1
            f_star = (b * mu_target - (1 - mu_target)) / b
            
            # 4. Final Sizing via Fractional Kelly & Equity
            return equity * (f_star * self.f_safe)
        
        return 0 # Condition not met

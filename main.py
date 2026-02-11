from core.engine import QuantEngine
from core.sentiment import MembitSentiment
from config import ALPHA, KELLY_FRACTION

def main_loop():
    engine = QuantEngine(ALPHA, KELLY_FRACTION)
    membit = MembitSentiment()

    while True:
        # Get raw data
        prices = api.get_market_prices()
        raw_texts = api.get_social_feed()

        # Step 1: Sentiment Instinct (Membit)
        sentiment_bias = membit.process_signals(raw_texts)

        # Step 2: Math Logic (Frank-Wolfe)
        # The bias shifts the target_mu before checking Kelly
        target_mu = solver.solve_with_bias(prices, sentiment_bias)
        fw_gap = solver.get_current_gap()

        # Step 3: Execution Decision
        position_size = engine.get_position_size(
            prices, target_mu, fw_gap, current_equity
        )

        if position_size > 0:
            execute_trade(position_size)

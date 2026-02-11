def update_risk_parameter(pnl, slippage):
    global KELLY_FRACTION
    if pnl < 0:
        if slippage > MAX_SLIPPAGE:
            # If loss is due to illiquidity, reduce aggressiveness
            KELLY_FRACTION *= 0.8
        else:
            # If loss is due to mathematical bias, reduce more drastically
            KELLY_FRACTION *= 0.5
    else:
        # If winning, gradually increase confidence to a safe cap
        KELLY_FRACTION = min(0.2, KELLY_FRACTION + 0.01)

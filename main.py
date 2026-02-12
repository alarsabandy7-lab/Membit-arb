import time
import logging
from core.engine import GodModeEngine
from utils.api_connect import PolymarketAPI, SocialScraper

# 1. SETUP LOGGING (For GitHub Audit Transparency)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("data/bot_runtime.log"), logging.StreamHandler()]
)

def main():
    # Initial Configuration
    config = {
        'alpha': 0.9,
        'kelly_fraction': 0.15,
        'initial_capital': 1000.0,  # Starting Balance
        'min_edge': 0.015
    }

    # Initialize Engine and Connectors
    bot = GodModeEngine(config)
    poly_api = PolymarketAPI()
    social_api = SocialScraper()

    logging.info("--- GOD-MODE ENGINE ACTIVATED ---")

    while True:
        try:
            # A. DATA INGESTION
            # Fetching real-time Order Book, Prices, and Sentiment
            market_data = poly_api.get_market_snapshot()
            order_book = poly_api.get_order_book()
            raw_social_signals = social_api.fetch_latest_signals()
            current_balance = poly_api.get_balance()

            # B. UNIFIED SOLVER (The 6 Elements)
            decision = bot.unified_solver(
                market_data, 
                raw_social_signals, 
                current_balance, 
                order_book
            )

            # C. EXECUTION GATE
            if decision['action'] == 'EXECUTE':
                logging.info(f"SIGNAL DETECTED: Placing order of size {decision['size']:.2f}")
                
                # Execute Trade via API
                execution_report = poly_api.place_order(
                    side='BUY', 
                    amount=decision['size']
                )

                # D. BAYESIAN LEARNING (The Memory)
                # Update the bot's internal brain based on execution results
                bot.update_brain(
                    pnl=execution_report['realized_pnl'],
                    slippage_realized=execution_report['slippage']
                )
                
                logging.info(f"LEARNING UPDATE: New Alpha: {bot.alpha:.4f}, New Kelly F: {bot.kelly_f:.4f}")

            else:
                logging.debug("HEARTBEAT: Scanning for Edge...")

            # E. ADAPTIVE SLEEP
            # High-frequency scanning with rate-limit protection
            time.sleep(1)

        except KeyboardInterrupt:
            logging.info("Shutting down gracefully...")
            break
        except Exception as e:
            logging.error(f"CRITICAL ERROR: {str(e)}")
            time.sleep(5) # Cooldown on error

if __name__ == "__main__":
    main()

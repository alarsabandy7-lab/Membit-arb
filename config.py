import os
from dotenv import load_dotenv

load_dotenv()

# MATHEMATICAL PARAMETERS (ROAN MATH)
ALPHA = 0.9           # Extract 90% of available arbitrage
EPSILON_START = 0.1   # Initial adaptive contraction for Barrier FW

# RISK PARAMETERS (LEARN FROM LOSS)
KELLY_FRACTION = 0.15 # Start with 15% of Kelly's recommendation
MAX_SLIPPAGE = 0.02   # Max allowed slippage (2%)

# API CREDENTIALS
POLY_API_KEY = os.getenv("POLY_API_KEY")

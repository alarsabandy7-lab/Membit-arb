# Membit-arb: Prediction Market Arbitrage Bot

## Overview
Membit-arb is an experimental quantitative finance framework for identifying and executing arbitrage opportunities in prediction markets. The system employs barrier Frank-Wolfe optimization with adaptive spacing rules and Kelly Criterion position sizing to generate alpha-extraction signals while maintaining risk-bounded operations.

## Key Features
- **Barrier Frank-Wolfe Optimization**: Adaptive ε-contraction for stable gradient computation
- **Marginal Polytope Navigation**: Valid interior point initialization to prevent gradient explosion
- **Fractional Kelly Sizing**: Data-driven position sizing based on probability estimates
- **Alpha-Extraction Threshold**: Configurable trigger for market inefficiency detection
- **Educational & Research Focus**: Designed for quantitative finance experimentation

## Mathematical Foundation

### Initialization (InitFW)
Before optimization begins, the system identifies a valid interior point **u** within the marginal polytope to:
- Prevent gradient explosion in early iterations
- Establish a stable reference point for the search procedure
- Ensure Lipschitz continuity of market scoring rule gradients

### Barrier Frank-Wolfe Algorithm
The core optimization employs an adaptive ε-contraction rule:
- **Search Space Shrinking**: By contracting toward the interior point u, we maintain bounded Lipschitz constants
- **Gradient Stability**: The LMSR (Logarithmic Market Scoring Rule) gradient remains stable throughout optimization
- **Convergence Guarantees**: Adaptive spacing ensures convergence to optimal probability estimates

### Position Sizing via Fractional Kelly Criterion
```
Position Size = f × (p × odds - 1) / odds
where:
  f = Kelly fraction (safety parameter, typically 0.25)
  p = probability derived from Frank-Wolfe target μ
```

## Alpha-Extraction & Risk Management

### Trigger Condition
The bot executes trades only when:
```
g(μ) ≤ (1 - α) × D(μ || p)
```
Where:
- **g(μ)** = Market inefficiency measure
- **D(μ || p)** = KL divergence between market and estimated probabilities
- **α** = Minimum alpha extraction threshold (configurable)

### Risk Disclaimer ⚠️
**This software is for educational and research purposes in quantitative finance only.**
- Prediction markets involve substantial financial risk
- Past performance does not guarantee future results
- Do not deploy with real capital without proper risk management
- Users assume all responsibility for trading decisions and losses

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment recommended

### Setup
```bash
# Clone repository
git clone https://github.com/alarsabandy7-lab/Membit-arb.git
cd Membit-arb

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials
```

## Usage

### Basic Example
```python
from membit_arb import BarrierFrankWolfe, KellySizer

# Initialize optimizer
optimizer = BarrierFrankWolfe(epsilon=0.01)

# Run optimization
mu_optimal = optimizer.optimize(market_probs, interior_point)

# Calculate position size
kelly_sizer = KellySizer(kelly_fraction=0.25)
position = kelly_sizer.size(mu_optimal, odds)
```

### Running the Bot
```bash
python main.py
```

**Important**: Verify `main.py` starts without errors before any operations.

## Environment Configuration

Create a `.env` file in the project root:
```
POLYMARKET_API_KEY=your_key_here
POLYMARKET_API_SECRET=your_secret_here
WALLET_ADDRESS=your_address_here
KELLY_FRACTION=0.25
ALPHA_THRESHOLD=0.05
```

⚠️ **Security**: Never commit `.env` to version control. Use `.gitignore` to exclude it.

## Implementation Roadmap

- [ ] Integrate Polymarket CLOB (Central Limit Order Book) API
- [ ] Implement HDBSCAN for real-time Sentiment Clustering (Membit Logic)
- [ ] Add support for Multi-Leg Arbitrage (Conditional Outcomes)
- [ ] Develop Backtesting Engine for historical NCAA data
- [ ] Add performance metrics and attribution analysis
- [ ] Implement circuit breakers and risk limits

## Project Structure
```
Membit-arb/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── src/
│   ├── optimizer.py       # Frank-Wolfe implementation
│   ├── kelly.py           # Kelly Criterion sizing
│   ├── market.py          # Market interface
│   └── utils.py           # Utilities
├── tests/
│   ���── test_*.py          # Unit tests
├── docs/
│   └── MATHEMATICAL_FRAMEWORK.md
└── README.md              # This file
```

## Dependencies
See `requirements.txt` for complete list. Key packages:
- NumPy: Numerical computing
- SciPy: Scientific algorithms
- Requests: HTTP client
- Python-dotenv: Environment management

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Recommended**: Add `LICENSE` file to your repository root for clarity on usage rights.

## References

- Boyd, S., & Parikh, N. (2013). Proximal algorithms.
- Abernethy, J., & Wang, J. C. (2014). Frank-Wolfe optimization for symmetric-NMF.
- Thorp, E. O. (1997). The Mathematics of Gambling.

## Disclaimer

This project is experimental software. The authors are not responsible for:
- Financial losses from trading decisions
- Data accuracy or API reliability
- Security vulnerabilities in dependencies

Users must conduct thorough due diligence before any real-world deployment.

## Contact & Support

For questions or issues, please open a GitHub Issue in this repository.
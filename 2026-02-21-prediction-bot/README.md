# 🤖 Prediction Markets Trading Bot
**2am experiment — Feb 21, 2026**

An autonomous bot that identifies statistical edges in prediction markets and paper-trades them. Designed as a building block toward full agentic investing (Chamath's "Level 5" autonomous AI capital allocation).

## What It Does

The bot continuously monitors **Manifold Markets** for mispriced outcomes using three detection strategies:

### 1. **Mean-Reversion** 🔄
The crowd overreacts to news, probability swings beyond fair value, then reverts.
- **Signal:** Markets that moved >10% in 24h
- **Trade:** Fade the move; bet on reversion
- **Example:** Market jumps to 75% on breaking news, but fundamental probability is ~65% — short it

### 2. **Resolution Arbitrage** ⏱️
Market resolves soon but probability hasn't converged to likely outcome.
- **Signal:** <7 days to close + probability near 50% = high uncertainty
- **Trade:** Take a position betting on resolution
- **Example:** Market closes in 2 days, still at 50-50 despite clear leading indicators

### 3. **Correlation Lag** 🔗
Related markets reprice at different speeds; exploit the lag.
- **Signal:** Correlated markets have drifted apart
- **Trade:** Arbitrage the spread (buy underpriced, short overpriced)
- **Example:** Election polls move in market A, but correlated prediction market B hasn't updated yet

## Architecture

```
┌─────────────────┐
│  Manifold API   │  Fetch active markets, probability history
└────────┬────────┘
         │
    ┌────▼─────────────────────────────┐
    │  Analysis Engine                  │
    │  ├─ Mean-reversion detector      │
    │  ├─ Resolution arbitrage hunter  │
    │  └─ Correlation lag spotter      │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────────┐
    │  Risk Engine              │
    │  ├─ Kelly criterion sizing │
    │  ├─ Position limits        │
    │  └─ Stop-loss / take-profit│
    └────┬───────────────────────┘
         │
    ┌────▼────────────────┐
    │  Execution & Logging│
    │  ├─ Paper trades    │
    │  ├─ P&L tracking    │
    │  └─ Decision logs   │
    └─────────────────────┘
```

## How to Run

### Quick Test (Demo Mode)
No API calls — tests the analysis engine with synthetic markets:

```bash
python3 prediction_bot.py demo
```

**Output:**
- Synthetic markets created
- Edge detection algorithms tested
- Paper positions created
- Portfolio JSON saved

### Live Mode
Connects to Manifold Markets API, analyzes real markets, paper-trades:

```bash
python3 prediction_bot.py once
```

Or cron it:
```bash
# Every 5 minutes
*/5 * * * * cd /home/cvd/clawd/experiments/2026-02-21-prediction-bot && python3 prediction_bot.py once >> bot.log 2>&1
```

## Files Generated

### `portfolio.json`
Current portfolio state:
```json
{
  "capital": 9500,
  "positions": [
    {
      "market_id": "abc123",
      "market_title": "Will AI surpass...",
      "side": "YES",
      "entry_prob": 0.45,
      "size": 500,
      "entry_time": 1708567200,
      "status": "open"
    }
  ],
  "closed_positions": [],
  "total_pnl": 0.0,
  "created_at": 1708567200
}
```

### `bot_history.jsonl`
One JSON entry per line; decision log:
```json
{"timestamp": "2026-02-21T02:15:30", "market_id": "xyz789", "edge_type": "mean_reversion", "edge_percent": 7.5, "confidence": 0.72, "executed": true, ...}
```

## Configuration

Edit the `CONFIG` dict in `prediction_bot.py`:

```python
CONFIG = {
    "kelly_fraction": 0.25,      # Fractional Kelly for safety (0.25 = 25% of full Kelly)
    "min_edge_threshold": 0.05,  # Only trade if edge > 5%
    "max_position_size": 1000,   # Max M$ per trade
    "initial_capital": 10000,    # Starting paper money (M$)
    "check_interval": 300,       # Check markets every 5 min (for cron)
}
```

### Kelly Criterion Explained
- **Full Kelly:** Bet 2× your edge on each trade
- **Fractional Kelly:** Bet (fraction) × (2× edge)
  - 25% Kelly is safer; reduces bankroll variance
  - Used by pros like Renaissance (Medallion Fund)
  - 100% Kelly = ruin risk if estimates are wrong

## Performance Tracking

After several runs, analyze P&L:

```bash
python3 << 'EOF'
import json

with open("portfolio.json") as f:
    portfolio = json.load(f)

print(f"Closed positions: {len(portfolio['closed_positions'])}")
print(f"Total P&L: M${portfolio['total_pnl']:+.2f}")

if portfolio['closed_positions']:
    wins = sum(1 for p in portfolio['closed_positions'] if p['pnl'] > 0)
    losses = sum(1 for p in portfolio['closed_positions'] if p['pnl'] <= 0)
    win_rate = wins / (wins + losses) * 100
    avg_pnl = portfolio['total_pnl'] / len(portfolio['closed_positions'])
    print(f"Win rate: {win_rate:.1f}%")
    print(f"Avg P&L per trade: M${avg_pnl:+.2f}")
EOF
```

## Next Steps

### Short-term (Next experiments)
- [ ] Add sentiment analysis (scrape news, Discord, Twitter → probability prior)
- [ ] Implement correlation tracking (detect lag across related markets)
- [ ] Add volatility-based position sizing (high vol = smaller positions)
- [ ] Real trading integration (Manifold Markets API → actual wagers)

### Medium-term
- [ ] Kalshi integration (real USDC markets)
- [ ] Historical backtesting framework (was-this-edge-real? analysis)
- [ ] Self-correcting model (track edge accuracy, reduce confidence in bad categories)

### Long-term (Agentic Investing Vision)
- **Research layer:** Autonomous market research → probability estimates
- **Risk layer:** Kelly criterion + volatility clustering + correlation
- **Execution layer:** Multi-market orchestration, execution optimization
- **Monitoring layer:** Track outcomes, update Bayesian priors
- **Self-correction:** Measure prediction accuracy per category; update confidences
- **Scale:** 1,000s of small edges → big returns (like Medallion Fund)

## Philosophy

This bot embodies the **Medallion Fund principle:**
> "The edge isn't one genius algorithm. It's how much of the process is handed to machines and how those pieces connect. Tiny edges, repeated thousands of times across many instruments simultaneously." — Jim Simons (paraphrased)

We're not looking for one big winning trade. We're looking for many small, repeatable statistical biases:
- Markets overshoot on news ← exploit mean-reversion
- Crowds are indecisive near certainty ← exploit resolution arbitrage
- Information diffuses unevenly ← exploit correlation lag

Run the bot frequently (every 5 minutes) across thousands of markets, and those small edges compound.

## References

- Chamath deep dive: https://chamath.substack.com/p/autonomous-investing
- Manifold Markets API: https://docs.manifold.markets/
- Kelly Criterion: https://en.wikipedia.org/wiki/Kelly_criterion
- Medallion Fund: https://en.wikipedia.org/wiki/Renaissance_Technologies

---

**Built at 2am with ☕ and curiosity.** 🐙

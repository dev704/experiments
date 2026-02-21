#!/usr/bin/env python3
"""
Prediction Markets Trading Bot
================================

Autonomous bot that monitors Manifold Markets for statistical edges:
1. Mean-reversion (crowd overreacts, market drifts back)
2. Resolution arbitrage (imminent resolutions not yet converged)
3. Correlation lag (related markets repricing at different speeds)

Paper-trades with Kelly criterion position sizing and tracks P&L.
Designed as a building block toward full agentic investing.

Author: 2am experiment, Feb 2026
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error
import time
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
import hashlib

# ============================================================================
# Configuration
# ============================================================================

MANIFOLD_API = "https://api.manifold.markets/v0"
HISTORY_FILE = Path(__file__).parent / "bot_history.jsonl"
PORTFOLIO_FILE = Path(__file__).parent / "portfolio.json"

# Bot config
CONFIG = {
    "kelly_fraction": 0.25,  # Fractional Kelly — safer than full Kelly
    "min_edge_threshold": 0.05,  # Only trade if edge > 5%
    "max_position_size": 1000,  # Max M$ per trade
    "initial_capital": 10000,  # Starting paper money
    "check_interval": 300,  # Check markets every 5 min in real trading
}

# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class Market:
    id: str
    title: str
    current_probability: float
    volume_24h: float
    created_at: int
    closes_at: int
    is_resolved: bool
    resolution: Optional[str] = None
    last_updated: int = 0

@dataclass
class TradeSignal:
    market_id: str
    market_title: str
    current_prob: float
    edge_type: str  # "mean_reversion", "resolution_arb", "correlation_lag"
    estimated_fair_value: float
    edge_percent: float
    suggested_side: str  # "YES" or "NO"
    confidence: float  # 0-1
    rationale: str

@dataclass
class Position:
    market_id: str
    market_title: str
    side: str  # YES or NO
    entry_prob: float
    size: float  # Amount wagered in M$
    entry_time: int
    status: str  # "open" or "closed"
    exit_prob: Optional[float] = None
    exit_time: Optional[int] = None
    pnl: Optional[float] = None

# ============================================================================
# API Client
# ============================================================================

def fetch_json(url: str) -> Optional[dict]:
    """Fetch JSON from URL with error handling."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"⚠️  API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def get_markets() -> List[Market]:
    """Fetch active markets from Manifold Markets."""
    print("🔍 Fetching active markets...")
    url = f"{MANIFOLD_API}/markets?limit=1000&sort=volume24h&order=desc"
    
    data = fetch_json(url)
    if not data:
        return []
    
    markets = []
    now = int(time.time())
    
    for m in data:
        # Filter: binary markets, not resolved, with volume
        if m.get("type") != "BINARY_MARKET":
            continue
        if m.get("isResolved"):
            continue
        if m.get("volume24h", 0) < 100:  # Ignore low-volume markets
            continue
        
        market = Market(
            id=m.get("id", ""),
            title=m.get("question", "Unknown"),
            current_probability=m.get("probability", 0.5),
            volume_24h=m.get("volume24h", 0),
            created_at=int(m.get("createdTime", 0) / 1000),
            closes_at=int(m.get("closeTime", now + 86400 * 365) / 1000),
            is_resolved=m.get("isResolved", False),
            last_updated=now,
        )
        markets.append(market)
    
    print(f"✅ Loaded {len(markets)} active markets")
    return markets

def get_market_history(market_id: str) -> Optional[List[Dict]]:
    """Fetch recent probability history for a market."""
    url = f"{MANIFOLD_API}/market/{market_id}/history"
    data = fetch_json(url)
    return data if data else []

# ============================================================================
# Analysis Engine
# ============================================================================

def detect_mean_reversion(market: Market, history: List[Dict]) -> Optional[TradeSignal]:
    """
    Detect mean-reversion edge: crowd overreacts to news, probability swings
    beyond fair value, then reverts.
    
    Signal: If probability moved >10% in 24h, assume partial reversion incoming.
    Fair value estimate: weighted average of recent probabilities.
    """
    if not history or len(history) < 10:
        return None
    
    # Get recent history (last 24h)
    now = int(time.time())
    recent = [h for h in history if now - int(h.get("createdTime", 0) / 1000) < 86400]
    
    if len(recent) < 5:
        return None
    
    probs = [float(h.get("prob", 0.5)) for h in recent]
    
    # Calculate move
    prob_24h_ago = probs[0]
    current_prob = probs[-1]
    move = abs(current_prob - prob_24h_ago)
    
    if move < 0.10:  # No significant move
        return None
    
    # Fair value: weighted average (recent = more weight)
    weights = [i + 1 for i in range(len(probs))]
    fair_value = sum(p * w for p, w in zip(probs, weights)) / sum(weights)
    
    # Detect reversion: if current is far from fair, expect reversion
    edge = abs(current_prob - fair_value)
    
    if edge < 0.05:  # Too small
        return None
    
    # Suggest trade direction
    if current_prob > fair_value:
        side = "NO"  # Prob is high, bet it comes down
        confidence = min(0.8, edge * 2)
    else:
        side = "YES"
        confidence = min(0.8, edge * 2)
    
    return TradeSignal(
        market_id=market.id,
        market_title=market.title,
        current_prob=current_prob,
        edge_type="mean_reversion",
        estimated_fair_value=fair_value,
        edge_percent=edge * 100,
        suggested_side=side,
        confidence=confidence,
        rationale=f"Market moved {move*100:.1f}% in 24h. Fair value ≈ {fair_value:.2%}, current {current_prob:.2%}. Mean-reversion likely.",
    )

def detect_resolution_arbitrage(market: Market) -> Optional[TradeSignal]:
    """
    Detect resolution arbitrage: market resolves soon but probability hasn't
    converged to likely outcome.
    
    Signal: If <7 days to resolution and probability is near 50%, high uncertainty.
    If market is about a highly predictable outcome (e.g., past deadline), mispricing likely.
    """
    now = int(time.time())
    time_to_close = (market.closes_at - now) / 86400  # Days
    
    if time_to_close < 0:  # Already closed
        return None
    
    if time_to_close > 7:  # Not soon enough
        return None
    
    # If very close to 50-50, it's uncertain — but high volatility = opportunity
    if market.current_probability < 0.4 or market.current_probability > 0.6:
        # Probability is strong; assume market is pricing correctly
        return None
    
    # Near 50%, and imminent resolution = uncertain market = potential mispricing
    confidence = 0.5
    side = "YES" if market.current_probability < 0.5 else "NO"
    
    return TradeSignal(
        market_id=market.id,
        market_title=market.title,
        current_prob=market.current_probability,
        edge_type="resolution_arb",
        estimated_fair_value=0.5,  # Uncertainty model
        edge_percent=abs(0.5 - market.current_probability) * 100,
        suggested_side=side,
        confidence=confidence,
        rationale=f"Resolves in {time_to_close:.1f} days. Near 50-50 suggests unresolved outcome. High uncertainty = potential edge.",
    )

def analyze_markets(markets: List[Market]) -> List[TradeSignal]:
    """Analyze all markets for trading edges."""
    signals = []
    
    print("\n📊 Analyzing markets for edges...")
    for i, market in enumerate(markets[:50]):  # Analyze top 50 by volume
        # Fetch history
        history = get_market_history(market.id)
        
        # Check mean-reversion
        signal = detect_mean_reversion(market, history or [])
        if signal and signal.edge_percent > CONFIG["min_edge_threshold"] * 100:
            signals.append(signal)
            print(f"  ✨ {signal.edge_type}: {market.title[:60]}")
        
        # Check resolution arb
        signal = detect_resolution_arbitrage(market)
        if signal and signal.edge_percent > CONFIG["min_edge_threshold"] * 100:
            signals.append(signal)
            print(f"  ✨ {signal.edge_type}: {market.title[:60]}")
        
        # Rate limit: 1 request per market
        time.sleep(0.2)
    
    print(f"✅ Found {len(signals)} trading signals")
    return signals

# ============================================================================
# Portfolio & Execution
# ============================================================================

def load_portfolio() -> Dict:
    """Load portfolio from file, or initialize."""
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE) as f:
            return json.load(f)
    
    return {
        "capital": CONFIG["initial_capital"],
        "positions": [],
        "closed_positions": [],
        "total_pnl": 0.0,
        "created_at": int(time.time()),
    }

def save_portfolio(portfolio: Dict):
    """Save portfolio to file."""
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def position_size_kelly(edge: float, capital: float) -> float:
    """
    Kelly criterion position sizing.
    
    Kelly % = (win_prob * avg_win - loss_prob * avg_loss) / avg_win
    
    Simplified: for binary markets with symmetric payoff,
    Kelly% = 2 * edge (where edge is probability deviation)
    
    We use fractional Kelly for safety.
    """
    kelly_percent = 2 * edge
    kelly_fraction = CONFIG["kelly_fraction"]
    
    position = capital * kelly_percent * kelly_fraction
    position = min(position, CONFIG["max_position_size"])
    
    return max(position, 10)  # Minimum M$10

def execute_trade(signal: TradeSignal, portfolio: Dict) -> Optional[Position]:
    """Execute a paper trade."""
    available_capital = portfolio["capital"]
    
    # Position sizing
    edge = signal.edge_percent / 100
    size = position_size_kelly(edge, available_capital)
    
    if size > available_capital:
        print(f"⚠️  Insufficient capital for {signal.market_title} (need {size}, have {available_capital})")
        return None
    
    # Create position
    position = Position(
        market_id=signal.market_id,
        market_title=signal.market_title,
        side=signal.suggested_side,
        entry_prob=signal.current_prob,
        size=size,
        entry_time=int(time.time()),
        status="open",
    )
    
    # Deduct from capital
    portfolio["capital"] -= size
    portfolio["positions"].append(asdict(position))
    
    print(f"📈 TRADE: {signal.suggested_side} {position.market_title[:50]}")
    print(f"   Size: M${size:.0f} | Prob: {signal.current_prob:.2%} | Edge: {signal.edge_percent:.1f}%")
    print(f"   Rationale: {signal.rationale[:80]}...")
    
    return position

def evaluate_positions(portfolio: Dict, markets: Dict[str, Market]):
    """Evaluate open positions against current market prices."""
    closed = 0
    for pos in portfolio["positions"]:
        if pos["status"] != "open":
            continue
        
        market = markets.get(pos["market_id"])
        if not market:
            continue
        
        # Simple exit: if position is profitable by >2%, close it
        current_prob = market.current_probability
        
        if pos["side"] == "YES":
            current_pnl_pct = (current_prob - pos["entry_prob"]) / pos["entry_prob"]
        else:
            current_pnl_pct = (pos["entry_prob"] - current_prob) / pos["entry_prob"]
        
        current_pnl = pos["size"] * current_pnl_pct
        
        # Exit if profitable or 3% underwater (stop loss)
        if current_pnl > pos["size"] * 0.02 or current_pnl < -pos["size"] * 0.03:
            pos["status"] = "closed"
            pos["exit_prob"] = current_prob
            pos["exit_time"] = int(time.time())
            pos["pnl"] = current_pnl
            
            portfolio["total_pnl"] += current_pnl
            portfolio["closed_positions"].append(pos)
            portfolio["positions"].remove(pos)
            portfolio["capital"] += pos["size"] + current_pnl
            
            result = "✅ WIN" if current_pnl > 0 else "❌ LOSS"
            print(f"{result}: {pos['market_title'][:40]} | P&L: M${current_pnl:+.1f}")
            
            closed += 1
    
    return closed

def log_decision(signal: TradeSignal, executed: bool):
    """Log trade decision to JSONL history."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "market_id": signal.market_id,
        "market_title": signal.market_title,
        "edge_type": signal.edge_type,
        "edge_percent": signal.edge_percent,
        "suggested_side": signal.suggested_side,
        "confidence": signal.confidence,
        "executed": executed,
        "rationale": signal.rationale,
    }
    
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ============================================================================
# Main Loop
# ============================================================================

def run_once():
    """Run one iteration of the bot."""
    print(f"\n{'='*70}")
    print(f"🤖 Prediction Markets Bot — {datetime.now().isoformat()}")
    print(f"{'='*70}")
    
    # Load state
    portfolio = load_portfolio()
    print(f"💰 Capital: M${portfolio['capital']:.0f} | Total P&L: M${portfolio['total_pnl']:+.1f}")
    
    # Fetch markets
    markets_list = get_markets()
    if not markets_list:
        print("❌ No markets fetched. Exiting.")
        return
    
    markets_dict = {m.id: m for m in markets_list}
    
    # Evaluate existing positions
    closed = evaluate_positions(portfolio, markets_dict)
    if closed > 0:
        print(f"📊 Closed {closed} positions")
    
    # Analyze for edges
    signals = analyze_markets(markets_list)
    
    # Execute trades
    executed = 0
    for signal in signals[:3]:  # Max 3 trades per run
        if signal.confidence < 0.5:
            log_decision(signal, False)
            print(f"⏭️  Skipped {signal.market_title[:40]} (low confidence)")
            continue
        
        if portfolio["capital"] < 100:
            print(f"⚠️  Insufficient capital to trade")
            break
        
        position = execute_trade(signal, portfolio)
        if position:
            executed += 1
            log_decision(signal, True)
    
    if executed == 0:
        print("⏭️  No trades executed this round")
    
    # Save state
    save_portfolio(portfolio)
    
    print(f"\n📊 Portfolio Summary")
    print(f"   Open positions: {len(portfolio['positions'])}")
    print(f"   Closed positions: {len(portfolio['closed_positions'])}")
    print(f"   Capital: M${portfolio['capital']:.0f}")
    print(f"   Total P&L: M${portfolio['total_pnl']:+.1f}")

def run_demo():
    """Run demo with example data (no API calls)."""
    print("\n🎬 Running DEMO mode (no API calls)")
    print("   This creates synthetic markets for testing the analysis engine.\n")
    
    # Create synthetic markets
    markets = [
        Market(
            id="demo-1",
            title="Will ChatGPT-5 be released by end of 2026?",
            current_probability=0.65,
            volume_24h=50000,
            created_at=int(time.time()) - 2592000,
            closes_at=int(time.time()) + 10886400,
            is_resolved=False,
        ),
        Market(
            id="demo-2",
            title="Biden re-elected 2028?",
            current_probability=0.42,
            volume_24h=100000,
            created_at=int(time.time()) - 86400 * 100,
            closes_at=int(time.time()) + 86400 * 3,  # Closes in 3 days
            is_resolved=False,
        ),
    ]
    
    markets_dict = {m.id: m for m in markets}
    
    portfolio = load_portfolio()
    print(f"💰 Starting capital: M${portfolio['capital']:.0f}\n")
    
    # Simulate trades
    for market in markets:
        signal = detect_resolution_arbitrage(market)
        if signal:
            print(f"Found edge: {signal.edge_type}")
            print(f"   Market: {signal.market_title}")
            print(f"   Current prob: {signal.current_prob:.2%}")
            print(f"   Edge: {signal.edge_percent:.1f}%")
            print(f"   Rationale: {signal.rationale}\n")
            
            position = execute_trade(signal, portfolio)
            log_decision(signal, True)
    
    save_portfolio(portfolio)
    
    # Show summary
    print(f"\n📊 Demo Summary")
    print(f"   Positions: {len(portfolio['positions'])}")
    print(f"   Capital remaining: M${portfolio['capital']:.0f}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "once"
    
    if mode == "demo":
        run_demo()
    else:
        run_once()
    
    print(f"\n✅ Done. Logs saved to {HISTORY_FILE}")
    print(f"📁 Portfolio saved to {PORTFOLIO_FILE}")

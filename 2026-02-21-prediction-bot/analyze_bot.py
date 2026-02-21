#!/usr/bin/env python3
"""
Bot Performance Analyzer
Reads bot_history.jsonl and portfolio.json, generates insights.
"""

import json
from pathlib import Path
from collections import defaultdict

HISTORY_FILE = Path(__file__).parent / "bot_history.jsonl"
PORTFOLIO_FILE = Path(__file__).parent / "portfolio.json"

def analyze():
    print("\n" + "="*70)
    print("📊 Prediction Bot Performance Analysis")
    print("="*70 + "\n")
    
    # Load portfolio
    if not PORTFOLIO_FILE.exists():
        print("❌ No portfolio.json found. Run the bot first!")
        return
    
    with open(PORTFOLIO_FILE) as f:
        portfolio = json.load(f)
    
    # Summary
    print("💰 PORTFOLIO SUMMARY")
    print(f"   Current capital: M${portfolio['capital']:.0f}")
    print(f"   Total P&L: M${portfolio['total_pnl']:+.2f}")
    print(f"   Open positions: {len(portfolio['positions'])}")
    print(f"   Closed positions: {len(portfolio['closed_positions'])}")
    
    if portfolio['closed_positions']:
        closed = portfolio['closed_positions']
        wins = [p for p in closed if p.get('pnl', 0) > 0]
        losses = [p for p in closed if p.get('pnl', 0) <= 0]
        
        win_rate = len(wins) / len(closed) * 100
        total_win = sum(p.get('pnl', 0) for p in wins)
        total_loss = sum(p.get('pnl', 0) for p in losses)
        
        print(f"\n🎯 CLOSED POSITIONS")
        print(f"   Total: {len(closed)}")
        print(f"   Wins: {len(wins)} ({win_rate:.1f}%)")
        print(f"   Losses: {len(losses)}")
        print(f"   Total profit: M${total_win:+.2f}")
        print(f"   Total loss: M${total_loss:+.2f}")
        
        if closed:
            avg_pnl = sum(p.get('pnl', 0) for p in closed) / len(closed)
            print(f"   Avg P&L per trade: M${avg_pnl:+.2f}")
    
    # Open positions
    if portfolio['positions']:
        print(f"\n📈 OPEN POSITIONS ({len(portfolio['positions'])})")
        for i, pos in enumerate(portfolio['positions'], 1):
            print(f"\n   {i}. {pos['market_title'][:60]}")
            print(f"      Side: {pos['side']} | Entry: {pos['entry_prob']:.2%} | Size: M${pos['size']:.0f}")
    
    # Decision history
    if HISTORY_FILE.exists():
        print(f"\n📋 DECISION HISTORY")
        
        decisions = []
        with open(HISTORY_FILE) as f:
            for line in f:
                try:
                    decisions.append(json.loads(line))
                except:
                    pass
        
        if decisions:
            executed = sum(1 for d in decisions if d.get('executed'))
            skipped = len(decisions) - executed
            
            edge_types = defaultdict(int)
            for d in decisions:
                edge_types[d.get('edge_type', 'unknown')] += 1
            
            print(f"   Total decisions: {len(decisions)}")
            print(f"   Executed: {executed}")
            print(f"   Skipped: {skipped}")
            print(f"\n   By edge type:")
            for edge_type, count in sorted(edge_types.items(), key=lambda x: -x[1]):
                pct = count / len(decisions) * 100
                print(f"      {edge_type}: {count} ({pct:.0f}%)")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    analyze()

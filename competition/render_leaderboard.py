"""
Render leaderboard.md from leaderboard.csv
"""

import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard" / "leaderboard.md"


def read_rows():
    """Read rows from leaderboard CSV."""
    if not CSV_PATH.exists():
        return []
    
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if (r.get("team") or "").strip()]
    
    return rows


def main():
    """Generate leaderboard markdown from CSV."""
    rows = read_rows()
    
    # Sort by RMSE ascending (lower is better)
    def score_key(r):
        try:
            return float(r.get("rmse", "inf"))
        except:
            return float("inf")
    
    def ts_key(r):
        try:
            return datetime.fromisoformat(r.get("timestamp_utc", "").replace("Z", "+00:00"))
        except:
            return datetime.fromtimestamp(0)
    
    rows.sort(key=lambda r: (score_key(r), -ts_key(r).timestamp()))
    
    # Render markdown
    lines = []
    lines.append("# CardioGraph Leaderboard\n\n")
    lines.append("This leaderboard is **auto-updated** when a submission PR is opened. ")
    lines.append("For interactive view, enable GitHub Pages and open **/docs/leaderboard.html**.\n\n")
    lines.append("**Metric**: RMSE (Root Mean Squared Error) - **lower is better**\n\n")
    lines.append("**Policy**: Only ONE submission per team allowed.\n\n")
    
    lines.append("| Rank | Team | Model | RMSE (ms) | MAE (ms) | Within ±10ms | Date (UTC) | Notes |\n")
    lines.append("|-----:|------|-------|----------:|---------:|-------------:|------------|-------|\n")
    
    for i, r in enumerate(rows, start=1):
        team = (r.get("team") or "").strip()
        model = (r.get("model") or "").strip()
        rmse = (r.get("rmse") or "").strip()
        mae = (r.get("mae") or "-").strip()
        tolerance = (r.get("within_tolerance_10ms") or "-").strip()
        ts = (r.get("timestamp_utc") or "").strip()
        notes = (r.get("notes") or "").strip()
        
        # Format model as code
        model_disp = f"`{model}`" if model else "-"
        
        # Format numbers
        try:
            rmse = f"{float(rmse):.2f}"
        except:
            pass
        
        try:
            mae = f"{float(mae):.2f}"
        except:
            mae = "-"
        
        try:
            tolerance = f"{float(tolerance):.1f}%"
        except:
            tolerance = "-"
        
        lines.append(f"| {i} | {team} | {model_disp} | {rmse} | {mae} | {tolerance} | {ts} | {notes} |\n")
    
    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Rendered {len(rows)} entries to leaderboard.md")


if __name__ == "__main__":
    main()
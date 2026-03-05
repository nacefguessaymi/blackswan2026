from blackswan2026.backtest import run

results = run(start="2002-10-01", end="2003-03-20")

for key, value in results.items():
    print(f"{key}: {value}\n")

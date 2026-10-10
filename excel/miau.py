import pandas as pd
from pathlib import Path

datei = Path(__file__).parent / "Gesamt_bereinigt.csv"

df = pd.read_csv(
    datei,
    sep=";",
    encoding="cp1252"
)

print(df)
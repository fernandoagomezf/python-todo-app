
from decimal import Decimal

principal = Decimal("1000.0")
rate = Decimal("0.05")

for year in range(11):
    amount = principal * (1 + rate) ** year
    print(f"{year:>2}{amount:>10.2f}")



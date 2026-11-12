# Python Bank Account System

An educational object-oriented account simulation with decimal balances, withdrawals, transfers, savings fees and a 5% deposit reward.

```python
from bank_account import BankAccount, SavingsAccount
sender = SavingsAccount(100, "Sender")
recipient = BankAccount(0, "Recipient")
sender.transfer(90, recipient)
assert sender.balance == 5  # 90 transfer plus 5 withdrawal fee
assert recipient.balance == 90
```

## Design

Amounts are finite, positive Decimal values rounded half-up to cents. Failed transfers leave both balances unchanged; the savings fee is validated before debiting. Original class aliases remain available. Transaction errors now raise exceptions so callers can reliably handle failure.

Run `python -m unittest discover -s tests -v` (Python 3.11+; no third-party dependencies). Tests cover negative/non-finite inputs, failed transfers, fees, rewards and decimal arithmetic.

This is a learning simulation, not banking software: no authentication, persistence, concurrent transaction protection or regulatory implementation. Deposit rewards are a deliberately simplified exercise, not real interest accounting.

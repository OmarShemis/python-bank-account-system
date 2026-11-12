"""Educational account simulation with validated decimal transactions."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

class BalanceException(ValueError):
    """A debit would exceed available funds."""

def money(value, *, allow_zero=False):
    try:
        result=Decimal(str(value))
        if not result.is_finite() or result < 0 or (not allow_zero and result == 0) or result > Decimal("1e15"):
            raise ValueError("Amount must be positive, finite, and at most 1e15.")
        result=result.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        if not allow_zero and result == 0:
            raise ValueError("Amount rounds to zero.")
        return result
    except InvalidOperation as error:
        raise ValueError("Invalid monetary amount.") from error

class BankAccount:
    def __init__(self, initial_amount, account_name):
        if not account_name.strip():
            raise ValueError("Account name is required.")
        self.balance=money(initial_amount,allow_zero=True)
        self.name=account_name.strip()

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += self.credit_amount(money(amount))
        return self.balance

    def credit_amount(self, amount):
        return amount

    def debit_amount(self, amount):
        return amount

    def viable_transaction(self, amount):
        debit=self.debit_amount(money(amount))
        if debit > self.balance:
            raise BalanceException("Insufficient funds, including any withdrawal fee.")
        return debit

    def withdraw(self, amount):
        debit=self.viable_transaction(amount)
        self.balance -= debit
        return self.balance

    def transfer(self, amount, account):
        if not isinstance(account,BankAccount) or account is self:
            raise ValueError("Choose a different valid destination account.")
        amount=money(amount)
        debit=self.viable_transaction(amount)
        credit=account.credit_amount(amount)
        # Compute all fallible values before either balance changes.
        sender_balance=self.balance-debit
        recipient_balance=account.balance+credit
        self.balance,account.balance=sender_balance,recipient_balance

    # Original tutorial-style names retained for existing callers.
    getBalance=get_balance
    viableTransaction=viable_transaction

class InterestRewardsAccount(BankAccount):
    def credit_amount(self,amount):
        return (amount*Decimal("1.05")).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

class SavingsAccount(InterestRewardsAccount):
    fee=Decimal("5.00")
    def debit_amount(self,amount):
        return amount+self.fee

InterestRewardsAcct=InterestRewardsAccount
SavingsAcct=SavingsAccount

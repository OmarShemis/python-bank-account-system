class BalanceException(Exception):
    pass

class BankAccount:
    def __init__ (self, initialAmount, acctName):
        self.balance = initialAmount
        self.name = acctName
        print(f"\nAccount '{self.name}' created.\nBalance = ${self.balance:.2f}")

    def getBalance(self):
        print(f"\nAccount '{self.name}' balance is ${self.balance:.2f}")

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"\nDeposit Complete, you have deposited {amount} and your current balance is ${self.balance}")

    def viableTransaction(self, amount):
        if self.balance >= amount:
            return
        else:
            raise BalanceException(f"\nSorry account '{self.name}' only has a balance of {self.balance:.2f}")

    def withdraw(self, amount):
        try:
            self.viableTransaction(amount)
            self.balance = self.balance - amount
            print("\nWithdraw Complete ✅")
            self.getBalance()
        except BalanceException as error:
            print(f"Withdraw interrupted: ❌ {error}")

    def transfer(self, amount, account):
        try:
            print("\n*********\n\nBeginning Transfer......🚀")
            self.viableTransaction(amount)
            self.withdraw(amount)
            account.deposit(amount)
            print("\nTransfer Complete! ✅")
        except BalanceException as error:
            print(f"\nTransfer Interrupted: ❌ {error}")

class InterestRewardsAcct(BankAccount):
    def deposit(self, amount):
        self.balance = self.balance + (amount * 1.05) #interest rate of 5%
        print("\nDeposit Complete ✅")
        self.getBalance()

class SavingsAcct(InterestRewardsAcct):
    def __init__(self, initialAmount, acctName):
        super().__init__(initialAmount, acctName)
        self.fee = 5

    def withdraw(self, amount):
        try:
            self.viableTransaction(amount + self.fee)
            self.balance = self.balance - (amount + self.fee)
            print("\nWithdraw Complete ✅")
            self.getBalance()
        except BalanceException as error:
            print(f"Withdraw interrupted: ❌ {error}")
import unittest
from decimal import Decimal
from bank_account import BankAccount,SavingsAccount,InterestRewardsAccount,BalanceException

class AccountsTests(unittest.TestCase):
    def test_failed_transfer_preserves_both_balances(self):
        sender= SavingsAccount(100,"sender"); recipient=BankAccount(0,"recipient")
        with self.assertRaises(BalanceException): sender.transfer(98,recipient)
        self.assertEqual((sender.balance,recipient.balance),(Decimal("100"),Decimal("0")))
    def test_transfer_fee_and_credit(self):
        sender=SavingsAccount(100,"sender"); recipient=BankAccount(0,"recipient")
        sender.transfer(90,recipient)
        self.assertEqual((sender.balance,recipient.balance),(Decimal("5"),Decimal("90")))
    def test_invalid_amounts_do_not_mutate(self):
        for amount in [-10,0,"NaN","Infinity","bad"]:
            account=BankAccount(100,"account")
            for action in [account.withdraw,account.deposit]:
                with self.assertRaises(ValueError): action(amount)
                self.assertEqual(account.balance,100)
    def test_decimal_and_reward(self):
        account=BankAccount("0.10","account");account.deposit("0.20")
        self.assertEqual(account.balance,Decimal("0.30"))
        reward=InterestRewardsAccount(0,"reward");reward.deposit(100)
        self.assertEqual(reward.balance,105)
    def test_self_transfer_rejected(self):
        account=BankAccount(100,"account")
        with self.assertRaises(ValueError): account.transfer(10,account)

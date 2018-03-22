import unittest
import blockchain
from blockchain.util import sha256_2_string
from blockchain.pow_block import PoWBlock
from blockchain.transaction import Transaction, TransactionOutput

class TestBlock(PoWBlock):
    """ We want to test PoW blocks without mining, so override seal check """

    def seal_is_valid(self):
        return True

    def calculate_appropriate_target(self):
        return int(2 ** 256)


class ValidityTest(unittest.TestCase):

    def setUp(self):
        self.test_chain = blockchain.Blockchain()
        self.old_chain = blockchain.chain # PoW chains need to look up difficulty in the db, so shadow the global DB blockchain w our test chain
        blockchain.chain = self.test_chain

    def tearDown(self):
        blockchain.chain = self.old_chain # restore original chain


    def test_valid_merkle_empty(self):
        block = TestBlock(0, [], "genesis", is_genesis=True)
        expected_value = sha256_2_string("")
        self.assertEqual(block.calculate_merkle_root(), expected_value)

    def test_valid_merkle_one_leaf(self):

        tx1 = Transaction([], [TransactionOutput("Alice", "Bob", 1), TransactionOutput("Alice", "Alice", 1)])
        transactions = [tx1]
        block = TestBlock(0, transactions, "genesis", is_genesis=True)
        expected_value = sha256_2_string(str(tx1))
        self.assertEqual(block.calculate_merkle_root(), expected_value)

    def test_valid_merkle_three_leafs(self):
        tx1 = Transaction([], [TransactionOutput("Alice", "Bob", 1), TransactionOutput("Alice", "Alice", 1)])
        tx2 = Transaction([tx1.hash + ":1"],
                          [TransactionOutput("Alice", "Bob", .9), TransactionOutput("Alice", "Carol", 0)])
        tx3 = Transaction([tx2.hash + ":0"], [TransactionOutput("Bob", "Bob", .8)])
        transactions = [tx1, tx2, tx3]
        block = TestBlock(0, transactions, "genesis", is_genesis=True)
        expected_value = sha256_2_string(sha256_2_string(str(tx1)) + sha256_2_string(str(tx2)))
        expected_value = sha256_2_string(expected_value + sha256_2_string(str(tx3)))
        self.assertEqual(block.calculate_merkle_root(), expected_value)
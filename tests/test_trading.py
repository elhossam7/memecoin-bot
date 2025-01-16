import unittest
from src.core.trading.arbitrage import Arbitrage
from src.core.trading.order_types import OrderTypes

class TestTrading(unittest.TestCase):

    def setUp(self):
        self.arbitrage = Arbitrage()
        self.order_types = OrderTypes()

    def test_basic_arbitrage(self):
        # Test basic arbitrage functionality
        result = self.arbitrage.execute_trade('MemeCoinA', 'MemeCoinB', 1.0)
        self.assertTrue(result['success'])
        self.assertIn('trade_id', result)

    def test_order_types(self):
        # Test different order types
        market_order = self.order_types.create_order('market', 'MemeCoinA', 10)
        self.assertEqual(market_order['type'], 'market')
        self.assertEqual(market_order['amount'], 10)

        limit_order = self.order_types.create_order('limit', 'MemeCoinB', 5, price=0.01)
        self.assertEqual(limit_order['type'], 'limit')
        self.assertEqual(limit_order['amount'], 5)
        self.assertEqual(limit_order['price'], 0.01)

    def test_sniping_functionality(self):
        # Test sniping functionality
        result = self.arbitrage.sniper('MemeCoinC')
        self.assertTrue(result['success'])
        self.assertIn('sniped_coin', result)

if __name__ == '__main__':
    unittest.main()
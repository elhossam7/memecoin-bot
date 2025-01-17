def test_balance_tracking():
    # Test the balance tracking functionality
    portfolio = Portfolio()
    portfolio.update_balance(100)
    assert portfolio.get_balance() == 100
    portfolio.update_balance(50)
    assert portfolio.get_balance() == 50
    pass

def test_performance_analysis():
    def test_performance_analysis():
        # Test the performance analysis functionality
        portfolio = Portfolio()
        portfolio.update_balance(1000)  # Initial balance
        
        # Simulate some trades
        portfolio.update_balance(1200)  # Gain
        assert portfolio.calculate_returns() == 0.2  # 20% return
        
        portfolio.update_balance(900)  # Loss
        assert portfolio.calculate_returns() == -0.1  # -10% return from initial
        
        # Test peak value tracking
        assert portfolio.get_peak_value() == 1200
        
        # Test drawdown calculation
        assert portfolio.calculate_max_drawdown() == 0.25  # 25% drawdown from peak
        
        # Test period returns
        portfolio.record_daily_return(0.05)  # 5% daily return
        portfolio.record_daily_return(-0.03)  # -3% daily return
        assert len(portfolio.get_daily_returns()) == 2
        assert abs(portfolio.get_average_daily_return() - 0.01) < 0.0001  # Average ~1%
    pass

def test_token_tracking():
    # Test the token tracking functionality
    portfolio = Portfolio()
    
    # Test adding new tokens
    portfolio.add_token("BTC", 1.5)
    assert "BTC" in portfolio.get_tokens()
    assert portfolio.get_token_balance("BTC") == 1.5
    
    # Test updating token amounts
    portfolio.update_token_balance("BTC", 2.0)
    assert portfolio.get_token_balance("BTC") == 2.0
    
    # Test multiple tokens
    portfolio.add_token("ETH", 10)
    assert len(portfolio.get_tokens()) == 2
    
    # Test removing tokens
    portfolio.remove_token("BTC")
    assert "BTC" not in portfolio.get_tokens()
    assert len(portfolio.get_tokens()) == 1
    
    # Test token value tracking
    portfolio.set_token_price("ETH", 2000)
    assert portfolio.get_token_value("ETH") == 20000  # 10 ETH * $2000
    
    # Test invalid operations
    with pytest.raises(ValueError):
        portfolio.get_token_balance("INVALID")
    pass
def test_price_alerts():
    # Test the functionality of price alerts
    def test_price_alerts():
        # Test alert for price above threshold
        assert price_alert(current_price=1000, threshold=900, direction="above")
        
        # Test alert for price below threshold  
        assert price_alert(current_price=800, threshold=900, direction="below")
        
        # Test no alert when threshold not met
        assert not price_alert(current_price=850, threshold=900, direction="above")
        
        # Test invalid direction parameter
        with pytest.raises(ValueError):
            price_alert(current_price=1000, threshold=900, direction="invalid")
            
        # Test with zero and negative values
        assert price_alert(current_price=0, threshold=-100, direction="above")
        assert price_alert(current_price=-200, threshold=-100, direction="below")


def test_trend_alerts():
    # Test the functionality of trend alerts
    # Test upward trend alert
    assert trend_alert(prices=[100, 110, 120], direction="up")
    
"""
Example usage of Futu OpenAPI trading functions.
"""

from scripts.futu_client import FutuClient
from scripts.trading import TradingManager
from scripts.market_data import MarketData
from futu import TrdSide, OrderType


def example_buy_stock():
    """Example: Buy a stock"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Place a limit buy order for Tencent
        result = trading.place_order(
            code="HK.00700",
            price=380.0,
            quantity=100,
            side=TrdSide.BUY,
            order_type=OrderType.NORMAL
        )
        print(f"Order placed: {result}")


def example_sell_stock():
    """Example: Sell a stock"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Place a market sell order
        result = trading.place_order(
            code="HK.00700",
            price=0,  # 0 for market order
            quantity=100,
            side=TrdSide.SELL,
            order_type=OrderType.MARKET
        )
        print(f"Order placed: {result}")


def example_check_positions():
    """Example: Check current positions"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Get all positions
        positions = trading.get_positions()
        print(f"Current positions: {len(positions)}")

        for pos in positions:
            print(f"  {pos['code']}: {pos['qty']} shares @ avg ${pos.get('cost_price', 'N/A')}")

        # Get specific position
        tencent_pos = trading.get_position("HK.00700")
        if tencent_pos:
            print(f"Tencent position: {tencent_pos['qty']} shares")


def example_check_orders():
    """Example: Check order status"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Get all today's orders
        orders = trading.get_today_orders()
        print(f"Today's orders: {len(orders)}")

        # Get pending orders
        pending = trading.get_pending_orders()
        print(f"Pending orders: {len(pending)}")

        # Get filled orders
        filled = trading.get_filled_orders()
        print(f"Filled orders: {len(filled)}")


def example_cancel_orders():
    """Example: Cancel orders"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Cancel specific order
        # result = trading.cancel_order(order_id="123456789")

        # Cancel all pending orders
        results = trading.cancel_all_orders()
        print(f"Cancelled {len(results)} orders")


def example_get_quotes():
    """Example: Get market quotes"""
    with FutuClient() as client:
        market = MarketData(client)

        # Subscribe to stocks
        market.subscribe(["HK.00700", "US.AAPL"])

        # Get quotes
        quotes = market.get_quote(["HK.00700", "US.AAPL"])

        for quote in quotes:
            print(f"{quote['code']}: ${quote['last_price']} (Change: {quote.get('change_rate', 'N/A')}%)")


def example_get_klines():
    """Example: Get K-line data"""
    with FutuClient() as client:
        market = MarketData(client)

        # Get daily K-lines for Tencent
        klines = market.get_klines(
            code="HK.00700",
            period="DAY",
            count=30
        )

        print(f"Got {len(klines)} daily candles")

        if klines:
            latest = klines[-1]
            print(f"Latest: Open=${latest['open']}, High=${latest['high']}, Low=${latest['low']}, Close=${latest['close']}")


def example_account_info():
    """Example: Get account information"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Get account info
        account = trading.get_account_info()
        print(f"Cash: ${account.get('cash', 'N/A')}")
        print(f"Total Assets: ${account.get('total_assets', 'N/A')}")
        print(f"Market Value: ${account.get('market_val', 'N/A')}")


def example_max_tradable():
    """Example: Get maximum tradable quantity"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        max_qty = trading.get_max_trd_qtys(code="HK.00700", price=380.0)
        print(f"Max buy quantity: {max_qty.get('max_cash_buy', 'N/A')}")
        print(f"Max sell quantity: {max_qty.get('max_sell', 'N/A')}")


if __name__ == "__main__":
    # Run examples (make sure FutuOpenD is running)
    print("Running Futu OpenAPI examples...")

    # Uncomment the examples you want to run:
    # example_get_quotes()
    # example_get_klines()
    # example_check_positions()
    # example_account_info()
    # example_check_orders()
    # example_buy_stock()
    # example_sell_stock()
    # example_cancel_orders()
    # example_max_tradable()

    print("Examples completed.")

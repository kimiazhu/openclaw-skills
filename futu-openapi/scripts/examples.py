"""
Example usage of Futu OpenAPI trading functions.
"""

from scripts.futu_client import FutuClient
from scripts.trading import TradingManager
from scripts.market_data import MarketData
from futu import TrdSide, OrderType
from futu import OpenQuoteContext, OpenSecTradeContext, TrdEnv, RET_OK


def example_buy_stock():
    """Example: Buy a stock"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

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
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

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
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

        # Get all positions
        ok, positions = trading.get_trade_ctx().position_list_query(trd_env=TrdEnv.SIMULATE, acc_id=acc_id)
        if ok == RET_OK:
            print(f"Current positions: {len(positions)}")
            for _, pos in positions.iterrows():
                print(f"  {pos['code']}: {pos['qty']} shares @ avg ${pos.get('cost_price', 'N/A')}")
        else:
            print(f"Failed to get positions: {positions}")

        # Get specific position
        ok, tencent_pos = trading.get_trade_ctx().position_list_query(code="HK.00700", trd_env=TrdEnv.SIMULATE, acc_id=acc_id)
        if ok == RET_OK and not tencent_pos.empty:
            print(f"Tencent position: {tencent_pos.iloc[0]['qty']} shares")


def example_check_orders():
    """Example: Check order status"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

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
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

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


def general_example():
    """Example: Get account information"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK")

        # Get account info
        account = trading.get_account_info()
        acc_id = account.get('acc_id', 'N/A')
        print(f"Account ID: {acc_id}")
        ok, assets = trading.get_trade_ctx().accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=acc_id)
        if ok == RET_OK:
            print(f"模拟账户可用资金:{assets.iloc[0]['cash']}")
            print(f"模拟账户最大购买力:{assets.iloc[0]['power']}")

            ok, positions = trading.get_trade_ctx().position_list_query(trd_env=TrdEnv.SIMULATE, acc_id=acc_id)
            if ok == RET_OK:
                if positions.empty:
                    print(f"账户 {acc_id} 目前没有持仓。")
                else:
                    print(f"--- 账户 {acc_id} 持仓详情 ---")
                    cols = ['code', 'stock_name', 'qty', 'can_sell_qty', 'cost_price', 'nominal_price', 'pl_val', 'pl_ratio']
                    display_data = positions[cols]
                    print(display_data)


def example_max_tradable():
    """Example: Get maximum tradable quantity"""
    with FutuClient() as client:
        trading = TradingManager(client, market="HK", trd_env=TrdEnv.SIMULATE)

        # Get account info first
        account = trading.get_account_info(account_type=TrdEnv.SIMULATE)
        acc_id = account.get('acc_id', 'N/A')
        print(f"Using account: {acc_id} (SIMULATE)")

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
    general_example()
    # example_check_orders()
    # example_buy_stock()
    # example_sell_stock()
    # example_cancel_orders()
    # example_max_tradable()

    print("Examples completed.")

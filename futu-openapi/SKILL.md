---
name: futu-openapi
description: This skill enables automated stock trading through Futu Open API. It provides capabilities to buy/sell stocks, query positions, check order status, and retrieve market data. This skill should be used when users need to programmatically trade Hong Kong stocks, US stocks, or A-shares through Futu securities.
---

# Futu OpenAPI Trading

## Overview

This skill provides programmatic access to Futu OpenAPI for automated stock trading. It supports:
- Placing buy/sell orders (market and limit orders)
- Querying account positions and balances
- Checking order status and history
- Retrieving real-time market data and K-line data
- Cancelling pending orders

## Prerequisites

Before using this skill, ensure you have:
1. A Futu securities account with OpenAPI access enabled
2. FutuOpenD software installed and running
3. Python 3.7+ with `futu-api` package installed (`pip install futu-api`)
4. API connection configuration (host, port, unlock password if needed)

## Core Capabilities

### 1. Connect to Futu API

Establish connection to FutuOpenD:

```python
from scripts.futu_client import FutuClient

# Initialize client
client = FutuClient(host="127.0.0.1", port=11111)

# Connect to trading server
trader = client.get_trade_ctx()

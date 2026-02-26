#!/bin/bash
# Get a fee quote from NanoStack
# Usage: ./get_quote.sh [chain_id] [amount] [destination]

CHAIN_ID=${1:-8453}  # Base by default
AMOUNT=${2:-"1000000000000000000"}  # 1 ETH in wei
DEST=${3:-"0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"}

echo "Requesting quote: chain=$CHAIN_ID amount=$AMOUNT"

curl -s -X POST https://api.nano-labs.io/v1/quote \
  -H "Content-Type: application/json" \
  -d "{\"chain_id\": $CHAIN_ID, \"amount\": \"$AMOUNT\", \"destination\": \"$DEST\"}" \
  | python3 -m json.tool

echo ""
echo "Chain IDs: ETH=1, Base=8453, ARB=42161, OP=10, SOL=501, BTC=0"

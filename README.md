# NanoStack API

Permissionless cross-chain execution across 59 chains. 8-15 bps fees. Real-time signal data with cryptographic proofs.

**Base URL:** `https://api.nano-labs.io`

## Quick Start

Get a fee quote on any chain:

```bash
curl -X POST https://api.nano-labs.io/v1/quote \
  -H "Content-Type: application/json" \
  -d '{"chain_id": 8453, "amount": "1000000", "destination": "0xYourAddress"}'
```

Get real-time signal data:

```bash
curl https://api.nano-labs.io/v1/signal/atoms?n=10
```

No API key required. No registration. Fully permissionless.

## Endpoints

### Execution

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/quote` | Fee quote for any chain. 8-15 bps tiered. 30s validity. |
| POST | `/v1/execute` | Execute on any chain. Fee deducted from amount. |
| POST | `/v1/cross-chain` | Cross-chain execution (permissionless) |
| POST | `/v1/register` | Self-service API key (optional, for attribution) |

### Signal Data

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/signal/atoms?n=50` | Latest N signal atoms — real-time price deviations, entropy scores |
| GET | `/v1/signal/summary?n=1000` | Aggregate stats: mean/median/p95 deviation, chain coverage |
| GET | `/v1/signal/root` | Rolling BLAKE3 Merkle root of all signal atoms |

### Bot Integration

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/bots/schema` | Full typed schema — every field with type, format, constraints |
| GET | `/v1/bots/ecosystems` | 6 ecosystem configs with chain lists, address formats, gas models |
| GET | `/v1/bots/pairs` | 50 tradeable pairs across all ecosystems |
| GET | `/v1/bots/signals` | Signal endpoint discovery map |
| GET | `/v1/bots/capabilities` | Protocol capabilities |

### Discovery

| Method | Path | Description |
|--------|------|-------------|
| GET | `/.well-known/openapi.json` | OpenAPI 3.0 specification |
| GET | `/.well-known/nanoport.json` | Protocol discovery document |
| GET | `/.well-known/ai-plugin.json` | AI/LLM plugin manifest |
| GET | `/apis.json` | API directory manifest |

## Supported Chains (59)

### EVM (40 chains)

Ethereum (1), Base (8453), Arbitrum (42161), Optimism (10), Polygon (137), BNB Chain (56), Avalanche (43114), Scroll (534352), zkSync Era (324), Linea (59144), Blast (81457), Mantle (5000), Mode (34443), Taiko (167000), Manta Pacific (169), Fraxtal (252), Ink (57073), Zora (7777777), Unichain (130), World Chain (480), Xai (660279), X Layer (196), Gnosis (100), Fantom (250), Sei (1329), Celo (42220), Cronos (25), Moonbeam (1284), Astar (592), Aurora (1313161554), Kava (2222), Metis (1088), Boba (288), Harmony (1666600000), Degen (666666666), Filecoin (314), Hedera (295), Ronin (2020), Arbitrum Nova (42170), Polygon zkEVM (1101)

### Non-EVM (19 chains)

Bitcoin (UTXO), Solana, Cosmos Hub, Aptos (Move), Sui (Move), NEAR, TON, Cardano, Polkadot, Algorand, Axelar, Flow, ICP, TRON, Stellar, Tezos, XRP Ledger

### Sovereign

SubZero 2477 — conservation-enforced settlement chain

## Signal Atom Schema

Each signal atom is a 64-byte cache-line-aligned binary structure:

```json
{
  "hash": {"type": "string", "format": "hex", "length": 64, "description": "BLAKE3 commitment"},
  "seq": {"type": "u64", "description": "monotonic sequence number"},
  "ecosystem": {"type": "u16", "enum": {"0": "evm", "1": "solana", "2": "cosmos", "3": "utxo", "4": "xrpl", "5": "move"}},
  "tier": {"type": "u16", "description": "signal tier"},
  "pair": {"type": "u16", "resolve": "/v1/bots/pairs"},
  "flags": {"type": "u16", "description": "bitfield"},
  "deviation_bps": {"type": "i32", "description": "signed basis points from reference price"},
  "entropy_score": {"type": "u32", "description": "full u32 range"},
  "venue": {"type": "string", "description": "source venue"},
  "price": {"type": "string", "format": "decimal", "description": "observed price"},
  "reference_price": {"type": "string", "format": "decimal", "description": "reference price"},
  "spread_bps": {"type": "i32", "description": "bid-ask spread in basis points"},
  "liquidity_usd": {"type": "u64", "description": "estimated depth in USD"},
  "base_token": {"type": "string", "description": "base token symbol"},
  "quote_token": {"type": "string", "description": "quote token symbol"},
  "chain_id": {"type": "u64", "description": "chain identifier"},
  "timestamp_ns": {"type": "u64", "format": "nanoseconds", "description": "unix nanosecond timestamp"}
}
```

## Quote Request

```json
{
  "chain_id": 8453,
  "amount": "1000000000000000000",
  "destination": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
  "source": "0xSenderAddress",
  "intent": "execute"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chain_id` | u64 | yes | Target chain ID |
| `amount` | string | yes | Amount in smallest unit (wei, satoshi, lamport) |
| `destination` | string | yes | Chain-native destination address |
| `source` | string | no | Source address |
| `intent` | string | no | `execute` (default) or `quote` |
| `quote_id` | string | no | Lock a prior quote for execution |

### Ecosystem-Specific Fields

**EVM**: `token_address` (0x hex ERC20), `gas_priority` (low/medium/high)

**Solana**: `token_mint` (base58 SPL mint), `priority_fee_lamports` (u64)

**Cosmos**: `denom` (e.g. uatom), `memo` (critical for exchanges)

**UTXO**: `fee_rate` (sat/vbyte), `change_address`

**XRPL**: `destination_tag` (u32, critical for exchanges), `currency`

**Move**: `coin_type` (fully qualified type)

## Fee Model

- **Base fee**: 10 bps (0.10%)
- **Range**: 8-15 bps depending on amount
- **Size discount**: >$10K amount: -1 bps, >$100K: -2 bps
- **Minimum fee**: 8 bps
- **Maximum fee**: 15 bps
- Fee is deducted from the execution amount
- Fee locked at quote time, valid for 30 seconds

## Examples

### Python

```python
import urllib.request, json

# Get signal atoms
req = urllib.request.urlopen("https://api.nano-labs.io/v1/signal/atoms?n=5")
atoms = json.loads(req.read())
for atom in atoms["atoms"]:
    print(f"seq={atom['seq']} pair={atom['pair']} dev={atom['deviation_bps']}bps")

# Get a quote
data = json.dumps({"chain_id": 8453, "amount": "1000000", "destination": "0x..."}).encode()
req = urllib.request.Request("https://api.nano-labs.io/v1/quote",
                              data=data,
                              headers={"Content-Type": "application/json"})
quote = json.loads(urllib.request.urlopen(req).read())
print(f"fee: {quote['fee_bps']} bps, quote_id: {quote['quote_id']}")
```

### Rust

```rust
use std::io::Read;
use std::net::TcpStream;
use std::io::Write;

fn get_signal_atoms() -> String {
    let mut stream = TcpStream::connect("api.nano-labs.io:443").unwrap();
    // ... TLS handshake, HTTP GET /v1/signal/atoms?n=5
    // Returns JSON array of signal atoms
    todo!()
}
```

### curl

```bash
# Signal atoms (latest 10)
curl -s https://api.nano-labs.io/v1/signal/atoms?n=10 | python3 -m json.tool

# Signal summary
curl -s https://api.nano-labs.io/v1/signal/summary?n=1000 | python3 -m json.tool

# Full schema
curl -s https://api.nano-labs.io/v1/bots/schema | python3 -m json.tool

# Ecosystem configs
curl -s https://api.nano-labs.io/v1/bots/ecosystems | python3 -m json.tool

# Trading pairs
curl -s https://api.nano-labs.io/v1/bots/pairs | python3 -m json.tool

# Fee quote
curl -X POST https://api.nano-labs.io/v1/quote \
  -H "Content-Type: application/json" \
  -d '{"chain_id": 1, "amount": "10000000000000000", "destination": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"}'

# Health check
curl -s https://api.nano-labs.io/health
```

## Conservation Invariant

All execution enforces: `gross == net + fee`

This is verified at every layer — from the execution engine through settlement on SubZero 2477. Signal atoms include cryptographic commitments (BLAKE3 hashes) that can be verified against the rolling Merkle root at `/v1/signal/root`.

## Rate Limits

- Signal endpoints: 100 req/s (unauthenticated)
- Quote: 10 req/s per IP
- Execute: 5 req/s per IP
- Bot schema: 10 req/s (cached)

## Links

- [OpenAPI Spec](https://api.nano-labs.io/.well-known/openapi.json)
- [Discovery Document](https://api.nano-labs.io/.well-known/nanoport.json)
- [AI Plugin Manifest](https://api.nano-labs.io/.well-known/ai-plugin.json)
- [Signal Atoms (live)](https://api.nano-labs.io/v1/signal/atoms?n=10)
- [Bot Schema](https://api.nano-labs.io/v1/bots/schema)

## License

MIT

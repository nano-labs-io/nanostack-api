# NanoStack

Permissionless cross-chain execution. Native assets. No wrapping. No SDK.

**Base URL:** `https://api.nano-labs.io`

```bash
# 1. Get a quote
curl -s -X POST https://api.nano-labs.io/v1/quote \
  -H "Content-Type: application/json" \
  -d '{"chain_id": 8453, "amount": "1000000000000000000", "destination": "0xYourAddress"}'

# 2. Execute
curl -s -X POST https://api.nano-labs.io/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"chain_id": 8453, "amount": "1000000000000000000", "destination": "0xYourAddress"}'

# Cross-chain: Cosmos → ETH
curl -s -X POST https://api.nano-labs.io/v1/cross-chain \
  -H "Content-Type: application/json" \
  -d '{"src_chain_id": 118, "dst_chain_id": 1, "amount": "1000000", "denom": "uatom", "destination": "0xYourAddress"}'
```

No API key. No registration. No SDK.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/quote` | Fee quote. 8-15 bps, locked 30s. |
| POST | `/v1/execute` | Execute. Fee deducted from amount. |
| POST | `/v1/cross-chain` | Cross-chain execution. src + dst + amount. |
| POST | `/v1/register` | Optional API key (attribution + higher limits). |
| GET | `/v1/health` | Liveness. Returns `{"ok":true}`. |
| GET | `/v1/status` | Protocol stats and execution counters. |
| GET | `/v1/signal` | Real-time signal data. |
| GET | `/.well-known/nanostack.json` | Full manifest: chains, schemas, fee model. |

## Quote Request

```json
{
  "chain_id": 8453,
  "amount": "1000000000000000000",
  "destination": "0xYourAddress"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `chain_id` | u64 | yes | See chain list below |
| `amount` | string | yes | Smallest unit (wei / satoshi / lamport / uatom / drops) |
| `destination` | string | yes | Chain-native address |
| `source` | string | no | |
| `token_address` | string | no | EVM ERC20 only |
| `token_mint` | string | no | Solana SPL only |
| `denom` | string | no | Cosmos only (e.g. `uatom`) |
| `memo` | string | no | Cosmos — critical for exchange deposits |
| `destination_tag` | u32 | no | XRP — critical for exchange deposits |
| `fee_rate` | u64 | no | BTC sat/vbyte |
| `coin_type` | string | no | Move (APT/SUI) full type path |

## Fee Model

- **Base**: 10 bps (0.10%)
- **Range**: 8–15 bps based on amount
- **Locked**: at quote time, valid 30 seconds
- **Deducted**: from execution amount
- **Permissionless**: no key required

## Supported Chains (46)

### EVM (40)

| Chain | ID | Native |
|-------|----|--------|
| Ethereum | 1 | ETH |
| Base | 8453 | ETH |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | MATIC |
| BNB Chain | 56 | BNB |
| Avalanche | 43114 | AVAX |
| Fantom | 250 | FTM |
| Scroll | 534352 | ETH |
| zkSync Era | 324 | ETH |
| Linea | 59144 | ETH |
| Blast | 81457 | ETH |
| Mantle | 5000 | MNT |
| Mode | 34443 | ETH |
| Taiko | 167000 | ETH |
| Manta Pacific | 169 | ETH |
| Fraxtal | 252 | frxETH |
| Ink | 57073 | ETH |
| Zora | 7777777 | ETH |
| Unichain | 130 | ETH |
| World Chain | 480 | ETH |
| Xai | 660279 | XAI |
| X Layer | 196 | OKB |
| Gnosis | 100 | xDAI |
| Sei | 1329 | SEI |
| Celo | 42220 | CELO |
| Cronos | 25 | CRO |
| Moonbeam | 1284 | GLMR |
| Astar | 592 | ASTR |
| Aurora | 1313161554 | ETH |
| Kava | 2222 | KAVA |
| Metis | 1088 | METIS |
| Boba | 288 | ETH |
| Harmony | 1666600000 | ONE |
| Degen | 666666666 | DEGEN |
| Filecoin | 314 | FIL |
| Hedera EVM | 295 | HBAR |
| Ronin | 2020 | RON |
| Arbitrum Nova | 42170 | ETH |
| Polygon zkEVM | 1101 | ETH |

### Non-EVM (6)

| Chain | ID | Native | Signing |
|-------|----|--------|---------|
| Bitcoin | 0 | BTC | secp256k1, P2WPKH, RBF |
| Solana | 501 | SOL | ed25519 |
| Cosmos Hub | 118 | ATOM | secp256k1, amino/proto |
| XRP Ledger | 144 | XRP | secp256k1 |
| Aptos | 637 | APT | ed25519 (Move) |
| Sui | 784 | SUI | ed25519 (Move) |

## Discovery

Machine-readable manifest with all chain IDs, fee model, address formats, and request schemas:

```bash
curl -s https://api.nano-labs.io/.well-known/nanostack.json | python3 -m json.tool
```

## Conservation

Every execution enforces: `gross == net + fee`

Proven via BLAKE3 on SubZero ledger 2477. No execution settles without a valid conservation proof.

## License

MIT

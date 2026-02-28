# Lithosphere Makalu — Network Reference

## Chain Parameters

| Parameter | Value |
|-----------|-------|
| Cosmos Chain ID | `lithosphere_777777-1` |
| EVM Chain ID | `777777` |
| Bech32 Prefix | `litho` |
| Base Denom | `ulitho` |
| Display Denom | `LITHO` |
| Decimals | **18** |
| Block Time | ~1s (900ms commit) |
| Max Block Size | 21 MB |
| Max Gas/Block | 100,000,000 |
| Unbonding Period | 21 days (504h) |

> **Decimals is the most common mistake.** `lithod` is built on Evmos which uses 18-decimal base units — the same as Ethereum. `1 LITHO = 1,000,000,000,000,000,000 ulitho`. Any balance formatting that assumes 6 decimals will show values 10^12 times too small.

## Live Network Endpoints

### Public DNS (TLS)

| Service | URL |
|---------|-----|
| Explorer | https://makalu.litho.ai |
| Network Status | https://status.litho.ai |
| Cosmos RPC | https://rpc.litho.ai |
| Cosmos REST API | https://api.litho.ai |

### Direct Endpoints

| Service | URL |
|---------|-----|
| Cosmos RPC (Sentry 1) | `http://54.163.248.63:26657` |
| Cosmos RPC (Sentry 2) | `http://52.41.98.79:26657` |
| Cosmos REST / LCD | `http://54.163.248.63:1317` |
| gRPC | `54.163.248.63:9090` |
| EVM JSON-RPC (NLB) | `http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545` |
| EVM WebSocket | `ws://54.163.248.63:8546` |
| P2P Seed | `226e832ce82edd937a23285627003e95f89b9ce9@54.163.248.63:26656` |

## Genesis File

| Field | Value |
|-------|-------|
| SHA256 | `a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01` |
| Genesis Time | February 20, 2026 |
| Total Supply | 1,050,000,000 LITHO |
| Accounts | 16 (15 allocation + 1 validator operator) |
| Gentx Memo | *"The World's 1st Decentralized Intelligence Layer. J. King Kasr KaJ Labs"* |

Verify your copy:
```bash
sha256sum genesis.json
# must return: a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01
```

## Address Format

All Cosmos-layer addresses use the `litho` bech32 prefix. The underlying key bytes are identical to the EVM address — only the encoding differs.

| Layer | Format | Example |
|-------|--------|---------|
| Cosmos | `litho1...` | `litho1qnk2n4nlkpw9xfqntladh74er2xa62wacf7c4` |
| Validator operator | `lithovaloper1...` | `lithovaloper1...` |
| EVM | `0x...` (hex, 20 bytes) | `0xABC123...` |

Conversion utilities are included in this repo:
- `scripts/bech32_convert.py` — Convert between bech32 prefixes (zero dependencies)
- `scripts/convert_evm_to_cosmos.py` — Convert EVM `0x` addresses to Cosmos bech32

## Binary Reference

| Field | Value |
|-------|-------|
| Binary | `lithod` |
| Source | `https://github.com/evmos/evmos.git` (Evmos v20.0.0 fork) |
| Build Script | `bin/build-lithod.sh` |
| SHA256 | `4158ecbc82d59e15c3cda16e10a99a5ad5877496af301879c3594fd18eb3eb5a` |
| Go Version | 1.22+ |
| Bech32 Prefix | `litho` (replaces `evmos`) |
| Denom | `ulitho` (replaces `aevmos`) |

If your tooling parses the binary version string or module path, it will contain `evmos` references — this is expected.

## Staking Parameters

| Parameter | Value |
|-----------|-------|
| Bond Denom | `ulitho` |
| Max Validators | 100 |
| Unbonding Time | 21 days |
| Min Commission | 5% |
| Min Self Delegation | 1 |

## Slashing Parameters

| Parameter | Value |
|-----------|-------|
| Signed Blocks Window | 10,000 |
| Min Signed Per Window | 5% |
| Downtime Jail Duration | 10 min |
| Slash Fraction Double Sign | 5% |
| Slash Fraction Downtime | 1% |

## Governance Parameters

| Parameter | Value |
|-----------|-------|
| Min Deposit | 10,000 LITHO |
| Max Deposit Period | 48 hours |
| Voting Period | 48 hours |
| Quorum | 33.4% |
| Threshold | 50% |
| Veto Threshold | 33.4% |
| Expedited Min Deposit | 50,000 LITHO |

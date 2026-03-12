# Lithosphere Makalu — Validator Toolkit

Official resources for running a validator on the **Lithosphere Makalu** network.

---

## Network Overview

| Parameter | Value |
|-----------|-------|
| **Chain ID (Cosmos)** | `lithosphere_777777-1` |
| **Chain ID (EVM)** | `777777` |
| **Block Time** | ~1s (900ms timeout_commit) |
| **Max Block Size** | 21 MB |
| **Max Gas/Block** | 100,000,000 |
| **Unbonding Period** | 21 days |
| **Native Denom** | `ulitho` (1 LITHO = 10^18 ulitho) |
| **Bech32 Prefix** | `litho` (addresses: `litho1...`) |
| **Binary** | `lithod` (Evmos v20 fork with Lithosphere branding) |

## Live Endpoints

| Service | URL |
|---------|-----|
| Explorer | https://makalu.litho.ai |
| Network Status | https://status.litho.ai |
| Cosmos RPC (TLS) | https://rpc.litho.ai |
| Cosmos REST API (TLS) | https://api.litho.ai |
| Cosmos RPC (Sentry 1) | `http://54.163.248.63:26657` |
| Cosmos RPC (Sentry 2) | `http://52.41.98.79:26657` |
| EVM JSON-RPC | `http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545` |
| P2P Seed | `226e832ce82edd937a23285627003e95f89b9ce9@54.163.248.63:26656` |

## Quick Start

```bash
# 1. Build the binary (Linux x86_64 required)
bash bin/build-lithod.sh

# 2. Initialize your node
lithod init <YOUR_MONIKER> --chain-id lithosphere_777777-1 --home /var/lib/litho

# 3. Set chain-id in client.toml (required for Evmos-based chains)
sed -i 's/^chain-id = .*/chain-id = "lithosphere_777777-1"/' /var/lib/litho/config/client.toml

# 4. Install genesis
cp genesis.json /var/lib/litho/config/genesis.json
sha256sum /var/lib/litho/config/genesis.json
# Expected: a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01

# 5. Configure peers (config.toml)
# seeds = "226e832ce82edd937a23285627003e95f89b9ce9@54.163.248.63:26656"

# 6. Start
lithod start --home /var/lib/litho
```

For the full step-by-step guide, see [docs/VALIDATOR_SETUP.md](docs/VALIDATOR_SETUP.md).

## Repository Contents

```
litho-makalu-validators/
├── README.md                   # This file
├── genesis.json                # Official genesis file (SHA256 verified)
├── bin/
│   └── build-lithod.sh         # Build lithod from Evmos source
├── scripts/
│   ├── health-check.sh         # Node health monitoring
│   ├── backup-validator.sh     # Validator state backup
│   ├── bech32_convert.py       # Address prefix conversion (zero deps)
│   └── convert_evm_to_cosmos.py # EVM 0x → Cosmos bech32 conversion
├── config/
│   ├── config.toml.example     # CometBFT configuration reference
│   └── app.toml.example        # Application configuration reference
└── docs/
    ├── VALIDATOR_SETUP.md      # Complete validator setup guide
    ├── BINARY_INFO.md          # Binary lineage and build details
    └── NETWORK_REFERENCE.md    # Chain parameters and endpoints
```

## Genesis File

| Field | Value |
|-------|-------|
| SHA256 | `a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01` |
| Genesis Time | February 20, 2026 |
| Total Supply | 1,000,000,000 LITHO |
| Accounts | 16 (15 allocation + 1 validator operator) |

## MetaMask / EVM Wallet

| Field | Value |
|-------|-------|
| Network Name | `Lithosphere` |
| RPC URL | `https://rpc.litho.ai` |
| Chain ID | `777777` |
| Currency Symbol | `LITHO` |
| Block Explorer | `https://makalu.litho.ai` |

## Hardware Requirements

| | Minimum | Recommended |
|--|---------|-------------|
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04+ / Amazon Linux 2023 |
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 500 GB NVMe SSD | 1 TB NVMe SSD |
| Network | 100 Mbps | 1 Gbps |
| Port | 26656 (P2P, inbound) | - |

## Important Notes

- **Decimals**: `lithod` is built on Evmos which uses **18-decimal** base units (same as Ethereum). `1 LITHO = 1,000,000,000,000,000,000 ulitho`.
- **Chain ID format**: Uses Ethermint convention `{name}_{evmChainId}-{revision}`. The `client.toml` must have the correct chain-id set.
- **Binary source**: `lithod` is built from `evmos/evmos` with branding patches. The `KaJLabs/lithosphere` repo is the JS/TS monorepo, not the Go source.

## License

Copyright 2026 KaJ Labs / LITHO Foundation. All rights reserved.

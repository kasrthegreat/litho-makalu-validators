# Lithosphere Binary — Evmos Fork

## Overview

The `lithod` binary is built from a **minimal fork of Evmos v20.0.0** with Lithosphere branding. This gives a production-grade Cosmos-SDK + CometBFT + EVM-compatible binary with the correct bech32 prefix (`litho`), native denom (`ulitho`), and all required modules.

## Why Fork Evmos?

The `KaJLabs/lithosphere` GitHub repository is a JS/TS monorepo — not Go source code. The genesis file contains `evm` + `feemarket` modules, confirming this is an Ethermint-based chain. Evmos is the most mature Ethermint implementation.

## What Changed from Upstream Evmos

| Change | From | To |
|--------|------|----|
| Bech32 prefix | `evmos` | `litho` |
| Default denom | `aevmos` (18 decimals) | `ulitho` (18 decimals) |
| Binary name | `evmosd` | `lithod` |
| Default home | `~/.evmosd` | `~/.lithod` |
| Display name | `Evmos` / `EVMOS` | `Lithosphere` / `LITHO` |

All upstream Evmos functionality is preserved — EVM, IBC, staking, governance, inflation, erc20, epochs, etc.

## Artifacts

### Binary

| Field | Value |
|-------|-------|
| Platform | Linux x86_64 (ELF) |
| Version | 20.0.0 |
| SHA256 | `4158ecbc82d59e15c3cda16e10a99a5ad5877496af301879c3594fd18eb3eb5a` |
| Source | Evmos v20.0.0 with Lithosphere branding patches |

### Genesis

| Field | Value |
|-------|-------|
| Chain ID | `lithosphere_777777-1` |
| EVM Chain ID | `777777` (encoded in Cosmos chain_id) |
| Genesis Time | February 20, 2026 |
| Total Supply | 1,000,000,000 LITHO |
| Accounts | 16 (15 allocation + 1 validator operator) |
| SHA256 | `a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01` |

## Chain ID Format

The chain_id follows Ethermint convention: `{name}_{evmChainId}-{revision}`.

```
lithosphere_777777-1
│           │      └─ revision number
│           └─ EVM chain ID (used by MetaMask, ethers.js, etc.)
└─ chain name
```

## Genesis Module Configuration

### Core Parameters

| Module | Key Parameters |
|--------|----------------|
| **Consensus** | 21 MB max block, 100M max gas, 1000ms time_iota |
| **Staking** | `ulitho` bond denom, 21-day unbonding, 100 max validators, 5% min commission |
| **Distribution** | 2% community tax |
| **Slashing** | 10,000 block window, 5% double-sign slash, 1% downtime slash |
| **Governance** | 10,000 LITHO min deposit, 48h voting/deposit periods, 50,000 LITHO expedited |
| **EVM** | `ulitho` evm_denom, all forks at block 0, no unprotected txs |
| **Feemarket** | 1 gwei base fee, EIP-1559 enabled |
| **IBC** | solomachine + tendermint clients |

### Evmos-Specific Modules

| Module | Purpose |
|--------|---------|
| **epochs** | Day/week epoch tracking |
| **erc20** | ERC-20 <> Cosmos coin conversion |
| **inflation** | Evmos-style inflation (replaces standard cosmos mint) |
| **interchainaccounts** | ICA controller + host |
| **ratelimit** | IBC rate limiting |
| **feegrant** | Fee grant allowances |
| **authz** | Authorization grants |

## Denomination Structure

```
1 LITHO = 10^18 ulitho

ulitho  (10^0)   — base unit, used on-chain
litho   (10^18)  — display unit (1 LITHO)
```

The EVM uses `ulitho` as its native denomination. This is the same 18-decimal structure as Ethereum's wei.

## Build Process

### Prerequisites

- Linux x86_64 (WSL, Docker, or bare metal)
- Go 1.22+, make, gcc, git

### Steps

```bash
# Build with the included script
bash bin/build-lithod.sh

# Or override version
EVMOS_VERSION=v19.0.0 bash bin/build-lithod.sh

# Verify
lithod version                         # → 20.0.0
lithod validate-genesis genesis.json   # → valid
```

## Verification Checklist

- `lithod version` → `20.0.0`
- `lithod validate-genesis genesis.json` → PASSED
- `lithod init test --chain-id lithosphere_777777-1` produces `litho1...` addresses
- `sha256sum genesis.json` → `a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01`

# Lithosphere Validator Setup Guide

**Version:** 1.0 | **Date:** February 2026 | **Status:** LIVE — Chain producing blocks

---

## Network Reference

| Parameter | Value |
|-----------|-------|
| Chain ID (Cosmos) | `lithosphere_777777-1` |
| Chain ID (EVM) | `777777` |
| Block Time | ~1s (900ms timeout_commit) |
| Max Block Size | 21 MB |
| Max Gas/Block | 100,000,000 |
| Unbonding Period | 21 days |
| Native Denom | `ulitho` (1 LITHO = 10^18 ulitho) |
| Cosmos RPC | https://rpc.litho.ai |
| Cosmos REST API | https://api.litho.ai |
| EVM RPC (NLB) | `http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545` |
| P2P Seeds | `226e832ce82edd937a23285627003e95f89b9ce9@54.163.248.63:26656` |
| Explorer | https://makalu.litho.ai |
| Status Page | https://status.litho.ai |

---

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Ubuntu 22.04 LTS | Amazon Linux 2023 |
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 500 GB NVMe SSD | 1 TB NVMe SSD |
| Network | 100 Mbps | 1 Gbps |
| Port | 26656 (P2P, inbound) | — |

---

## Step-by-Step Setup

### Step 1 — Install Dependencies

```bash
# Ubuntu / Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git make gcc g++ jq curl wget unzip

# Amazon Linux 2023
sudo dnf update -y
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y git make gcc g++ jq curl wget unzip

# Install Go 1.22+
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
go version   # should print go1.22.0 linux/amd64
```

---

### Step 2 — Build the lithod Binary

The `lithod` binary is built from the **Evmos source** with Lithosphere branding applied.

```bash
# Use the build script from this repo
bash bin/build-lithod.sh

# Verify
lithod version
lithod keys add --help | grep -i litho   # should show litho1... prefix
```

Or build manually:

```bash
git clone https://github.com/evmos/evmos.git lithosphere-src
cd lithosphere-src
git checkout main

# Apply Lithosphere branding (bech32 prefix + denom)
find . -type f -name "*.go" | xargs sed -i \
  's/evmos/litho/g; s/aevmos/ulitho/g; s/Evmos/Litho/g; s/EVMOS/LITHO/g'

make install

lithod version
```

> **Pre-built binary SHA256**: `4158ecbc82d59e15c3cda16e10a99a5ad5877496af301879c3594fd18eb3eb5a`

---

### Step 3 — Create System User

```bash
sudo useradd -r -m -s /bin/false litho
sudo mkdir -p /var/lib/litho
sudo chown litho:litho /var/lib/litho
```

---

### Step 4 — Initialize Node

```bash
# IMPORTANT: chain-id must be lithosphere_777777-1 (Ethermint format)
lithod init <YOUR_MONIKER> --chain-id lithosphere_777777-1 --home /var/lib/litho

# Also set it in client.toml (required for Evmos-based chains)
sed -i 's/^chain-id = .*/chain-id = "lithosphere_777777-1"/' \
  /var/lib/litho/config/client.toml
```

---

### Step 5 — Install Genesis File

```bash
# Copy the official genesis from this repo
cp genesis.json /var/lib/litho/config/genesis.json

# Verify checksum
sha256sum /var/lib/litho/config/genesis.json
# Expected: a8e1ed954e671b7c8c7ffa043d9de2e7655ae21058ac3aa7c2e5a03c4340ba01
```

---

### Step 6 — Configure Peers

Edit `/var/lib/litho/config/config.toml`:

```toml
[p2p]
seeds = "226e832ce82edd937a23285627003e95f89b9ce9@54.163.248.63:26656"
persistent_peers = ""
addr_book_strict = false
max_num_inbound_peers = 40
max_num_outbound_peers = 10
```

See `config/config.toml.example` for a full reference.

---

### Step 7 — Configure app.toml

Edit `/var/lib/litho/config/app.toml`:

```toml
minimum-gas-prices = "0ulitho"
pruning = "custom"
pruning-keep-recent = "100"
pruning-interval = "10"

[json-rpc]
enable = true
address = "0.0.0.0:8545"
ws-address = "0.0.0.0:8546"
api = "eth,net,web3,txpool"

[api]
enable = true
swagger = false
address = "tcp://0.0.0.0:1317"
```

See `config/app.toml.example` for a full reference.

---

### Step 8 — Create systemd Service

```bash
sudo tee /etc/systemd/system/lithod.service > /dev/null << 'EOF'
[Unit]
Description=Lithosphere Node (lithod)
After=network-online.target
Wants=network-online.target

[Service]
User=litho
Group=litho
ExecStart=/usr/local/bin/lithod start --home /var/lib/litho
Restart=always
RestartSec=3
LimitNOFILE=1048576
LimitNPROC=65536
ProtectSystem=full
NoNewPrivileges=true
PrivateTmp=true
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable lithod
sudo systemctl start lithod
```

---

### Step 9 — Monitor Sync

```bash
# Watch logs
journalctl -u lithod -f

# Check sync status (should show catching_up: false when fully synced)
curl -s http://localhost:26657/status | jq '.result.sync_info'

# Check block height (compare against network)
curl -s http://localhost:26657/status | jq '.result.sync_info.latest_block_height'
curl -s https://rpc.litho.ai/status | jq '.result.sync_info.latest_block_height'
```

---

### Step 10 — Create Validator (after full sync)

```bash
# Create or recover a key
lithod keys add <KEY_NAME> --home /var/lib/litho
# or recover: lithod keys add <KEY_NAME> --recover --home /var/lib/litho

# Check balance (you need LITHO tokens to stake)
lithod query bank balances <YOUR_LITHO_ADDRESS> \
  --node https://rpc.litho.ai \
  --chain-id lithosphere_777777-1

# Create validator
lithod tx staking create-validator \
  --amount=1000000000000000000ulitho \
  --pubkey=$(lithod tendermint show-validator --home /var/lib/litho) \
  --moniker="<YOUR_MONIKER>" \
  --chain-id=lithosphere_777777-1 \
  --commission-rate="0.10" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1" \
  --from=<KEY_NAME> \
  --fees=500000000000000ulitho \
  --node https://rpc.litho.ai \
  --home /var/lib/litho
```

> **Note**: 1 LITHO = `1000000000000000000 ulitho` (18 decimals). Minimum stake is 1 ulitho.

---

## MetaMask / EVM Wallet Configuration

| Field | Value |
|-------|-------|
| Network Name | `Lithosphere` |
| RPC URL | `http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545` |
| Chain ID | `777777` |
| Currency Symbol | `LITHO` |
| Block Explorer | `https://makalu.litho.ai` |

---

## Health Check Commands

```bash
# Cosmos RPC — sync status
curl -s https://rpc.litho.ai/status | jq '.result.sync_info'

# Cosmos RPC — connected peers
curl -s https://rpc.litho.ai/net_info | jq '.result.n_peers'

# Cosmos RPC — latest block height
curl -s https://rpc.litho.ai/status | jq '.result.sync_info.latest_block_height'

# Cosmos RPC — validator set
curl -s https://rpc.litho.ai/validators | jq '.result'

# EVM RPC — current block number
curl -s -X POST http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# EVM RPC — chain ID
curl -s -X POST http://litho-mainnet-rpc-nlb-90cbce98dabd2453.elb.us-east-1.amazonaws.com:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

---

## Useful Scripts

This repository includes several utility scripts:

| Script | Purpose |
|--------|---------|
| `scripts/health-check.sh` | Comprehensive node health check (service, sync, peers, resources) |
| `scripts/backup-validator.sh` | Backup validator config and state (excludes private keys) |
| `scripts/bech32_convert.py` | Convert bech32 addresses between prefixes (e.g., `cosmos1` to `litho1`) |
| `scripts/convert_evm_to_cosmos.py` | Convert EVM `0x` addresses to Cosmos bech32 format |

#!/bin/bash
# LITHO Node Health Check Script
# Usage: ./health-check.sh [validator|sentry]

set -euo pipefail

NODE_TYPE="${1:-validator}"
RPC_ENDPOINT="${LITHO_RPC:-http://127.0.0.1:26657}"
METRICS_PORT="${LITHO_METRICS_PORT:-26660}"
LITHO_HOME="${LITHO_HOME:-/var/lib/litho}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "  LITHO Node Health Check - ${NODE_TYPE}"
echo "============================================"
echo ""

# Check systemd service
echo -n "Systemd Service: "
if systemctl is-active --quiet lithod; then
    echo -e "${GREEN}RUNNING${NC}"
else
    echo -e "${RED}STOPPED${NC}"
    exit 1
fi

# Check RPC endpoint
echo -n "RPC Endpoint: "
if curl -s "${RPC_ENDPOINT}/status" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}UNREACHABLE${NC}"
    exit 1
fi

# Get node status
STATUS=$(curl -s "${RPC_ENDPOINT}/status")

# Check sync status
CATCHING_UP=$(echo "$STATUS" | jq -r '.result.sync_info.catching_up')
LATEST_HEIGHT=$(echo "$STATUS" | jq -r '.result.sync_info.latest_block_height')
LATEST_TIME=$(echo "$STATUS" | jq -r '.result.sync_info.latest_block_time')

echo -n "Sync Status: "
if [ "$CATCHING_UP" == "false" ]; then
    echo -e "${GREEN}SYNCED${NC}"
else
    echo -e "${YELLOW}CATCHING UP${NC}"
fi

echo "Latest Block Height: ${LATEST_HEIGHT}"
echo "Latest Block Time: ${LATEST_TIME}"

# Check peers
PEERS=$(curl -s "${RPC_ENDPOINT}/net_info" | jq -r '.result.n_peers')
echo -n "Connected Peers: "
if [ "$PEERS" -gt 0 ]; then
    echo -e "${GREEN}${PEERS}${NC}"
else
    echo -e "${RED}${PEERS}${NC}"
fi

# Check metrics endpoint
echo -n "Metrics Endpoint: "
if curl -s "http://127.0.0.1:${METRICS_PORT}/metrics" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}UNAVAILABLE${NC}"
fi

# Validator-specific checks
if [ "$NODE_TYPE" == "validator" ]; then
    echo ""
    echo "--- Validator Checks ---"

    # Check if validator is in active set (requires voting power check)
    VOTING_POWER=$(echo "$STATUS" | jq -r '.result.validator_info.voting_power')
    echo -n "Voting Power: "
    if [ "$VOTING_POWER" != "0" ] && [ "$VOTING_POWER" != "null" ]; then
        echo -e "${GREEN}${VOTING_POWER}${NC}"
    else
        echo -e "${YELLOW}${VOTING_POWER:-N/A}${NC}"
    fi
fi

# Disk usage
echo ""
echo "--- System Resources ---"
DISK_USAGE=$(df -h "${LITHO_HOME}" 2>/dev/null | tail -1 | awk '{print $5}' || echo "N/A")
echo "Disk Usage: ${DISK_USAGE}"

# Memory usage
MEM_USAGE=$(free -h | grep Mem | awk '{print $3 "/" $2}')
echo "Memory Usage: ${MEM_USAGE}"

# CPU load
LOAD=$(uptime | awk -F'load average:' '{print $2}' | xargs)
echo "Load Average: ${LOAD}"

echo ""
echo "============================================"
echo "Health check complete"
echo "============================================"

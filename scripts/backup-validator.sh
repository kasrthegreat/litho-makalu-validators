#!/bin/bash
# LITHO Validator Backup Script
# Usage: ./backup-validator.sh [backup-dir]

set -euo pipefail

LITHO_HOME="${LITHO_HOME:-/var/lib/litho}"
BACKUP_DIR="${1:-/opt/backups/litho}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="litho-validator-backup-${TIMESTAMP}"

echo "============================================"
echo "  LITHO Validator Backup"
echo "============================================"
echo ""
echo "Source: ${LITHO_HOME}"
echo "Destination: ${BACKUP_DIR}/${BACKUP_NAME}"
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Stop service for consistent backup
echo "Stopping lithod service..."
sudo systemctl stop lithod || true
sleep 5

# Backup config (without private keys)
echo "Backing up configuration..."
mkdir -p "${BACKUP_DIR}/${BACKUP_NAME}/config"
cp "${LITHO_HOME}/config/config.toml" "${BACKUP_DIR}/${BACKUP_NAME}/config/"
cp "${LITHO_HOME}/config/app.toml" "${BACKUP_DIR}/${BACKUP_NAME}/config/"
cp "${LITHO_HOME}/config/genesis.json" "${BACKUP_DIR}/${BACKUP_NAME}/config/" 2>/dev/null || true
cp "${LITHO_HOME}/config/addrbook.json" "${BACKUP_DIR}/${BACKUP_NAME}/config/" 2>/dev/null || true

# Backup priv_validator_state.json (required for recovery)
echo "Backing up validator state..."
cp "${LITHO_HOME}/data/priv_validator_state.json" "${BACKUP_DIR}/${BACKUP_NAME}/" 2>/dev/null || true

# NOTE: Validator keys are NOT backed up here
echo "WARNING: Validator private keys are NOT included in this backup."
echo "         Key custody is your responsibility."

# Backup data directory (optional, large)
read -p "Backup data directory? This may take a while. (y/N): " BACKUP_DATA
if [[ "$BACKUP_DATA" =~ ^[Yy]$ ]]; then
    echo "Backing up data directory..."
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}/data.tar.gz" -C "${LITHO_HOME}" data/
fi

# Restart service
echo "Starting lithod service..."
sudo systemctl start lithod

# Create checksum
echo "Creating checksums..."
cd "${BACKUP_DIR}/${BACKUP_NAME}"
sha256sum * > SHA256SUMS 2>/dev/null || true

# Compress backup
echo "Compressing backup..."
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
rm -rf "${BACKUP_NAME}"

echo ""
echo "============================================"
echo "Backup complete: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo "============================================"

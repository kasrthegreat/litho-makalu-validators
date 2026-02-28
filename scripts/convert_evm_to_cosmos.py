#!/usr/bin/env python3
"""
Convert EVM addresses to Cosmos SDK bech32 addresses.

This script reads the token distribution CSV and converts all EVM addresses
to their equivalent Cosmos SDK format (cosmos1...) using the same underlying
public key hash.

Requirements:
    pip install bech32
"""

import csv
import sys
from pathlib import Path

try:
    import bech32
except ImportError:
    print("Error: bech32 library not installed")
    print("Install with: pip install bech32")
    sys.exit(1)


def evm_to_cosmos(evm_address: str, prefix: str = "cosmos") -> str:
    """
    Convert an EVM address (0x...) to Cosmos bech32 format.
    
    Args:
        evm_address: Ethereum address starting with 0x
        prefix: Bech32 prefix (default: "cosmos")
    
    Returns:
        Cosmos address in bech32 format (e.g., cosmos1...)
    """
    # Remove 0x prefix and convert to lowercase
    evm_address = evm_address.strip().lower()
    if evm_address.startswith('0x'):
        evm_address = evm_address[2:]
    
    # Convert hex string to bytes
    addr_bytes = bytes.fromhex(evm_address)
    
    # Convert bytes to 5-bit groups for bech32
    five_bit_data = bech32.convertbits(addr_bytes, 8, 5)
    
    if five_bit_data is None:
        raise ValueError(f"Failed to convert address: {evm_address}")
    
    # Encode with bech32
    cosmos_address = bech32.bech32_encode(prefix, five_bit_data)
    
    if cosmos_address is None:
        raise ValueError(f"Failed to encode bech32 address for: {evm_address}")
    
    return cosmos_address


def main():
    # Path to CSV file
    csv_path = Path(__file__).parent.parent / "LITHO_token_distribution 2.csv"
    
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    print("Converting EVM addresses to Cosmos format...")
    print("=" * 80)
    
    # Read CSV and convert addresses
    conversions = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            evm_addr = row['address'].strip()
            category = row['category'].strip()
            allocation = row['allocation_amount'].strip()
            
            # Convert to Cosmos format
            cosmos_addr = evm_to_cosmos(evm_addr)
            
            conversions.append({
                'index': idx,
                'category': category,
                'evm_address': evm_addr,
                'cosmos_address': cosmos_addr,
                'allocation': allocation
            })
            
            print(f"{idx:2d}. {category:30s}")
            print(f"    EVM:    {evm_addr}")
            print(f"    Cosmos: {cosmos_addr}")
            print(f"    Amount: {allocation:>15s} LITHO")
            print()
    
    print("=" * 80)
    print(f"Total addresses converted: {len(conversions)}")
    
    # Save to output file
    output_path = Path(__file__).parent.parent / "address_mapping_cosmos.csv"
    
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['index', 'category', 'evm_address', 'cosmos_address', 'allocation']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(conversions)
    
    print(f"\nAddress mapping saved to: {output_path}")
    
    # Also create a JSON mapping for easy reference
    import json
    json_output = Path(__file__).parent.parent / "address_mapping_cosmos.json"
    
    with open(json_output, 'w') as f:
        json.dump(conversions, f, indent=2)
    
    print(f"JSON mapping saved to: {json_output}")


if __name__ == "__main__":
    main()

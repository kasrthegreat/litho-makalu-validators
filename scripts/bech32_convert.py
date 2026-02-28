#!/usr/bin/env python3
"""
bech32_convert.py — Convert bech32 addresses between prefixes.

Standalone, zero-dependency implementation of BIP-173 bech32 encoding.
Used by generate_lithosphere_genesis.sh to re-encode cosmos1... → litho1...

Usage:
    python3 bech32_convert.py <address> <new_prefix>
    python3 bech32_convert.py cosmos1jqa20fhuxlceg7mwflpcxgfe4r2p2g2flq05zr litho

The underlying key bytes are identical — only the prefix and checksum change.
"""
import sys

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    GEN = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def _hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _verify_checksum(hrp, data):
    return _polymod(_hrp_expand(hrp) + data) == 1


def _create_checksum(hrp, data):
    values = _hrp_expand(hrp) + data
    polymod = _polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_decode(bech):
    """Decode a bech32 string. Returns (hrp, data) or (None, None)."""
    bech = bech.strip().lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        return None, None
    if not all(x in CHARSET for x in bech[pos + 1 :]):
        return None, None
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1 :]]
    if not _verify_checksum(hrp, data):
        return None, None
    return hrp, data[:-6]


def bech32_encode(hrp, data):
    """Encode hrp + data (5-bit integers) into a bech32 string."""
    combined = data + _create_checksum(hrp, data)
    return hrp + "1" + "".join(CHARSET[d] for d in combined)


def convert(address, new_prefix):
    """Re-encode a bech32 address with a new human-readable prefix."""
    hrp, data = bech32_decode(address)
    if hrp is None:
        print(f"ERROR: invalid bech32 address: {address}", file=sys.stderr)
        sys.exit(1)
    return bech32_encode(new_prefix, data)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Single address conversion
        print(convert(sys.argv[1], sys.argv[2]))
    elif len(sys.argv) == 4 and sys.argv[1] == "--batch":
        # Batch mode: read addresses from file, convert, write to stdout
        new_prefix = sys.argv[2]
        with open(sys.argv[3]) as f:
            for line in f:
                addr = line.strip()
                if addr:
                    print(convert(addr, new_prefix))
    else:
        print(
            f"Usage:\n"
            f"  {sys.argv[0]} <address> <new_prefix>\n"
            f"  {sys.argv[0]} --batch <new_prefix> <file_of_addresses>",
            file=sys.stderr,
        )
        sys.exit(1)

#!/usr/bin/env python3
"""QR code encoder (Version 1, numeric mode)."""
import sys

# Simplified QR — generates the data encoding portion
def encode_numeric(data):
    bits = "0001"  # Numeric mode
    bits += format(len(data), "010b")  # Character count (10 bits for V1)
    for i in range(0, len(data), 3):
        group = data[i:i+3]
        if len(group) == 3: bits += format(int(group), "010b")
        elif len(group) == 2: bits += format(int(group), "07b")
        else: bits += format(int(group), "04b")
    bits += "0000"  # Terminator
    while len(bits) % 8: bits += "0"
    # Pad to 19 bytes (Version 1-M)
    pads = [0xEC, 0x11]; idx = 0
    while len(bits) < 152:
        bits += format(pads[idx % 2], "08b"); idx += 1
    return bits

def bits_to_bytes(bits):
    return [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]

def display_matrix(size=21):
    """Show a QR-like pattern (finder patterns only for demo)."""
    m = [["░"] * size for _ in range(size)]
    # Finder patterns at corners
    for pos in [(0,0),(0,size-7),(size-7,0)]:
        r,c = pos
        for i in range(7):
            for j in range(7):
                if i in(0,6) or j in(0,6) or (2<=i<=4 and 2<=j<=4):
                    if 0<=r+i<size and 0<=c+j<size: m[r+i][c+j]="█"
    return "\n".join("".join(row) for row in m)

if __name__ == "__main__":
    data = sys.argv[1] if len(sys.argv) > 1 else "12345678"
    bits = encode_numeric(data)
    bytez = bits_to_bytes(bits)
    print(f"Data: {data}")
    print(f"Encoded: {len(bits)} bits, {len(bytez)} bytes")
    print(f"Bytes: {' '.join(f'{b:02x}' for b in bytez[:10])}...")
    print(f"\nQR Pattern (V1 finder patterns):")
    print(display_matrix())

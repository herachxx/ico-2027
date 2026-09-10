#!/usr/bin/env python3
_K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
_MASK = 0xffffffff


def _rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & _MASK


def _compress(state, block):
    w = list(int.from_bytes(block[i:i+4], "big") for i in range(0, 64, 4))
    for i in range(16, 64):
        s0 = _rotr(w[i-15], 7) ^ _rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = _rotr(w[i-2], 17) ^ _rotr(w[i-2], 19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & _MASK)
    a, b, c, d, e, f, g, h = state
    for i in range(64):
        S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        t1 = (h + S1 + ch + _K[i] + w[i]) & _MASK
        S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (S0 + maj) & _MASK
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & _MASK, c, b, a, (t1 + t2) & _MASK
    return [(x + y) & _MASK for x, y in zip(state, (a, b, c, d, e, f, g, h))]


def sha256_padding(total_len_bytes):
    bit_len = (total_len_bytes * 8) & 0xffffffffffffffff
    pad = b"\x80"
    pad += b"\x00" * ((56 - (total_len_bytes + 1) % 64) % 64)
    pad += bit_len.to_bytes(8, "big")
    return pad


def state_from_hexdigest(hexdigest):
    b = bytes.fromhex(hexdigest)
    return [int.from_bytes(b[i:i+4], "big") for i in range(0, 32, 4)]


def hexdigest_from_state(state):
    return b"".join(x.to_bytes(4, "big") for x in state).hex()


def extend(known_hexdigest, known_total_len, suffix):
    state = state_from_hexdigest(known_hexdigest)
    glue = sha256_padding(known_total_len)
    total_before_suffix = known_total_len + len(glue)
    data = suffix + sha256_padding(total_before_suffix + len(suffix))
    for i in range(0, len(data), 64):
        state = _compress(state, data[i:i+64])
    return hexdigest_from_state(state), glue

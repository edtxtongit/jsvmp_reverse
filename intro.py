import math

def to_uint32(n):
    """模拟JS float到uint32截断"""
    mod = math.fmod(n, 4294967296.0)
    if mod < 0:
        mod += 4294967296.0
    return int(mod)

def rotl13_32(h):
    """32位左旋13位"""
    return ((h << 13) | (h >> 19)) & 0xFFFFFFFF

def hash_salt(s, init=2166136261):
    """盐字符串：纯signed float FNV路径（无rotation分支）"""
    h = float(init)
    prime = float(16777619)
    for c in s:
        u_h = to_uint32(h)
        int_h = u_h if u_h < 0x80000000 else (u_h - 0x100000000)  # ToInt32
        xor_s = int_h ^ ord(c)
        temp = float(xor_s) * prime
        h = float(to_uint32(temp))
    return int(h)

def hash_long(s, init):
    """长字符串：signed float + 每index%3==2时左旋13位"""
    h = float(init)
    prime = float(16777619)
    for i, c in enumerate(s):
        u_h = to_uint32(h)
        int_h = u_h if u_h < 0x80000000 else (u_h - 0x100000000)
        xor_s = int_h ^ ord(c)
        temp = float(xor_s) * prime
        new_h = to_uint32(temp)
        if i % 3 == 2: 
            new_h = rotl13_32(new_h)
        h = float(new_h)
    return int(h)

def to_base36(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    res = ""
    n = n & 0xFFFFFFFF
    while n > 0:
        res = digits[n % 36] + res
        n //= 36
    return res or "0"

# 字符串
salt = "16f16d1474ec2efb82255baqRYG669d58pTIny8"
long_str = "1766835263864wF7jLiS5X6023CH2knM1f4Gfs8o7yEunwb4Vi9N1B05HY87p99"+salt # Date.now+随机字符串有格式要求

# 计算
seed = hash_salt(salt)
print(f"Salt seed: {seed} (0x{seed:08X})")  # 533659804 (0x1FD4A42C)

final_hash = hash_long(long_str, seed)
print(f"Final hash: {final_hash} (0x{final_hash:08X})")
print(f"Base36 output: {to_base36(final_hash)}")  # 1q6olre

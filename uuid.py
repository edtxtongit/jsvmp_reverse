def u32(n: int) -> int:
    return n & 0xFFFFFFFF

def rol_left_5(acc: int) -> int:
    return u32((acc << 5) | (acc >> 27))

def compute_part(seed: int, data: str, offset: int) -> str:
    acc = seed
    length = len(data)
    i = offset
    while i < length:
        c = ord(data[i])
        acc = acc ^ c  # 净效果，隐藏的 ^856 ^c ^856 同
        i += 1
        if i < length:  # 关键：最后一个char不mix！
            acc = rol_left_5(acc)
    return format(acc, '08x')

def generate_pseudo_uuid(data: str) -> str:
    seeds = [0x79bde035, 0x468acf02, 0xdb97531f, 0xeca86430]
    
    parts = [compute_part(seeds[r], data, r) for r in range(4)]
    
    # 伪造v4 UUID格式
    uuid_chars = list(f"{parts[0]}-{parts[1][:4]}-{parts[1][4:]}-{parts[2][:4]}-{parts[2][4:]}{parts[3]}")
    uuid_chars[14] = '4'  # 疑似时间最后一位
    uuid_chars[19] = '9'  # 疑似随机最后一位
    return ''.join(uuid_chars)

# 测试
data = "MhrcLF0LMJHA3tUg2J0o0abXaVmynhDIiEW5mclebU2wjN9hHGhKSC9xsluvHA2uCX5RwrXZKNXvi9W1CXNPFoZpMDLRbNhpZPLT8aybBG"
print(generate_pseudo_uuid(data))
# 输出: a33e3c74-95fe-4105-938b-c3bd241b41df

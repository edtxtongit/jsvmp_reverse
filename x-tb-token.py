def rotate_left(value, shift):
    v = value & 0xFF
    k = shift % 8
    if k == 0:
        return v
    return ((v << k) | (v >> (8 - k))) & 0xFF

long_str = "MhrcLF0LMJHA3tUg2J0o0abXaVmynhDIiEW5mclebU2wjN9hHGhKSC9xsluvHA2uCX5RwrXZKNXvi9W1CXNPFoZpMDLRbNhpZPLT8aybBG" # x-ab-token来的
input_bytes = [ord(c) for c in long_str]
key = [110, 67, 90, 87, 66, 86, 53] # "nCZWBV5"
seed = 105
state = seed
carry = seed
output = [seed]

# 第一步：生成原始 output
for i in range(len(input_bytes)):
    key_idx = i % len(key)
    key_byte = key[key_idx]
    temp = input_bytes[i] ^ state
    temp ^= key_byte
    temp += carry
    temp &= 0xFF
    shift = key_idx
    rotated = rotate_left(temp, shift)
    output.append(rotated)
    carry = rotated
    state = ((state + i) + seed + key_byte) & 0xFF

# 第二步：奇偶拆分重组
arr1 = []  # 奇数索引
arr2 = []  # 偶数索引

for index, item in enumerate(output):
    if (index - 1) % 2 == 0 or index == 0:
        arr2.append(item)  # 偶数索引
    else:
        arr1.append(item)  # 奇数索引

# 数组二 + 数组一
result = arr2 + arr1
hex_string = "".join(f"{b:02x}" for b in result)
print(hex_string) # 输出为 69b304fcfc1cec2942b868af135b8e4a9eedfa4a5c3d6297135fd33f72ad7b612bb86fabaec7bf977cb14f11a77da46e89cf06c476ed3c5406aaa83a674630081990c22fde22cb53fc911c237c95a9ac17ede05301be01fe5c8c6983bd81c58a0ed333c6ead26acdfeb993

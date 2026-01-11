def to_int32(n: int) -> int:
    """模拟 JavaScript ToInt32 / |0 的 signed 32 位截断"""
    n %= (1 << 32)
    if n >= (1 << 31):
        n -= (1 << 32)
    return n

alphabet = "LMNOPQRShiTUVWXYZ2pJKqrs56789ABFGHIabcde34fgjk01lmnotuvwCDExyz-_"

def custom_b64encode(data: bytes) -> str:
    """自定义 Base64 编码（无 padding，按 3 字节 -> 4 字符处理，最后不完整组正确截断）"""
    result = []
    i = 0
    while i < len(data):
        chunk_len = min(3, len(data) - i)
        num = 0
        for j in range(chunk_len):
            num = (num << 8) | data[i + j]
        # 生成  chunk_len + 1 个字符
        for j in range(chunk_len + 1):
            shift = 18 - j * 6
            result.append(alphabet[(num >> shift) & 0x3F])
        i += 3
    return ''.join(result)

def generate_token(input_str: str) -> str:
    fixed_key = "16f16d1474ec2efb82255baqRYG669d58pTIny8"
    seed = 1515870810

    # 密钥哈希（精确 signed 32 位，与日志匹配）
    h = seed
    for c in fixed_key:
        h = to_int32(h * 33 + ord(c))

    plaintext = input_str.encode('utf-8')
    state = h

    encrypted = bytearray()
    for b in plaintext:
        # 模拟 JS float 精度丢失的乘法（关键！）
        temp = float(state) * 1103515245.0 + 12345.0
        state = to_int32(int(temp))  # 取回 signed 32 位
        # 提取中间字节（bits 16-23）
        k = ((state & 0xFFFFFFFF) >> 16) & 0xFF
        c = b ^ k
        encrypted.append(c)

    # 前缀：长度编码为 12 位（高 6 位 + 低 6 位）
    length = len(plaintext)
    prefix = alphabet[length >> 6] + alphabet[length & 0x3F]

    # 自定义 Base64
    payload = custom_b64encode(bytes(encrypted))

    return prefix + payload

# 测试（你的原输入）
input_str = "1766835263864|wF7jLiS5X6023CH2knM1f4Gfs8o7yEunwb4Vi9N1B05HY87p99|1q6olre"
token = generate_token(input_str)
print("Generated token:", token)

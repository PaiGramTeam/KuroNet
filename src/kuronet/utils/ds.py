import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt(value):
    # JavaScript代码中的Base64编码密钥
    key_base64 = "XSNLFgNCth8j8oJI3cNIdw=="

    # 将Base64编码的密钥解码为字节
    key = base64.b64decode(key_base64)

    # 输入的'value'应该是Base64编码的加密字符串
    # 将其解码为字节
    encrypted_data = base64.b64decode(value)

    # 使用解码后的密钥创建一个AES密码对象，使用ECB模式
    cipher = AES.new(key, AES.MODE_ECB)

    # 解密加密的数据
    decrypted_data = cipher.decrypt(encrypted_data)

    # 使用PKCS7填充方式去除填充
    plaintext = unpad(decrypted_data, AES.block_size, style="pkcs7")

    # 将明文字节转换为UTF-8字符串并返回
    return plaintext.decode("utf-8")

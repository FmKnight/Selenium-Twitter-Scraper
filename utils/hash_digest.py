from hashlib import sha256

def msg_digest(content):
    """[summary]

    Args:
        content ([str]): [big str which ready to get its hash msg digest]

    Returns:
        [str]: [hash msg digest str]
    """
    content = content.encode("utf-8")
    sha256_str = sha256(content).hexdigest()
    return sha256_str


if __name__ == '__main__':
    raw_content = "hello my name is krahets"
    print(msg_digest(raw_content))

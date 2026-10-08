def mask_secret(value):
    """Che bí mật cho log: luôn có dấu sao, chỉ lộ tối đa 4 ký tự cuối."""
    if not isinstance(value, str) or len(value) < 12:
        return "****"
    return "****" + value[-4:]

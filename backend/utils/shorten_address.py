def get_shorten_address(address: str, front_chars=6, back_chars=6, ellipsis_='…') -> str:
    """
    Returns:
    str: The shortened address.
    """
    return address[:front_chars] + ellipsis_ + address[-back_chars:]

def bytes2human(n, format_str="%(value).1f%(symbol)s"):
    """Used by various scripts. See:
    http://goo.gl/zeJZl

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'
    """
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format_str % locals()
    return format_str % dict(symbol=symbols[0], value=n)

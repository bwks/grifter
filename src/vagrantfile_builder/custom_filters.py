def explode_port(port):
    """
    Create a high port number > 10000 for use with UDP tunnels
    :param port: port number to add to 10000
    :return: Int port number
    """
    port_error = 'port must be and integer from 1 to 99 or 666'
    base_port = 10000

    if not isinstance(port, int):
        raise AttributeError(port_error)

    if port == 666:
        return base_port + port

    elif not 0 < port < 100:
        raise AttributeError(port_error)

    return base_port + port


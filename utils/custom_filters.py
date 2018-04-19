def explode_port(port):
    """
    Create a high port number > 10000 for use with UDP tunnels
    :param port: port number to add to 10000
    :return: Int port number
    """
    if not isinstance(port, int) or port < 0 or port > 99:
        raise AttributeError('port must be and integer between 0 and 99')

    return 10000 + port

#! /usr/bin/env python
import random

def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for i in range(0,3)])     
    return '{0}:{1}'.format(oui, nic)

if __name__ == '__main__':
    print(get_mac())


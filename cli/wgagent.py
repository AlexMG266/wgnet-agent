#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: AlexMG266 <alex.mosquera@udc.es>

import argparse
from pkg.__version__ import __version__

def main():
    parser = argparse.ArgumentParser(
        description='wgagent - A WireGuard VPN local configuration manager for wgnet-weaver',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--version', action='version', version=f'NetWeaver {__version__}')
    subparsers = parser.add_subparsers(dest='command', required=True)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
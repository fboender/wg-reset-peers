#!/bin/env python3

"""
Script that reads wireguard configurations and resets each peer's endpoint.

This is useful when wireguard configurations use domain names for endpoints,
such as:

    Endpoint = vpn.electricmonk.nl:51820

Wireguard only resolves the domain name on startup. If the IP changes, the
peer's endpoint must be reset using:

    $ wg set <INTERFACE> peer <PUBLIC_KEY> endpoint <ENDPOINT>

This does not interrupt the peer's connection or traffic.

This script automatically takes care of this.

You can run it from a cronjob every 5 minutes:

    */5 * * * * /usr/local/bin/wg-reset-peers.py
"""

import os
import sys
import glob
import subprocess


def debug_msg(msg):
    if os.environ.get("WG_RESET_PEERS_DEBUG", 0) == "1":
        sys.stderr.write(msg + "\n")

class WGPeer:
    def __init__(self, interface, public_key, endpoint):
        self.interface = interface
        self.public_key = public_key
        self.endpoint = endpoint

    def set_endpoint(self):
        res = subprocess.run(
            [
                "wg",
                "set",
                self.interface,
                "peer",
                self.public_key,
                "endpoint",
                self.endpoint
            ],
            check=True
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} interface={self.interface} public_key={self.public_key} endpoint={self.endpoint}>"

class WGConfig:
    def __init__(self, path):
        self.path = path
        self.interface = os.path.splitext(os.path.basename(self.path))[0]

    def get_peers(self):
        def add_peer(public_key, endpoint):
            if public_key is not None and endpoint is not None:
                debug_msg(f"Adding peer {public_key} with endpoint {endpoint}")
                peers.append(WGPeer(self.interface, public_key, endpoint))
            return (None, None)

        peers = []
        public_key = None
        endpoint = None

        with open(self.path, "r") as fh:
            for line in fh:
                line = line.strip()
                if line == "[Peer]":
                    public_key, endpoint = add_peer(public_key, endpoint)
                elif line.startswith("PublicKey"):
                    public_key = line.split()[-1]
                elif line.startswith("Endpoint"):
                    endpoint = line.split()[-1]

            add_peer(public_key, endpoint)

        return peers

if __name__ == "__main__":
    for path in glob.glob("/etc/wireguard/*.conf"):
        debug_msg(f"Reading config {path}")
        config = WGConfig(path)
        for peer in config.get_peers():
            debug_msg(f"Resetting peer endpoint for {peer}")
            peer.set_endpoint()

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


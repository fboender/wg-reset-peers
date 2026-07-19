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

You can export the `WG_RESET_PEERS_DEBUG` environment variable to get some
debugging:

    $ export WG_RESET_PEERS_DEBUG=1
    $ ./wg-reset-peers.py 
    Reading config /etc/wireguard/wg0.conf
    Adding peer rf4k3f4k3f4k3f4k32S0JlF3uSTwPpCf4k3f4k3f4ke= with endpoint vpn.electricmonk.nl:51820
    Resetting peer endpoint for <WGPeer interface=wg0 public_key=rf4k3f4k3f4k3f4k32S0JlF3uSTwPpCf4k3f4k3f4ke= endpoint=vpn.electricmonk.nl:51820>

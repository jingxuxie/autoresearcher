#!/usr/bin/env python3
"""Small local TCP relay for WSL-to-Windows localhost services."""

from __future__ import annotations

import argparse
import selectors
import socket
import threading
from typing import Tuple


BUFFER_SIZE = 64 * 1024


def pipe(left: socket.socket, right: socket.socket) -> None:
    selector = selectors.DefaultSelector()
    left.setblocking(False)
    right.setblocking(False)
    selector.register(left, selectors.EVENT_READ, right)
    selector.register(right, selectors.EVENT_READ, left)
    try:
        while True:
            events = selector.select(timeout=60)
            if not events:
                continue
            for key, _ in events:
                source = key.fileobj
                target = key.data
                try:
                    chunk = source.recv(BUFFER_SIZE)
                except OSError:
                    return
                if not chunk:
                    return
                try:
                    target.sendall(chunk)
                except OSError:
                    return
    finally:
        selector.close()
        left.close()
        right.close()


def handle(client: socket.socket, target: Tuple[str, int]) -> None:
    try:
        upstream = socket.create_connection(target, timeout=10)
    except OSError:
        client.close()
        return
    pipe(client, upstream)


def main() -> int:
    parser = argparse.ArgumentParser(description="Forward one TCP port to another host/port.")
    parser.add_argument("--listen-host", required=True)
    parser.add_argument("--listen-port", type=int, required=True)
    parser.add_argument("--target-host", required=True)
    parser.add_argument("--target-port", type=int, required=True)
    args = parser.parse_args()

    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind((args.listen_host, args.listen_port))
    listen.listen(64)
    target = (args.target_host, args.target_port)
    print(f"tcp_relay listening on {args.listen_host}:{args.listen_port} -> {args.target_host}:{args.target_port}", flush=True)
    while True:
        client, _ = listen.accept()
        threading.Thread(target=handle, args=(client, target), daemon=True).start()


if __name__ == "__main__":
    raise SystemExit(main())

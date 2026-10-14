#!/usr/bin/env python3
"""CLI Account Management Tool for Moly-Viet.

Usage:
  python manage_accounts.py list
  python manage_accounts.py create --nickname "Player1" --password "123456" [--vip 8] [--beans 999999]
  python manage_accounts.py set-vip --user-id 10000002 [--level 8] [--beans 999999]
  python manage_accounts.py link-google --user-id 10000002 --sub "google_sub_123" [--email "user@gmail.com"]
  python manage_accounts.py reset-password --user-id 10000002 --password "newpass"
"""

from __future__ import annotations

import argparse
import json
import sys
from account_system import accounts, google_oidc


def main() -> None:
    parser = argparse.ArgumentParser(description="Moly-Viet Account Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all registered accounts")

    # create
    create_p = subparsers.add_parser("create", help="Create a new player account")
    create_p.add_argument("--nickname", default="Moly Viet", help="Character nickname")
    create_p.add_argument("--password", required=True, help="Account password")
    create_p.add_argument("--email", default=None, help="Optional email")
    create_p.add_argument("--google-id", default=None, help="Optional Google sub")
    create_p.add_argument("--vip", type=int, default=0, help="Initial VIP level (0-8)")
    create_p.add_argument("--beans", type=int, default=1000, help="Initial Gold Beans")

    # set-vip
    vip_p = subparsers.add_parser("set-vip", help="Set VIP status and beans")
    vip_p.add_argument("--user-id", type=int, required=True, help="User ID")
    vip_p.add_argument("--level", type=int, default=8, help="VIP level (default 8)")
    vip_p.add_argument("--beans", type=int, default=999999, help="Gold beans (default 999999)")
    vip_p.add_argument("--months", type=int, default=120, help="VIP months (default 120)")

    # link-google
    link_p = subparsers.add_parser("link-google", help="Link Google OAuth account")
    link_p.add_argument("--user-id", type=int, required=True, help="User ID")
    link_p.add_argument("--sub", required=True, help="Google subject / user ID")
    link_p.add_argument("--email", default=None, help="Google email")

    # reset-password
    pwd_p = subparsers.add_parser("reset-password", help="Reset account password")
    pwd_p.add_argument("--user-id", type=int, required=True, help="User ID")
    pwd_p.add_argument("--password", required=True, help="New password")

    # google-url
    subparsers.add_parser("google-url", help="Generate Google OAuth authorization URL")

    args = parser.parse_args()

    if args.command == "list":
        acc_list = accounts.list_accounts()
        print(f"Total Accounts: {len(acc_list)}\n")
        print(f"{'ID':<10} {'Nickname':<18} {'VIP':<5} {'Beans':<10} {'Email':<25} {'Google Linked'}")
        print("-" * 80)
        for acc in sorted(acc_list, key=lambda x: int(x.get("user_id", 0))):
            uid = acc.get("user_id")
            nick = acc.get("nickname", "")
            vip = f"Lv{acc.get('vip_level', 0)}"
            beans = str(acc.get("gold_beans", 0))
            email = acc.get("email") or "-"
            google = "YES" if acc.get("google_id") else "NO"
            print(f"{uid:<10} {nick:<18} {vip:<5} {beans:<10} {email:<25} {google}")

    elif args.command == "create":
        acc = accounts.create_account(
            password=args.password,
            nickname=args.nickname,
            email=args.email,
            google_id=args.google_id,
            vip_level=args.vip,
            gold_beans=args.beans,
        )
        print(f"Created Account ID: {acc['user_id']}")
        print(f"Nickname: {acc['nickname']}")
        print(f"VIP Level: {acc['vip_level']}")
        print(f"Gold Beans: {acc['gold_beans']}")

    elif args.command == "set-vip":
        ok = accounts.set_vip(
            user_id=args.user_id,
            vip_level=args.level,
            gold_beans=args.beans,
            months=args.months,
        )
        if ok:
            print(f"Updated VIP for User {args.user_id}: VIP {args.level}, Beans {args.beans}")
        else:
            print(f"Error: User {args.user_id} not found.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "link-google":
        ok = accounts.link_google(
            user_id=args.user_id,
            google_id=args.sub,
            email=args.email,
        )
        if ok:
            print(f"Linked Google ID '{args.sub}' to User {args.user_id}")
        else:
            print(f"Error: User {args.user_id} not found.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "reset-password":
        ok = accounts.update_account(args.user_id, {"password": args.password})
        if ok:
            print(f"Password reset successful for User {args.user_id}")
        else:
            print(f"Error: User {args.user_id} not found.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "google-url":
        url = google_oidc.build_authorization_url()
        print(f"Google OAuth Authorization URL:\n{url}")


if __name__ == "__main__":
    main()

import time
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.token.associated import get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.client import Token
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed

global session
session = requests.Session()

def sol_estimate(droplist, gas_cost=.002):
    return len(droplist) * gas_cost

def process_drop(to_public_key, counter, client, token_client, sender_token_account, amount2Drop):
    try_counter = 20
    print(f"Trying Drop for #{counter} | {to_public_key}")
    recipient_token_account = token_client.get_accounts_by_owner(owner=Pubkey.from_string(to_public_key))
    if len(recipient_token_account.value) > 0:
        recipient_token_account_pubkey = recipient_token_account.value[0].pubkey
        print(f"Sender token account existed: {recipient_token_account_pubkey}")
    else:
        recipient_token_account = None
        while recipient_token_account is None:
            if try_counter <= 0:
                print(f"FAILED FOR {to_public_key}.")
                with open('failed.txt', 'a') as f:
                    f.write(f"failed, {to_public_key}\n")
                return
            try:
                token_client.create_associated_token_account(owner=Pubkey.from_string(to_public_key))
                recipient_token_account = token_client.get_accounts_by_owner(owner=Pubkey.from_string(to_public_key))
                recipient_token_account_pubkey = recipient_token_account.value[0].pubkey
                print(f"Recipient token account created: {recipient_token_account_pubkey}")
                break
            except:
                print(f"Token account creation failed for {to_public_key}. Retrying...")
                try_counter -= 1
                time.sleep(1)
    confirmed_tx = None
    try_counter = 30
    while confirmed_tx is None:
        if try_counter < 0:
            print(f"FAILED FOR {to_public_key}.")
            with open('failed.txt', 'a') as f:
                f.write(f"failed, {to_public_key}\n")
            return
        try:
            transfer_tx = token_client.transfer(
                source=sender_token_account,
                dest=recipient_token_account_pubkey,
                owner=token_client.payer,
                amount=amount2Drop
            )
            print(f"Transfer transaction sent: {transfer_tx}")
            print("Monitoring For TX Confirmation...")
            confirmed_tx = client.confirm_transaction(transfer_tx.value, commitment=Confirmed)
            print(f"{counter}th transaction confirmed.")
            return confirmed_tx
        except Exception as e:
            print(f"Transaction failed for wallet {to_public_key} Number {counter}. Retrying...")
            time.sleep(1)
            print(e)
            try_counter -= 1


def main():
    parser = argparse.ArgumentParser(description='Solana Token Distribution Script')
    parser.add_argument('--rpc-url', type=str, required=True, help='RPC URL')
    parser.add_argument('--distro-wallet-pvkey', type=str, required=True, help='Distribution wallet private key')
    parser.add_argument('--token-address', type=str, required=True, help='Token address')
    parser.add_argument('--amount', type=int, required=True, help='Amount to drop (in lamports)')
    parser.add_argument('--droplist-file', type=str, required=True, help='Path to the droplist file')
    parser.add_argument('--num-executors', type=int, default=10, help='Number of executors for parallel processing')
    parser.add_argument('--mode', type=str, default='fast', choices=['fast', 'slow'], help='Distribution mode (fast or slow)')

    args = parser.parse_args()

    rpc_url = args.rpc_url
    distro_wallet_pvkey = args.distro_wallet_pvkey
    distro_keypair = Keypair.from_base58_string(distro_wallet_pvkey)
    token_address = args.token_address
    amount2Drop = args.amount

    with open(args.droplist_file, 'r') as f:
        dropList = [line.strip() for line in f]

    estimated_gas = sol_estimate(dropList)
    print(f"Estimated SOL gas: {estimated_gas}")
    user_input = input("Do you want to proceed with the token distribution? (y/n): ")
    if user_input.lower() != 'y':
        print("Token distribution cancelled.")
        return

    client = Client(rpc_url)
    token_client = Token(
        conn=client,
        pubkey=Pubkey.from_string(token_address),
        program_id=TOKEN_PROGRAM_ID,
        payer=distro_keypair
    )

    sender_token_account = get_associated_token_address(distro_keypair.pubkey(), Pubkey.from_string(token_address))
    print(f"Sender token account created: {sender_token_account}")

    if args.mode == 'fast':
        with ThreadPoolExecutor(max_workers=args.num_executors) as executor:
            futures = [executor.submit(process_drop, to_public_key, i, client,token_client, sender_token_account, amount2Drop) for i, to_public_key in enumerate(dropList)]
            for future in as_completed(futures):
                future.result()
    else:
        for i, to_public_key in enumerate(dropList):
            process_drop(to_public_key, i, client, token_client, sender_token_account, amount2Drop)

if __name__ == '__main__':
    main()
    
    # python script.py --rpc-url "https://mainnet.helius-rpc.com/?api-key=785d2698-60bd-45e2-a7f1-37f59e68cb08" --distro-wallet-pvkey "Distro_wallet_Private_key" --token-address "7JhmUcZrrfhyt5nTSu3AfsrUq2L9992a7AhwdSDxdoL2" --amount 10 --droplist-file droplist.txt --mode fast

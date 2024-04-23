# HampDropper-py

This Python script allows you to distribute Solana tokens to multiple recipients. It provides a command-line interface (CLI) for easy configuration and supports parallel processing for improved performance.

## Features

- Distribute Solana tokens to multiple recipients
- Fast distribution mode with parallel processing
- Slow distribution mode for processing one transaction at a time
- Automatic creation of recipient token accounts if they don't exist
- Retry mechanism for failed transactions
- Estimation of SOL gas cost before distribution
- Customizable number of executors for parallel processing

## Requirements

- Python +3.10
- solders library
- solana library
- spl library
- requests library

## Installation

1. Clone the repository:
```
git clone https://github.com/HampterFi/Bulk-SPL-Sender.git
```
2. Install the required dependencies:
```
pip install solders solana spl requests
```

## Usage
```
python script.py --rpc-url RPC_URL --distro-wallet-pvkey DISTRO_WALLET_PRIVATE_KEY --token-address TOKEN_ADDRESS --amount AMOUNT --droplist-file DROPLIST_FILE [--mode MODE] [--num-executors NUM_EXECUTORS]
```

### Arguments

- `--rpc-url`: RPC URL (required)
- `--distro-wallet-pvkey`: Distribution wallet private key (required)
- `--token-address`: Token address (required)
- `--amount`: Amount to drop in lamports (required)
- `--droplist-file`: Path to the file containing the list of recipient addresses (required)
- `--mode`: Distribution mode, either 'fast' (default) or 'slow'
- `--num-executors`: Number of executors for parallel processing (default: 10)

### Running Example
```python bulk_sender.py --rpc-url "https://api.mainnet-beta.solana.com" --distro-wallet-pvkey "Distro_wallet_Private_key" --token-address "7JhmUcZrrfhyt5nTSu3AfsrUq2L9992a7AhwdSDxdoL2" --amount 279427367 --droplist-file droplist.txt --mode fast --num-executors 20```

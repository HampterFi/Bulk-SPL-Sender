<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solana Token Distribution</title>
</head>
<body>
    <h1>HampDropper</h1>
    <p>This Python script allows you to distribute Solana tokens to multiple recipients. It provides a command-line interface (CLI) for easy configuration and supports parallel processing for improved performance.</p>
    
    <h2>Features</h2>
    <ul>
        <li>Distribute Solana tokens to multiple recipients</li>
        <li>Fast distribution mode with parallel processing</li>
        <li>Slow distribution mode for processing one transaction at a time</li>
        <li>Automatic creation of recipient token accounts if they don't exist</li>
        <li>Retry mechanism for failed transactions</li>
        <li>Estimation of SOL gas cost before distribution</li>
        <li>Customizable number of executors for parallel processing</li>
    </ul>
    
    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>solders library</li>
        <li>solana library</li>
        <li>spl library</li>
        <li>requests library</li>
    </ul>
    
    <h2>Installation</h2>
    <ol>
        <li>Clone the repository:</li>
        <pre><code>git clone https://github.com/your-username/solana-token-distribution.git</code></pre>
        <li>Install the required dependencies:</li>
        <pre><code>pip install solders solana spl requests</code></pre>
    </ol>
    
    <h2>Usage</h2>
    <pre><code>python script.py --rpc-url RPC_URL --distro-wallet-pvkey DISTRO_WALLET_PRIVATE_KEY --token-address TOKEN_ADDRESS --amount AMOUNT --droplist-file DROPLIST_FILE [--mode MODE] [--num-executors NUM_EXECUTORS]</code></pre>
    
    <h3>Arguments</h3>
    <ul>
        <li><code>--rpc-url</code>: RPC URL (required)</li>
        <li><code>--distro-wallet-pvkey</code>: Distribution wallet private key (required)</li>
        <li><code>--token-address</code>: Token address (required)</li>
        <li><code>--amount</code>: Amount to drop in lamports (required)</li>
        <li><code>--droplist-file</code>: Path to the file containing the list of recipient addresses (required)</li>
        <li><code>--mode</code>: Distribution mode, either 'fast' (default) or 'slow'</li>
        <li><code>--num-executors</code>: Number of executors for parallel processing (default: 10)</li>
    </ul>
    
    <h3>Example</h3>
    <pre><code>python script.py --rpc-url "https://mainnet.helius-rpc.com/?api-key=785d2698-60bd-45e2-a7f1-37f59e68cb08" --distro-wallet-pvkey "Distro_wallet_Private_key" --token-address "7JhmUcZrrfhyt5nTSu3AfsrUq2L9992a7AhwdSDxdoL2" --amount 100 --droplist-file droplist.txt --mode fast --num-executors 20</code></pre>
    
    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>

import requests
from web3 import Web3
import json

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
answer = True
to_address = ''

while answer:
    contract_address = input('Enter contract address or bnb, if you want to collect chain token: ')
    if contract_address == 'bnb':
        break
    contract_address = web3.toChecksumAddress(contract_address).lower()
    API_ENDPOINT = "https://api.bscscan.com/api?module=contract&action=getabi&address=" + str(contract_address)
    r = requests.get(url=API_ENDPOINT)
    response = r.json()
    abi = json.loads(response["result"])
    contract = web3.eth.contract(address=web3.toChecksumAddress(contract_address), abi=abi)
    if input(f'Do you want to collect {contract.functions.symbol().call()}?(y/N)').lower() == 'y':
        answer = False
    else:
        continue


def take_addresses_and_privates():
    accounts = {}

    with open('addresses.txt', 'r') as file:
        for line in file.readlines():
            address_private = line.split(':')
            accounts[address_private[0]] = address_private[1]

    return accounts


def send_tx(send_address: str, private_key: str):
    from_address = send_address
    private_key = private_key
    amount = contract.functions.balanceOf(from_address).call()
    nonce = web3.eth.getTransactionCount(from_address)

    tx = {
        'gas': 100000,
        'gasPrice': web3.toWei('10', 'gwei'),
        'nonce': nonce
    }

    token_tx = contract.functions.transfer(to_address, amount).buildTransaction(tx)
    sign_txn = web3.eth.account.signTransaction(token_tx, private_key=private_key)
    txn_hash = web3.eth.sendRawTransaction(sign_txn.rawTransaction)
    web3.eth.wait_for_transaction_receipt(txn_hash)
    print(sign_txn)


def main():
    global to_address
    to_address = input("Enter main address: ")
    accounts = take_addresses_and_privates()
    for address, key in accounts.items():
        send_tx(send_address=address, private_key=key)


if __name__ == '__main__':
    main()

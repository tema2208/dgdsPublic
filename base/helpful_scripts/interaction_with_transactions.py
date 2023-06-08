from web3 import Web3
import json


def connect_to_blockchain():
    json_file = get_json("infura_info.json")
    w3 = Web3(Web3.HTTPProvider(json_file["http_provider"]))
    return w3


def get_json(path):
    with open(path, "r") as file:
        info = json.load(file)
    return info


def get_recipient_wallet(transaction_address):
    w3 = connect_to_blockchain()
    tx_receipt = w3.eth.getTransactionReceipt(transaction_address)
    if tx_receipt:  # check that this is exist
        return tx_receipt["to"]

    return ""


def get_amount_of_transaction(transaction_address):
    w3 = connect_to_blockchain()
    transaction = w3.eth.getTransaction(transaction_address)
    if transaction:  # check that this is exist
        return w3.fromWei(transaction["value"], "ether")

    return -1


def check_transaction_status(transaction_address):
    w3 = connect_to_blockchain()
    tx_receipt = w3.eth.getTransactionReceipt(transaction_address)
    return tx_receipt is not None  # it is equivalent to previous code


def check_validity_of_transaction(transaction_address, developer_wallet, game_price):
    try:
        if not check_transaction_status(transaction_address):
            return (
                False,
                "Transactions in the process of being added to the blockchain, try your attempt later.",
            )

        recipient_wallet = get_recipient_wallet(transaction_address)
        if recipient_wallet != developer_wallet:
            return (
                False,
                "The recipient in this transaction is not the owner-developer of the game.",
            )

        amount_of_transaction = get_amount_of_transaction(transaction_address)
        if amount_of_transaction < game_price:
            return False, "You sent an amount less than the cost of the game."

        return True, "Congratulations you got your game!"
    except:
        return (
            False,
            "Oops, something worng, check your transaction address and network again.",
        )

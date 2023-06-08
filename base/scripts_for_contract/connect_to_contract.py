from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from eth_account import Account
from .developer_contract.interaction_with_developer_contract import DeveloperContract
from .buy_game_contract.interaction_with_buy_game_contract import BuyGameContract
from .customer_contract.interaction_with_customer_contract import CustomerContract


def read_json(path):
    with open(f"base/scripts_for_contract/{path}.json", "r") as file:
        info = json.load(file)
    return info


def get_deployed_contract(w3, contract_address, abi):
    contract = w3.eth.contract(address=contract_address, abi=abi)
    return contract


def create_web3_account(w3):
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # I have written this personal data here because it is convenient, but this is very bad practice to do it
    public_address = "0x99bc949975C4bd87D2a6d2a5043112C121EC68D1"
    private_key = "750bb8368c19376f2ddb57f78a4a810bc73789f7845a9f52a7651a444fd8fb84"

    account = Account.privateKeyToAccount(private_key)
    assert account.address.lower() == public_address.lower()

    return account


def convert_info_json(info, name):
    contract_address = info["contract_address"]
    w3 = Web3(Web3.HTTPProvider(info["http_provider"]))
    abi = read_json(f"{name}_contract/info/{contract_address}")["abi"]

    contract = get_deployed_contract(w3, contract_address, abi)
    account = create_web3_account(w3)
    return contract, account, w3


def get_web3_info(name):
    info = read_json(f"{name}_contract/info/{name}_contract_info")
    return convert_info_json(info, name)


def return_contract(contract_type):
    if contract_type == "Developer":
        name = "developer"
        contract, account, w3 = get_web3_info(name)
        return DeveloperContract(account, contract, w3)
    if contract_type == "BuyGame":
        name = "buy_game"
        contract, account, w3 = get_web3_info(name)
        return BuyGameContract(account, contract, w3)
    if contract_type == "Customer":
        name = "customer"
        contract, account, w3 = get_web3_info(name)
        return CustomerContract(account, contract, w3)

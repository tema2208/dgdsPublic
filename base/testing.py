from scripts_for_contract import connect_to_contract


def main():
    wallet_address = "0x99bc949975C4bd87D2a6d2a5043112C121EC68D1"
    customer_contract = connect_to_contract.return_contract("Customer")

    # sometimes u have to wait, because it takes time to load into blockchain, that's why sometimes token_id will be wrong
    game_id = 1
    token_id = customer_contract.createCustomerNFT(game_id, wallet_address)

    print(f"token id = {token_id}")

    info = customer_contract.get_gameId_from_tokenId(token_id)

    print(f"info = {info}")


main()

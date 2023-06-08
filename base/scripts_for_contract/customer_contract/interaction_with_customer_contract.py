class CustomerContract:
    def __init__(self, _account, _contract, _w3):
        self.account = _account
        self.contract = _contract
        self.w3 = _w3

    def create_customer_nft(self, gameId, owner):
        transaction = self.contract.functions.createCustomerNFT(
            owner, gameId
        ).buildTransaction(
            {
                "from": self.account.address,
                "gas": 200000,
                "gasPrice": self.w3.toWei("40", "gwei"),
                "nonce": self.w3.eth.getTransactionCount(self.account.address),
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.account.privateKey
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
        token_id = self.contract.functions.customerId().call()
        return token_id

    def get_tokenId(self):
        return self.contract.functions.customerId().call()

    def get_gameId_from_tokenId(self, tokenId):
        return self.contract.functions.getGameIdFromCustomerId(tokenId).call()

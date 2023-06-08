class DeveloperContract:
    def __init__(self, _account, _contract, _w3):
        self.account = _account
        self.contract = _contract
        self.w3 = _w3

    def create_developer_nft(self, metadata_uri, owner):
        transaction = self.contract.functions.createDeveloperNFT(
            metadata_uri, owner
        ).buildTransaction(
            {
                "from": self.account.address,
                "gas": 200000,
                "gasPrice": self.w3.toWei("40", "gwei"),
                "nonce": self.w3.eth.getTransactionCount(self.account.address) + 1,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.account.privateKey
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        token_id = self.contract.functions.tokenId().call()
        return token_id

    def get_tokenId(self):
        return self.contract.functions.tokenId().call()

    def get_metadata_from_tokenId(self, tokenId):
        return self.contract.functions.getMetadataFromID(tokenId).call()

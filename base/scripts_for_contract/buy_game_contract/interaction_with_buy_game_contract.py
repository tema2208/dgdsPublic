class BuyGameContract:
    def __init__(self, _account, _contract, _w3):
        self.account = _account
        self.contract = _contract
        self.w3 = _w3

    def make_transcation(
        self, eth_amount, developer_address, game_id, customer_address
    ):
        transaction = self.contract.functions.payAndRetrieveInformation(
            developer_address, game_id
        ).buildTransaction(
            {
                "from": customer_address,
                "value": eth_amount,
                "gas": 200000,
                "gasPrice": self.w3.toWei("40", "gwei"),
                "nonce": self.w3.eth.getTransactionCount(self.account.address) + 1,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.account.privateKey
        )

        transaction_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        transaction_receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash)

        # Check if the transaction was successful
        if transaction_receipt.status == 1:
            print("Transaction successful!")

            # Get the event logs from the transaction receipt
            event_logs = self.contract.events.InformationRetrieved().processReceipt(
                transaction_receipt
            )

            # Extract the retrieved information from the event logs
            information = event_logs[0].args.information

            return information
        else:
            print("Transaction failed.")

    def update_deployed_contract_address(self, contract_address):
        pass

import sys
sys.path.append('../')
from db_provider import query_action_records_gas_is_null, update_gas_by_tx, update_status_by_tx
from third_party_utils import get_gas_by_zkevm


def update_gas(network_id):
    tx_data_list = query_action_records_gas_is_null("MAINNET")
    for tx_data in tx_data_list:
        if tx_data["action_network_id"] == "zkEVM":
            gas_data = get_gas_by_zkevm(tx_data["tx_id"])
            if gas_data["gas"] is not None:
                update_gas_by_tx(network_id, tx_data["tx_id"], gas_data["gas"])
            else:
                update_status_by_tx(network_id, tx_data["tx_id"])


if __name__ == '__main__':
    print("#############################")

    if len(sys.argv) == 2:
        network_id = str(sys.argv[1]).upper()
        if network_id in ["MAINNET", "TESTNET", "DEVNET"]:
            update_gas(network_id)
        else:
            print("Error, network_id should be MAINNET, TESTNET or DEVNET")
            exit(1)
    else:
        print("Error, must put NETWORK_ID as arg")
        exit(1)

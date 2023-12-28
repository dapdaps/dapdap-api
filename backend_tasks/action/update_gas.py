import sys
sys.path.append('../../')
from db_provider import update_gas_by_tx, update_status_fail_by_tx, query_action_records
from third_party_utils import get_gas, get_status, get_gas_by_zkevm
from settings.config import settings


def update_gas():
    tx_data_list = query_action_records()
    for tx_data in tx_data_list:
        if tx_data["chain_id"] in settings.DAPDAP_COFING:
            url = settings.DAPDAP_COFING[tx_data["chain_id"]]["URL"]
            apikey = settings.DAPDAP_COFING[tx_data["chain_id"]]["APIKEY"]
            if 42161 == tx_data["chain_id"] or 1101 == tx_data["chain_id"]:
                gas_data = get_gas(tx_data["tx_id"], url, apikey)
                if gas_data["gas"] == "" and gas_data["status"] == "":
                    update_status_fail_by_tx(tx_data["tx_id"])
                else:
                    if gas_data["gas"] == "" and 1101 == tx_data["chain_id"]:
                        url = settings.DAPDAP_COFING[tx_data["chain_id"]]["SPARE_URL"]
                        gas_price = get_gas_by_zkevm(tx_data["tx_id"], url, apikey)
                        if gas_price == 0:
                            update_status_fail_by_tx(tx_data["tx_id"])
                            continue
                        else:
                            gas_data["gas"] = "{:.10f}".format(gas_data["gasUsed"] * gas_price)
                    update_gas_by_tx(tx_data["tx_id"], gas_data["gas"], gas_data["status"])
            else:
                status_data = get_status(tx_data["tx_id"], url, apikey)
                if status_data["status"] != "":
                    update_gas_by_tx(tx_data["tx_id"], status_data["gas"], status_data["status"])
        else:
            update_status_fail_by_tx(tx_data["tx_id"])


if __name__ == '__main__':
    print("##############START UPDATE GAS###############")
    update_gas()
    print("##############END UPDATE GAS###############")

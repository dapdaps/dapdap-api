import json
import requests


def get_gas_by_zkevm(tx):
    ret_data = {
        "gas": None,
        "status": ""
    }
    etherscan_query_url = "https://api-zkevm.polygonscan.com/api?module=proxy&action=eth_getTransactionReceipt&txhash=" + tx + "&apikey=R9W5WXT73IXX92X8ZGYYUZB3KH43YHTZX4"
    requests.packages.urllib3.disable_warnings()
    etherscan_query_ret = requests.get(url=etherscan_query_url, verify=False)
    etherscan_query_data = json.loads(etherscan_query_ret.text)
    if "result" in etherscan_query_data:
        result = etherscan_query_data["result"]
        if result is None:
            return ret_data
        if "gasUsed" in result and "effectiveGasPrice" in result:
            gas_data = int(result["gasUsed"], base=16)
            gas_price_data = int(result["effectiveGasPrice"], base=16) / 1000000000000000000
            ret_data["gas"] = "{:.8f}".format(gas_data * gas_price_data)
        if "status" in result:
            status_data = int(result["status"], base=16)
            if status_data == 1:
                ret_data["status"] = "Success"
            elif status_data == 0:
                ret_data["status"] = "Failed"
    return ret_data


if __name__ == '__main__':
    print("#############################")
    ret = get_gas_by_zkevm("0x8113ccfaec16c7417fae2b8c10e5f0cf461eb2d5ea216b11bfc1f698d6cbf345")
    print(ret)

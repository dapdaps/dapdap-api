import json
import requests


def get_gas(tx, url, apikey):
    ret_data = {
        "gas": "",
        "status": "",
        "gasUsed": 0
    }
    query_url = url + tx + "&apikey=" + apikey
    requests.packages.urllib3.disable_warnings()
    query_ret = requests.get(url=query_url, verify=False)
    query_data = json.loads(query_ret.text)
    if "result" in query_data:
        result = query_data["result"]
        if result is None:
            return ret_data
        if "gasUsed" in result:
            gas_data = int(result["gasUsed"], base=16)
            ret_data["gasUsed"] = gas_data
            if "effectiveGasPrice" in result:
                gas_price_data = int(result["effectiveGasPrice"], base=16) / 1000000000000000000
                ret_data["gas"] = "{:.10f}".format(gas_data * gas_price_data)
        if "status" in result and result["status"] != "":
            status_data = int(result["status"], base=16)
            if status_data == 1:
                ret_data["status"] = "Success"
            elif status_data == 0:
                ret_data["status"] = "Failed"
    return ret_data


def get_status(tx, url, apikey):
    ret_data = {
        "gas": "",
        "status": ""
    }
    try:
        query_url = url + tx + "&apikey=" + apikey
        requests.packages.urllib3.disable_warnings()
        query_ret = requests.get(url=query_url, verify=False)
        query_data = json.loads(query_ret.text)
        if "result" in query_data:
            result = query_data["result"]
            if result is None:
                return ret_data
            if "gasUsed" in result and "effectiveGasPrice" in result:
                gas_data = int(result["gasUsed"], base=16)
                gas_price_data = int(result["effectiveGasPrice"], base=16) / 1000000000000000000
                ret_data["gas"] = "{:.10f}".format(gas_data * gas_price_data)
            if "status" in result and result["status"] != "":
                status_data = int(result["status"], base=16)
                if status_data == 1:
                    ret_data["status"] = "Success"
                elif status_data == 0:
                    ret_data["status"] = "Failed"
    except Exception as e:
        print("error:", e)
    return ret_data


def get_gas_by_zkevm(tx, url, apikey):
    gas_price = 0
    query_url = url + tx + "&apikey=" + apikey
    requests.packages.urllib3.disable_warnings()
    query_ret = requests.get(url=query_url, verify=False)
    query_data = json.loads(query_ret.text)
    if "result" in query_data:
        result = query_data["result"]
        if result is None:
            return gas_price
        if "gas" in result and "gasPrice" in result:
            gas_price = int(result["gasPrice"], base=16) / 1000000000000000000
    return gas_price


if __name__ == '__main__':
    print("#############################")
    ret = get_gas("0xfb782cc8246a1307e556a075a90e0af04634b8a6da674cfe5d770a7e58e1a3b4", "https://api-zkevm.polygonscan.com/api?module=proxy&action=eth_getTransactionReceipt&txhash=", "R9W5WXT73IXX92X8ZGYYUZB3KH43YHTZX4")
    print(ret)

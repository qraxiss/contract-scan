from bs4 import BeautifulSoup
import inspect
import re

from ..base import CheckByResponse

from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/1ad00f3ac1694ee5b27921d22887fc46"))
contract_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]


def get_name(address):
    contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=contract_abi)
    return {
        'name': contract.functions.name().call(),
        'symbol': contract.functions.symbol().call()
    }

class EthScan(CheckByResponse):
    @classmethod
    def get_coin_informations(cls):
        return get_name(cls.contract)
    
        soup = BeautifulSoup(cls.ethscan_res.text, features="html.parser")
        title = soup.title.text
        for replace_str in ['\r', '\n', '\t', ' Token Tracker | Etherscan']:
            title = title.replace(replace_str, '')

        title = title.strip(' ')
        title = title.split(' | ')

        if len(title) == 1:
            title = title[0]
        else:
            title = title[1]

        symbol = re.search(r'\((.*?)\)', title).group(1)
        name = title.replace(f' ({symbol})', '')
        
        result = {
            'name': name,
            'symbol': symbol
        }
        
        return result
    @classmethod
    def ethscan(cls, contract):
        cls.contract = contract
        def _check_contains(cls, site, page, string):
            def _req(cls, site, page):
                url = cls.url[site](page)
                res = cls.get(url)
                cls.ethscan_res = res
                return res

            res = _req(cls, site, page)
            return not string in res.text

        method = inspect.stack()[0][3]
        return _check_contains(cls, method, contract, 'Invalid Token')
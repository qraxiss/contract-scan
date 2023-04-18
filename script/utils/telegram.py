from ..base import CheckByResponse
from helpers import CircleList, timeout

import inspect


import re


class Telegram(CheckByResponse):
    tokens = [
        "5830428208:AAEUMef43_80THkIkBPuBzTp4XHdIvjfcbk",
        "5868558898:AAExlOh5cueANlQX1ECTxK52k9tHvtpTOyE",
        "5774795789:AAEc-gmFa6XvTcCsIBrXq8HQK3SanTIuhlU",
        "5946551401:AAEFsV3YAr0kKi-ahyhQMOrQAQvhlj1Dpkg",
        "5646839184:AAFy7heZAjJBkBq-vnjFlAwxI_Br9xB-kWE",
        "5961281395:AAHJIYNxTfg8zSLHqpKgcSHe79afTYRzteU",
        "5496122360:AAHaxU6l3nL42dsamvpuWg_Sckbn6FYepJI",
        "5823307816:AAGIilPt1DuAi4GqI8jegolR6-L3IVnu6J8",
        "5800126234:AAEEaDhjdH1wvNXkIIjYsvtQCcvPS_I03yM",
        "5849966942:AAHylbmhp-bZ25-jLENkP5yOIH8vTJKyR_8",
        "5963204010:AAGcPsh0g0sTKjjDD5TMdJbVz64of4UOEu4",
        "5968815937:AAFo-2VWGQwbwfmuODejnE-CwNtc4fIGjds",
        "5980125469:AAH0W6G6RIL5vawz4A6vMJPrkli3YL43928",
        "5935873959:AAF089h3FH2VC2qBl8Rv8GSL75XN5NVodxo",
        "5857061983:AAEEazpJuJOHzNNSvwH3dSEISuyi0rQHmks",
        "5787194644:AAG8_kxLHT4j41YIbB7dNi6_6bjozg7wo0k",
        "5755067074:AAE1_aQOAWcCniBZiFUdWqf6jYHXEEgZOLc",
        "5971417003:AAGhBGs2v-a_pahIHbIX-jnSDOL2h9oj7Z0",
        "5874296770:AAGPndaKfmm8L7DMNAYGW9iZuhJXJO4lRks"
    ]

    bots = iter(CircleList([f"https://api.telegram.org/bot{token}/getChat" for token in tokens]))

    @property
    def bot_(self):
        return next(self.bots)

    
    # def _telegram(self, username) -> dict:
    #     return self.apiget(self.bot_, json={'chat_id':f'@{username}'})


    def telegram(self, username):
        method = inspect.stack()[0][3]
        if 32 > len(username) > 5 and '__' not in username and username[0] != '_':
            result, status = self._check_contains(method, username, '<meta property="twitter:image" content="https://telegram.org/img/t_logo.png">')
        else:
            result, status = False, 404
        return method, username, result, status
    

    # def telegram(self, username):
    #     method = inspect.stack()[0][3]
    #     c = 0
    #     while True:
    #         try:
    #             result = self._telegram(username)
    #         except Exception as e:
    #             result = e
    #         else:
    #             match result.status_code:
    #                 case 429:
    #                     c+=1
    #                     if c < len(self.bots):
    #                         continue
    #                 case 200:
    #                     result = True
    #                 case 400:
    #                     result = False
    #         break

    #     return method, username, result, None

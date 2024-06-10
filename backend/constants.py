from enum import Enum

from strenum import StrEnum


class WebApp(Enum):
    """Web App data"""

    ROOT_URL = "https://tonplex.up.railway.app/"


class Photo(StrEnum):
    """Photo links"""

    START = 'https://telegra.ph/file/202f01b20031cf146a773.jpg'


class CryptoLogo(StrEnum):
    """Crypto logo image links"""

    TON = 'https://res.coinpaper.com/coinpaper/toncoin_ton_logo_c5fb8b4302.png'


class SmartContractAddresses(StrEnum):
    """Smart contract addresses"""

    TON = 'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'

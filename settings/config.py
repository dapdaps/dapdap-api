# @Time : 10/7/23 1:58 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : config.py
import os


DATABASE_HOST = os.getenv('DATABASE_HOST') or "127.0.0.1"
DATABASE_NAME = os.getenv('DATABASE_NAME') or "dapdap"
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') or "jaki"
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD') or "root"
REDIS_HOST = os.getenv('REDIS_HOST') or "localhost"
REDIS_PORT = os.getenv('REDIS_PORT') or 6379
INVITE_CODE_QUANTITY = os.getenv('INVITE_CODE_QUANTITY') or 3
TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID') or ""
TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET') or ""
TWITTER_REDIRECT_URL = os.getenv('TWITTER_REDIRECT_URL') or ""
TWITTER_USER_ID = os.getenv('TWITTER_USER_ID') or 0
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME') or ""
TWITTER_TWEET_ID = os.getenv('TWITTER_TWEET_ID') or 0
TELEGRAM_BOT_ID = os.getenv('TELEGRAM_BOT_ID') or ""
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or ""
TELEGRAM_BOT_DOMAIN = os.getenv('TELEGRAM_BOT_DOMAIN') or ""
DISCORD_REDIRECT_URL = os.getenv('DISCORD_REDIRECT_URL') or ""
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID') or ""
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET') or ""
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME') or ""
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME') or ""
AWS_S3_AKI = os.getenv('AWS_S3_AKI') or ""
AWS_S3_SAK = os.getenv('AWS_S3_SAK') or ""
AWS_PATH = os.getenv('AWS_PATH') or ""
INVITE_LOGO = os.getenv('INVITE_LOGO') or ""
INVITE_TITLE = os.getenv('INVITE_TITLE') or "Invite Friends"
DAILY_CHECK_IN_LOGO = os.getenv('DAILY_CHECK_IN_LOGO') or ""
DAILY_CHECK_IN_TITLE = os.getenv('DAILY_CHECK_IN_TITLE') or "Daily Connect"

ETHERSCAN_API_KEY_TOKEN = os.getenv('ETHERSCAN_API_KEY_TOKEN') or ""
ZKEVM_API_KEY_TOKEN = os.getenv('ZKEVM_API_KEY_TOKEN') or ""
AVALANCHE_KEY = os.getenv('AVALANCHE_KEY') or ""
ARBITRUM_KEY = os.getenv('ARBITRUM_KEY') or ""
BSC_KEY = os.getenv('BSC_KEY') or ""
GNOSIS_KEY = os.getenv('GNOSIS_KEY') or ""
OPTIMISM_KEY = os.getenv('OPTIMISM_KEY') or ""
LINEA_KEY = os.getenv('LINEA_KEY') or ""
POLYGON_KEY = os.getenv('POLYGON_KEY') or ""
POLYGON_ZKEVM_KEY = os.getenv('POLYGON_ZKEVM_KEY') or ""
BASE_KEY = os.getenv('BASE_KEY') or ""

class Settings:
    VERSION = '0.1.0'
    APP_TITLE = 'dapdap-api'
    PROJECT_NAME = 'dapdap'
    APP_DESCRIPTION = 'dapdap-api'

    SERVER_HOST = 'localhost'

    DEBUG = True

    APPLICATIONS = [
        'user',
        'invite',
        # 'integral',
        'action',
        'uniswap_rpc',
        'dapp',
        'quest',
        'network',
        'ad',
    ]

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT = os.path.join(PROJECT_ROOT, "logs")
    # EMAIL_TEMPLATES_DIR = os.path.join(BASE_DIR, "app/templates/emails/build/")

    DB_URL = f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"
    DB_CONNECTIONS = {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'db_url': DB_URL,
            'credentials': {
                'host': DATABASE_HOST,
                'port': 5432,
                'user': DATABASE_USERNAME,
                'password': DATABASE_PASSWORD,
                'database': DATABASE_NAME,
            }
        },
    }

    SECRET_KEY = '665c3ffa948a78fbaccd71c44c7cca7b988013fe337e758c06b9faa5f2d6b71e'  # openssl rand -hex 32
    REFRESH_SECRET_KEY = '5e89bdc45ab0c611ca52668717e23509bff38021ae731847e1e162f605ef2119'  # openssl rand -hex 32
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 day
    JWT_REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 day

    EMAILS_FROM_NAME = ''
    EMAILS_FROM_EMAIL = ''
    SMTP_USER = ''
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_TLS = True
    SMTP_PASSWORD = ''
    EMAIL_RESET_TOKEN_EXPIRE_HOURS = 1
    EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL
    LOGIN_URL = SERVER_HOST + '/api/auth/login/access-token'

    RABBIT_LOGIN = 'guest'
    RABBIT_PASSWORD = ''
    RABBIT_HOST = 'localhost'

    REDIS_HOST = REDIS_HOST
    REDIS_PORT = REDIS_PORT

    # APPLICATIONS_MODULE = 'apps'
    APPLICATIONS_MODULE = 'apps'

    CORS_ORIGINS = [
        # "http://localhost",
        # "http://localhost:8080",
        # "http://localhost:5000",
        # "http://localhost:3000",
        "*"
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    ACTIVITY_REPORT_CHANGE = 0

    INVITE_CODE_QUANTITY = int(INVITE_CODE_QUANTITY)

    TWITTER_CLIENT_ID = TWITTER_CLIENT_ID
    TWITTER_CLIENT_SECRET = TWITTER_CLIENT_SECRET
    TWITTER_REDIRECT_URL = TWITTER_REDIRECT_URL
    TWITTER_USER_ID = TWITTER_USER_ID
    TWITTER_USERNAME = TWITTER_USERNAME
    TWITTER_TWEET_ID = int(TWITTER_TWEET_ID)
    TELEGRAM_BOT_ID = TELEGRAM_BOT_ID
    TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
    TELEGRAM_BOT_DOMAIN = TELEGRAM_BOT_DOMAIN
    DISCORD_REDIRECT_URL = DISCORD_REDIRECT_URL
    DISCORD_CLIENT_ID = DISCORD_CLIENT_ID
    DISCORD_CLIENT_SECRET = DISCORD_CLIENT_SECRET

    AWS_REGION_NAME = AWS_REGION_NAME
    AWS_BUCKET_NAME = AWS_BUCKET_NAME
    AWS_S3_AKI = AWS_S3_AKI
    AWS_S3_SAK = AWS_S3_SAK
    AWS_PATH = AWS_PATH

    INVITE_LOGO = INVITE_LOGO
    INVITE_TITLE = INVITE_TITLE
    DAILY_CHECK_IN_LOGO = DAILY_CHECK_IN_LOGO
    DAILY_CHECK_IN_TITLE = DAILY_CHECK_IN_TITLE

    DAPDAP_COFING = {
        43114: {
            "URL": "https://api.snowtrace.io/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": AVALANCHE_KEY,
        },
        42161: {
            "URL": "https://api.arbiscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash=",
            "APIKEY": ARBITRUM_KEY,
        },
        56: {
            "URL": "https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": BSC_KEY,
        },
        100: {
            "URL": "https://api.gnosisscan.io/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": GNOSIS_KEY,
        },
        59144: {
            "URL": "https://api.lineascan.build/api?module=proxy&action=eth_getTransactionReceipt&txhash=",
            "APIKEY": LINEA_KEY,
        },
        5000: {
            "URL": "https://explorer.mantle.xyz/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": "",
        },
        1088: {
            "URL": "https://andromeda-explorer.metis.io/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": "",
        },
        10: {
            "URL": "https://api-optimistic.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": OPTIMISM_KEY,
        },
        137: {
            "URL": "https://api.polygonscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=",
            "APIKEY": POLYGON_KEY,
        },
        1101: {
            "URL": "https://api-zkevm.polygonscan.com/api?module=proxy&action=eth_getTransactionReceipt&txhash=",
            "SPARE_URL": "https://api-zkevm.polygonscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash=",
            "APIKEY": POLYGON_ZKEVM_KEY,
        },
        8453: {
            "URL": "https://api.basescan.org/api?module=proxy&action=eth_getTransactionByHash&txhash=",
            "APIKEY": BASE_KEY,
        }
    }

settings = Settings()
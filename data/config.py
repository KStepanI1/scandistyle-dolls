
from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
SUPERUSER_ID = env.list("SUPERUSER_ID")
IP = env.str("IP")

PG_USER = env.str("POSTGRES_USER")
PG_PASSWORD = env.str("POSTGRES_PASSWORD")
DATABASE = env.str("POSTGRES_DATABASE")

QIWI_TOKEN = env.str("qiwi")
WALLET_QIWI = env.str("wallet")
QIWI_PUBKEY = env.str("qiwi_pub")

EMAIL_ADDRESS = env.str("EMAIL_ADDRESS")
EMAIL_PASSWORD = env.str("EMAIL_PASSWORD")


DB_HOST = IP


POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{DB_HOST}/{DATABASE}"

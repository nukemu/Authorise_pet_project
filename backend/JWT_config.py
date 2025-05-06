from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_SECRET_KEY = "my_secrete_key"
config.JWT_ACCESS_COOKIE_NAME = "youre_access_key"
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)
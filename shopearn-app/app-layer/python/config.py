from botocore.config import Config

ddb_config = Config(
    retries={
        'max_attempts': 7,
        'mode': 'standard'
    },
    read_timeout=20,
    connect_timeout=10,
)


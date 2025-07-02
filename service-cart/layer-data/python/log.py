from aws_lambda_powertools import Logger

class AppLogger(Logger):
    def structure_log(self, log: dict) -> dict:
        # Remove or mask fields
        log.pop("email", None)
        return log

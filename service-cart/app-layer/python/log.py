from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging.formatter import LambdaPowertoolsFormatter
from aws_lambda_powertools.logging.types import LogRecord


class AppLogger(Logger):
    pass


class LambdaLogFormatter(LambdaPowertoolsFormatter):
    def serialize(self, log: LogRecord) -> str:
        # TODO: implement wide log logic here
        # user = {k: v for k, v in log. if k.startswith("app_")}
        return self.json_serializer({
            "lv": log["level"],
            "ts": log["timestamp"],
            "gw": log["correlation_id"],
            "fn": f"{log['function_name']}[{log['function_memory_size']}]:{int(log['cold_start'])}",
            "msg": log["message"]
        })

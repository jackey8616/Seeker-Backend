from models.user.quota import ModelQuota


class ExecutionQuotaExceedError(Exception):
    def __init__(self, name: str, remaining_quotas: list[ModelQuota]):
        super().__init__()
        self.name = name
        self.remaining_quotas = remaining_quotas

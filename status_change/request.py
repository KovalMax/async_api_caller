class StatusChangeRequest:
    def __init__(self, mid: str, id_item: str, market: str, status: str, status_reason: str | None = None):
        self.mid = mid
        self.id_item = id_item
        self.market = market
        self.status = status
        self.status_reason = status_reason

    def to_json(self) -> dict[str, str | None]:
        json = {'status': self.status}
        if self.status_reason:
            json['statusReason'] = self.status_reason

        return json

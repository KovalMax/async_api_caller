from status_change.request import StatusChangeRequest


class StatusChangeResult:
    def __init__(self,
                 info: str,
                 req: StatusChangeRequest,
                 succeed: bool = False,
                 skip: bool = False):
        self.info = info
        self.req = req
        self.succeed = succeed
        self.skip = skip

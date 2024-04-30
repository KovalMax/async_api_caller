from golden_record.request import GoldenRecordRequest


class GoldenRecordResult:
    def __init__(self,
                 info: str,
                 req: GoldenRecordRequest,
                 succeed: bool = False,
                 skip: bool = False):
        self.info = info
        self.req = req
        self.succeed = succeed
        self.skip = skip

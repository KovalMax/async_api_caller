from client import BaseClient
from golden_record.request import GoldenRecordRequest
from golden_record.result import GoldenRecordResult


class GoldenRecordService:
    no_gr_info = '{mid}, GoldenRecord not found'
    error = '{mid}, {error}'
    connection_error = 'Calling {uri} failed for mid#{mid}, response code - {status}, body - {body}'

    def __init__(self, client: BaseClient):
        self.client = client

    async def get_no_gr(self, reqeust: GoldenRecordRequest) -> GoldenRecordResult:
        uri = self.client.get_gr_uri().format(mid=reqeust.mid)
        url = f'{self.client.get_gr_url()}/{uri}'

        try:
            response = await self.client.send_get(url)
            match response.status:
                case 404:
                    info = self.no_gr_info.format(mid=reqeust.mid)
                    result = GoldenRecordResult(succeed=True, info=info, req=reqeust)
                case 200:
                    result = GoldenRecordResult(succeed=True, info='', req=reqeust, skip=True)
                case _:
                    body = await response.text()
                    raise ConnectionError(
                        self.connection_error.format(uri=uri,
                                                     mid=reqeust.mid,
                                                     status=response.status,
                                                     body=body))
        except ConnectionError as api_error:
            result = GoldenRecordResult(info=str(api_error), req=reqeust)
        except Exception as e:
            error = str(e) if str(e) else e.__repr__()
            text = self.error.format(mid=reqeust.mid, error=error)

            result = GoldenRecordResult(info=text, req=reqeust)

        return result

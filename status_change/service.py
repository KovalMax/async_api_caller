from client import BaseClient
from status_change.request import StatusChangeRequest
from status_change.result import StatusChangeResult


class StatusChangeService:
    success = 'Status was changed for item with mid#{mid}, ' \
              'status changed to - {status},  market - {market},  status reason - {reason}'
    error = 'Error during change mid#{mid} - error is: {error}'

    def __init__(self, client: BaseClient):
        self.client = client

    async def change_status(self, reqeust: StatusChangeRequest) -> StatusChangeResult:
        uri = self.client.get_change_status_uri().format(id=reqeust.id_item, market=reqeust.market)
        url = f'{self.client.get_gr_url()}/{uri}'

        try:
            response = await self.client.send_put(url, reqeust.to_json())
            if response.status != 200:
                body = await response.text()
                raise ConnectionError(
                    f'Calling {uri} failed for mid#{reqeust.mid}, response code - {response.status}, body - {body}')

            reason = reqeust.status_reason if reqeust.status_reason else 'None'
            info = self.success.format(mid=reqeust.mid, status=reqeust.status, market=reqeust.market, reason=reason)

            result = StatusChangeResult(succeed=True, info=info, req=reqeust)
        except ConnectionError as api_error:
            result = StatusChangeResult(info=str(api_error), req=reqeust)
        except Exception as e:
            error = str(e) if str(e) else e.__repr__()

            result = StatusChangeResult(info=self.error.format(mid=reqeust.mid, error=error), req=reqeust)

        return result

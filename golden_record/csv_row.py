class CsvRow:
    __HEADERS = ['mid', 'id_item']

    def __init__(self, headers: list[str], values: list[str]):
        self.__validate_headers_are_present(headers)

        row = dict(zip(headers, values))
        self.mid = row.get('mid')
        self.id_item = row.get('id_item')

    def __validate_headers_are_present(self, headers: list[str]) -> None:
        for header in self.__HEADERS:
            if header not in headers:
                raise KeyError(f'Key {header} not found in headers')

    def __dict__(self) -> dict:
        return {'mid': self.mid, 'id_item': self.id_item}
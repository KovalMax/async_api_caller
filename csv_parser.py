import csv


class Row:
    __HEADERS = ['mid', 'id_item', 'market', 'status']

    def __init__(self, headers: list[str], values: list[str]):
        self.__validate_headers_are_present(headers)

        row = dict(zip(headers, values))
        self.mid = row.get('mid')
        self.id_item = row.get('id_item')
        self.market = row.get('market')
        self.status = row.get('status')
        self.status_reason = row.get('status_reason', None)

    def __validate_headers_are_present(self, headers: list[str]) -> None:
        for header in self.__HEADERS:
            if header not in headers:
                raise KeyError(f'Key {header} not found in headers')

    def __dict__(self) -> dict:
        return {'mid': self.mid, 'id_item': self.id_item, 'market': self.market, 'status': self.status,
                'status_reason': self.status_reason}


class CsvParser:
    def __init__(self, file_path: str, delimiter: str):
        self.delimiter = delimiter
        self.file_path = file_path

    def iterate(self) -> list[Row]:
        with open(self.file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter)
            headers = reader.__next__()
            for values in reader:
                yield Row(headers, values)

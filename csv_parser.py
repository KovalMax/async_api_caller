import csv


class ClassLoader:
    def __init__(self, module: str, sub_module: str, data_class: str):
        self.module = module
        self.sub_module = sub_module
        self.data_class = data_class


class CsvParser:
    def __init__(self, file_path: str, delimiter: str, loader: ClassLoader):
        self.delimiter = delimiter
        self.file_path = file_path
        self.loader = loader

    def iterate(self) -> list:
        module = __import__(self.loader.module)
        data_class = getattr(getattr(module, self.loader.sub_module), self.loader.data_class)

        with open(self.file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter)
            headers = reader.__next__()
            for values in reader:
                yield data_class(headers, values)

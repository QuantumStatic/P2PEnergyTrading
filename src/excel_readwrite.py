import sys
sys.path.append("/Users/utkarsh/Desktop/Utkarsh/Languages/Python/Modules/ExcelReader")
print('\n', sys.path, '\n')

from ExcelFileReader import ExcelFileReader
from myFunctions import execute_this
from typing import Union

writes = 0

def read_data_from_excel(name: str) -> dict[str, list]:
    with ExcelFileReader(f"{name}") as excel_reader:
        excel_reader.change_active_worksheet("Sheet3")
        col_headers = excel_reader.column_headers()
        all_data = dict.fromkeys(col_headers.keys())
        for col_header in all_data:
            all_data[col_header] = []
        for row in excel_reader.rows:
            for header in all_data:
                all_data[header].append(row[col_headers[header]].value)

    return all_data


def write_data_to_excel(name: str, data: Union[dict[str, list], list, tuple]) -> None:
    global writes

    with ExcelFileReader(f"{name}") as excel_reader:
        if isinstance(data, dict):
            col_headers = excel_reader.column_headers()
            for index, row in enumerate(excel_reader.rows):
                for header in data:
                    row[col_headers[header]].value = data[header][index]
        elif isinstance(data, list):
            for x, cell_value in enumerate(data):
                excel_reader[x+1, writes + 1] = cell_value
        else:
            raise TypeError("data must be a dict or a list")

        writes += 1
        excel_reader.save()


@execute_this
def main():
    pass

from rest_framework.parsers import BaseParser


class ExcelParser(BaseParser):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def parse(self, stream, media_type=None, parser_context=None):
        import pandas as pd
        return pd.read_excel(stream, engine='openpyxl')

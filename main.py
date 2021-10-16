import json
import re
import sys
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    string_io = StringIO()
    layout_analysis_params = LAParams()
    text_converter = TextConverter(
        resource_manager,
        string_io,
        laparams=layout_analysis_params
    )
    file_stream = open(path, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, text_converter)

    for page in PDFPage.get_pages(
            file_stream,
            maxpages=1,
            check_extractable=True
    ):
        interpreter.process_page(page)

    parsed_text = string_io.getvalue()

    file_stream.close()
    text_converter.close()
    string_io.close()
    return parsed_text


if __name__ == '__main__':

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        else:
            output_file = 'output.txt'
    else:
        input_file = 'certificate.pdf'
        output_file = 'output.txt'

    text = convert_pdf_to_txt(input_file)

    lines = text.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""

    text_rows = list()
    for line in non_empty_lines:
        line = line.lstrip(' \t')
        text_rows.append(line)

    if 'Сертификат о вакцинации COVID-19' not in text_rows:
        raise SystemExit('Неверный формат файла')

    last_name, first_name, middle_name = (
        re.sub(' +', ' ', text_rows[5])).split(' ')

    birthday = text_rows[text_rows.index('Дата рождения:') + 1]
    sex = text_rows[text_rows.index('Пол:') + 1]

    document = text_rows[
        text_rows.index('Документ удостоверяющий личность') + 1]

    last_vaccine_date = text_rows[max(
        index for index, item in enumerate(text_rows)
        if item == 'Дата введения вакцины:') + 1]

    preparation_row_index = max(
        index for index, item in enumerate(text_rows)
        if item == 'Препарат:')

    preparation = text_rows[preparation_row_index + 1] \
        + ' ' + text_rows[preparation_row_index + 2]

    return_dict = {
        'last_name': last_name,
        'first_name': first_name,
        'middle_name': middle_name,
        'birthday': birthday,
        'sex': sex,
        'document': document,
        'vaccine': {
            'date': last_vaccine_date,
            'preparation': preparation,
        },
    }

    json_date = json.dumps(return_dict, indent=4, ensure_ascii=False)

    f = open(output_file, "w+")
    f.write(json_date)
    f.close()

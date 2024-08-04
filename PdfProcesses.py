import pdfplumber
import re
import shutil
from fastapi import UploadFile
from pathlib import Path

class PdfProcesses():

    @staticmethod
    def read_pdf(file_path: str) -> dict:

        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        # Metni satırlara ayırın
        lines = text.split('\n')

        title = lines[4].strip()
        doc_code = lines[0].strip()
        doc_get_date = lines[1].split(' ')[1].strip()
        id_number = lines[5].split(':')[1].strip()
        name = lines[6].split(':')[1].strip()
        year = re.search(r'\d', lines[13]).group().strip()
        birthday = lines[9].split(':')[1].split('/')[0].strip()
        nation = lines[9].split(':')[1].split('/')[1].strip()

        school_info = (lines[14] + ' ' + lines[15]).split(':')[1].strip().split('/')

        university = school_info[0]
        faculty = school_info[1]
        department = school_info[2]
        program = school_info[3]

        output = dict()
        output.update({'title': title})
        output.update({'doc_code': doc_code})
        output.update({'doc_get_date': doc_get_date})
        output.update({'id_number': id_number})
        output.update({'name': name})
        output.update({'year': year})
        output.update({'birthday': birthday})
        output.update({'nation': nation})
        output.update({'university': university})
        output.update({'faculty': faculty})
        output.update({'department': department})
        output.update({'program': program})


        # print('title: ', title)
        # print('doc_code: ', doc_code)
        # print('doc_get_date: ', doc_get_date)

        # print('id_number: ', id_number)
        # print('name: ', name)
        # print('year: ', year)
        # print('birthday: ', birthday)
        # print('nation: ', nation)

        # print('university: ', university)
        # print('faculty: ', faculty)
        # print('department: ', department)
        # print('program: ', program)

        return output
    
    @staticmethod
    def save_pdf(file_path: str, file: UploadFile):
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)


    @staticmethod
    def delete_pdf(file_path: str):

        file = Path(file_path)

        if file.exists():
            file.unlink()


    @staticmethod
    def move_pdf(file_path: str, dest_file_name: str):
        file = Path(file_path)

        Path('permanent').mkdir(parents=True, exist_ok=True)

        dest_file = Path(f'permanent/{dest_file_name}')

        if dest_file.exists():
            dest_file.unlink()

        shutil.move(file, dest_file)
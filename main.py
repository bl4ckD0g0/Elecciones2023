
import fitz
import os, os.path as path
import sys
import requests
import shutil


def get_folder():
    url = 'https://resultados.generales23j.es/assets/files/congreso_municipios.zip'
    r = requests.get(url, allow_redirects= True)
    open('congreso_municipios.zip', 'wb').write(r.content)

    # Unzip the file
    shutil.unpack_archive(filename, extract_dir)


def process_folder(path_folder):
    files = os.listdir(path_folder)
    os.chdir(path_folder)

    output_folder = "..\\results"
    if not path.exists(output_folder):
        os.mkdir(output_folder)

    for file in files:
        process_doc(file, output_folder)

def process_doc(doc_name, output_path):
    doc = fitz.open(doc_name)

    page0 = doc[0]
    lines = page0.get_text().split('\n')
    out = open(output_path +'\\' + lines[2] + '.csv', "wb")
    out.write('Municipio; Número de votos; Porcentaje\n'.encode('utf8'))

    lines = lines[2:]
    process_page_words(lines, out)

    doc.delete_page(0)

    for page_number, page in enumerate(doc):
        text = page.get_text()
        lines = text.split('\n')
        process_page_words(lines, out)
    out.close()


def process_page_words(lines, out):
    municipio = lines[1]
    numero_votos = porcentaje = 0
    for j, line in enumerate(lines):
        if line == 'FO':
            numero_votos = lines[j + 1]
            porcentaje = lines[j + 2]
            break
    out.write('{} ;{} ;{} \n'.format(municipio, numero_votos, porcentaje).encode('utf8'))


if __name__ == '__main__':
    path_folder = sys.argv[1]
    get_folder()
    process_folder(path_folder)

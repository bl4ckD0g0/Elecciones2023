
import os
import os.path as path
from pathlib import Path

import fitz

CARPETA_MUNICIPIOS = 'congreso_municipios'
CARPETA_RESULTADOS = str(Path().absolute().joinpath('resultados'))


def process_folder():
    files = os.listdir(CARPETA_MUNICIPIOS)

    os.chdir(CARPETA_MUNICIPIOS)

    if not path.exists(CARPETA_RESULTADOS):
        os.mkdir(CARPETA_RESULTADOS)

    for file in files:
        print(file)
        if file.endswith('.pdf'):
            procesar_provincia(file)


def procesar_provincia(doc_name):
    doc = fitz.open(doc_name)
    current_folder = os.getcwd()
    os.chdir(CARPETA_RESULTADOS)

    page0 = doc[0]
    lines = page0.get_text().split('\n')

    nombre_provincia = lines[2].replace("/", "_")
    os.mkdir(nombre_provincia)
    os.chdir(nombre_provincia)








    # out = open(Path(OUTPUT_FOLDER).joinpath(nombre_municipio), "wb")
    # out.write('Municipio; Número de votos; Porcentaje\n'.encode('utf8'))
    #
    # lines = lines[2:]
    # procesar_municipio(lines, out)
    #
    # doc.delete_page(0)
    #
    # for page_number, page in enumerate(doc):
    #     text = page.get_text()
    #     lines = text.split('\n')
    #     procesar_municipio(lines, out)
    # out.close()

    os.chdir(current_folder)


def procesar_municipio(lines, out):
    municipio = lines[1]
    numero_votos = porcentaje = 0
    for j, line in enumerate(lines):
            numero_votos = lines[j + 1]
            porcentaje = lines[j + 2]
            break
    out.write('{} ;{} ;{} \n'.format(municipio, numero_votos, porcentaje).encode('utf8'))


if __name__ == '__main__':
    process_folder()

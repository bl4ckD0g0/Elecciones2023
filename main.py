import os
import os.path as path
import re
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

    lines = lines[2:]
    procesar_municipio(lines)

    doc.delete_page(0)

    for page_number, page in enumerate(doc):
        text = page.get_text()
        lines = text.split('\n')
        procesar_municipio(lines)

    os.chdir(current_folder)


def procesar_municipio(lines):
    municipio = lines[1].replace("/", "_")
    out = open(municipio + '.csv', "wb")
    out.write('Partido; Número de votos; Porcentaje\n'.encode('utf8'))
    ultimo_partido_leido = ''
    votos = porcentaje = 0

    j = lines.index('Candidaturas') + 6
    while j < len(lines):
        partido = lines[j]
        j += 1
        while re.search('[a-zA-Z]', lines[j]):
            partido += ' ' + lines[j]
            j += 1

        if partido != ultimo_partido_leido:
            votos = lines[j]
            porcentaje = lines[j + 1]

            out.write('{} ;{} ;{} \n'.format(partido, votos, porcentaje).encode('utf8'))
            ultimo_partido_leido = partido
            if j < len(lines) and not re.search('[a-zA-Z]', lines[j+2]):
                j += 6

        while j < len(lines) and not re.search('[a-zA-Z]', lines[j]):
            j += 1

    out.close()


if __name__ == '__main__':
    process_folder()

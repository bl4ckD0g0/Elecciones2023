
import fitz
import os, os.path as path
import requests
import shutil
from pathlib import Path

MSJ_INPUT_PARTIDOS = 'Indique el partido del que desea optener la clasificación de votos por municipios'
MUNICIPIOS_ZIP = 'congreso_municipios.zip'
CARPETA_MUNICIPIOS = 'congreso_municipios'
URL_MUNICIPIOS = 'https://resultados.generales23j.es/assets/files/congreso_municipios.zip'
TO_BE_DELETED_FILES = [MUNICIPIOS_ZIP, '__MACOSX']
OUTPUT_FOLDER = str(Path().absolute().joinpath('resultados'))
WEB_CANDIDATURAS = 'https://resultados.generales23j.es/es/resultados/0/0/20'

def get_folder():
    r = requests.get(URL_MUNICIPIOS)
    open(MUNICIPIOS_ZIP, 'wb').write(r.content)

    shutil.unpack_archive(MUNICIPIOS_ZIP)

    os.remove(TO_BE_DELETED_FILES[0])
    shutil.rmtree(TO_BE_DELETED_FILES[1])

def get_candidaturas():
    #candidaturas = {}
    resultados = requests.get(WEB_CANDIDATURAS)
    content = resultados.text
    #patron = "print:pl-0! flex break-inside-avoid items-center col-span-4 !pl-4 col-span-4"


    #return candidaturas
    return content


def seleccionar_partido():
    partidos = get_candidaturas()
    print(partidos)
    partido = input(MSJ_INPUT_PARTIDOS)
    if partido not in partidos:
        print("No se ha seleccionado un partido válido")
    return partido

def process_folder():
    files = os.listdir(CARPETA_MUNICIPIOS)

    if not path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    os.chdir(CARPETA_MUNICIPIOS)
    partido = seleccionar_partido()

    for file in files:
        print(file)
        if file.endswith('.pdf'):
            process_doc(file, partido)
        else:
            os.remove(file)


def process_doc(doc_name, partido):
    doc = fitz.open(doc_name)

    page0 = doc[0]
    lines = page0.get_text().split('\n')
    nombre_municipio = lines[2] + '.csv'
    out = open(Path(OUTPUT_FOLDER).joinpath(nombre_municipio), "wb")
    out.write('Municipio; Número de votos; Porcentaje\n'.encode('utf8'))

    lines = lines[2:]
    process_page_words(lines, out, partido)

    doc.delete_page(0)

    for page_number, page in enumerate(doc):
        text = page.get_text()
        lines = text.split('\n')
        process_page_words(lines, out, partido)
    out.close()


def process_page_words(lines, out, partido):
    municipio = lines[1]
    numero_votos = porcentaje = 0
    for j, line in enumerate(lines):
        if line == partido:
            numero_votos = lines[j + 1]
            porcentaje = lines[j + 2]
            break
    out.write('{} ;{} ;{} \n'.format(municipio, numero_votos, porcentaje).encode('utf8'))


if __name__ == '__main__':
    get_folder()
    process_folder()
    #print(get_candidaturas())

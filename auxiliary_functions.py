import json

TITLES_TO_REMOVE = [
    'ADMINISTRACIÓN DE NEGOCIOS',
    'CONTADOR PUBLICO Y AUDITOR',
    'CONTADURÍA PÚBLICA',
    'CONTADURÍA PÚBLICA Y ESTRATEGIA FINANCIERA',
    'INGENIERÍA EN COMPUTACIÓN',
]


def analyze_scraper_results(alumni):
    total_titles = 0
    double_title_count = 0
    triple_title_names = []
    for name, degree_year_list in alumni.items():
        total_titles += len(degree_year_list)
        if len(degree_year_list) == 2:
            double_title_count += 1
        elif len(degree_year_list) == 3:
            triple_title_names.append(name)
    print('\nResultados obtenidos del scraper:')
    print(f'Total alumnos titulados: {len(alumni)}')
    print(f'Total títulos: {total_titles}')
    print(f'Alumnos con doble titulación: {double_title_count}')
    print(f'Alumnos con triple titulación: {len(triple_title_names)}')
    for name in triple_title_names:
        print(f'\t{name}')
        for degree in alumni[name]:
            print(f'\t\t{degree}')


def filter_alumni(alumni):
    # Seleccionar exclusivamente a los alumnos cuyo nombre está formado por tres palabras
    total_titles = 0
    titles_3_count = 0
    alumni_3 = {}
    for name, degree_year_list in alumni.items():
        if len(name.split(' ')) == 3:
            alumni_3[name] = degree_year_list
            titles_3_count += len(degree_year_list)
        total_titles += len(degree_year_list)

    # Filtrar los títulos cuyo nombre no coincide con el de la SEP
    title_count = 0
    alumni_3_sep = {}
    for name, degree_year_list in alumni_3.items():
        filtered_list = []
        for degree_year in degree_year_list:
            if degree_year[0] not in TITLES_TO_REMOVE:
                filtered_list.append(degree_year)
                title_count += 1
        if filtered_list:
            alumni_3_sep[name] = filtered_list

    # Imprimir resultados
    print('\n\nResultados del filtro:')
    print(f'Alumnos con nombre de tres palabras: {len(alumni_3)}')
    print(f'Títulos pertenecientes a alumnos con nombre de tres palabras: {titles_3_count}')
    print(f'Alumnos con nombre de tres palabras con título cuyo nombre coincide con la SEP: {len(alumni_3_sep)}')
    print(f'Número de títulos restantes: {title_count}')

    return alumni_3_sep


def restructure_alumni(alumni):
    restructured_alumni = {}
    for name, degree_year_list in alumni.items():
        name_split = name.split(' ')
        restructured_alumni[name] = {}
        # Construir los parámetros para usar la API
        restructured_alumni[name]['api_input'] = {}
        restructured_alumni[name]['api_input']['json'] = json.dumps(
            dict(
                maxResult='1000',
                nombre=name_split[2],
                paterno=name_split[0],
                materno=name_split[1],
                idCedula='',
            )
        )
        restructured_alumni[name]['degrees'] = [dict(title_name=dy[0], year=dy[1]) for dy in degree_year_list]
    return restructured_alumni


def analyze_api_results(alumni):
    empty_responses = 0
    matched_degrees = 0
    unmatched_degrees = 0
    unmatched_degrees_due_to_empty_response = 0
    for name, info in alumni.items():
        items = info['api_output']['items']
        if len(items) == 0:
            empty_responses += 1
        for degree in info['degrees']:
            if 'idCedula' in degree:
                matched_degrees += 1
            else:
                unmatched_degrees += 1
                if len(items) == 0:
                    unmatched_degrees_due_to_empty_response += 1
                    # print(f'{name} (sin resultados) {degree["year"]}')
                else:
                    # print(f'{name} (con resultados) {degree["year"]}')

    # Imprimir resultados
    print('\n\nResultados obtenidos de la API:')
    print(f'Total de alumnos buscados: {len(alumni)}')
    print(f'Total de alumnos con respuesta vacía: {empty_responses}')
    print(f'Total de títulos: {matched_degrees + unmatched_degrees}')
    print(f'Total de títulos con cédula: {matched_degrees}')
    print(f'Total de títulos sin cédula: {unmatched_degrees}')
    print(
        'Total de títulos sin cédula (por respuesta vacía): '
        f'{unmatched_degrees_due_to_empty_response} de {unmatched_degrees}'
    )

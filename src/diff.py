import converter


# command
def diff_service_lists(args):
    path0 = converter.verify_path(args[0], [converter.CSV_SUFFIX,
                                            converter.XML_SUFFIX])
    path1 = converter.verify_path(args[1], [converter.CSV_SUFFIX,
                                            converter.XML_SUFFIX])
    s_list1 = converter.from_file(args[0], path0.suffix)
    s_list2 = converter.from_file(args[1], path1.suffix)



'''
{
    "diff": [
        {
            "name": "",
            "value1": "",
            "value2": ""
        }
    ],
    "eq": [
        ""
    ],
    "not": [
        {
            "name": "",
            "description": ""
        }
    ]
}
'''
# TODO Crear HTML y CSS para mostrar los resultados de la comparación
# TODO Comparar las 2 listas de objetos
# TODO Crear JSON con los resultados de la comparación
# TODO Guardar archivos JSON

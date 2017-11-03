from lib.hashlib.sha512 import sha512 as hash


def parser_insee(row):
    other = {}
    other_data = [
        'I_Code_Arrondissements',
        'I_Ar',
        'I_Cheflieu',
        'I_Code_canton',
        'I_Region',
        'I_Dep',
        'I_Canton',
        'I_Typct',
        'I_Burcentral',
        'I_Tncc',
        'I_Artmaj',
        'I_Ncc',
        'I_Armin',
        'I_Nccenr',
        'I_Nccent',
        'InseeXls_CodeCommune',
        'InseeXls_NameCommune',
        'InseeXls_Population',
        'I_Code_departament'
        'ColResultInSnipet'
    ]
    for name_column in other_data:
        try:
            value = row[name_column]
        except KeyError:
            continue
        if value not in ['', 'None']:
            other.update({name_column: value})
    code = hash().make(hash().make(row))
    other.update(code=code)

    if row.get('I_Nccenr'):
        other.update(name=row.get('I_Nccenr'))
    if row.get('I_Nccent'):
        other.update(name=row.get('I_Nccent'))
    elif row.get('InseeXls_NameCommune'):
        other.update(name=row.get('InseeXls_NameCommune'))

    return other
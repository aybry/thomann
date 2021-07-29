import json
import os
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thomann.settings")

import django

django.setup()

from lookup_hub import models


def main():
    DICTIONARY_FP = '/home/aybry/dictionary.jsonl'
    LANGUAGES = ['en', 'de', 'nl']

    expect_category = False
    cat_counter = 0
    row_counter = 0
    category = None
    dictionary = models.Dictionary.objects.get(name='hub')

    with open(DICTIONARY_FP, 'r') as dict_f:
        for line in dict_f.readlines():
            row = json.loads(line)
            print(row)

            if (row['en'].get('colour') == '#0600CE'
                or np.sum([
                    [(row[lang]['text'] is None or
                        row[lang]['text'].strip() == '') for lang in LANGUAGES]
                    ]) == 2):

                print(f'\nen: {row["en"].get("text")}')
                print(f'de: {row["de"].get("text")}')
                print(f'nl: {row["nl"].get("text")}\n')
                text = row["de"]["text"]

                feedback = input(f'[c]ategory, [r]ow, [s]kip\n')

                if feedback in ['c', '']:
                    print(json.dumps(row, indent=2))
                    text = row['de']['text']
                    if feedback != '':
                        language = input('Enter language (leave blank for \'de\'):')
                        if language in ['en', 'nl']:
                            text = row[language][language]

                    category = models.Category(name=text,
                                                dictionary=dictionary,
                                                order=cat_counter)
                    category.save()
                    cat_counter += 1
                    row_counter = 0
                    continue
                elif feedback == 'r':
                    pass
                elif feedback == 's':
                    continue


            row_instance = models.Row(order=row_counter,
                                    category=category)
            row_instance.save()
            row_counter += 1

            for lang in LANGUAGES:
                if (row[lang]['text'] == ''
                    and row[lang].get('comment') is None
                    and row[lang].get('colour') in ['', None]):
                    continue
                else:
                    entry = models.Cell(
                        language=lang,
                        row=row_instance,
                        text=row[lang].get('text'),
                        comment=row[lang].get('comment'),
                        colour=row[lang].get('colour'),
                    )
                    entry.save()

main()

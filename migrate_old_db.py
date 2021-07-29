import json
import os
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thomann.settings.dev")

import django

django.setup()

from lookup_hub import models


def main():
    DICTIONARY_FP = "/home/aybry/dictionary.jsonl"
    LANGUAGES = ["en", "de", "nl"]

    cat_counter = 0
    category = None

    with open(DICTIONARY_FP, "r") as dict_f:
        for line in dict_f.readlines():
            row = json.loads(line)
            print(row)

            # input()

            if (row["en"].get("colour") == "#0600CE"
                or np.sum([
                    [(row[lang]["text"] is None or
                        row[lang]["text"].strip() == "") for lang in LANGUAGES]
                    ]) == 2):

                print(f"\nen: {row['en'].get('text')}")
                print(f"de: {row['de'].get('text')}")
                print(f"nl: {row['nl'].get('text')}\n")
                text = row["de"]["text"]

                feedback = input(f"[c]ategory, [r]ow, [s]kip\n")

                if feedback in ["c", ""]:
                    print(json.dumps(row, indent=2))
                    text = row["de"]["text"]
                    category = models.Category(name=text)
                    category.save()
                    cat_counter += 1
                    continue
                elif feedback == "r":
                    pass
                elif feedback == "s":
                    continue

            vars = dict(
                en_text = row["en"].get("text"),
                en_comment = row["en"].get("comment"),
                en_colour = row["en"].get("colour"),
                de_text = row["de"].get("text"),
                de_comment = row["de"].get("comment"),
                de_colour = row["de"].get("colour"),
                nl_text = row["nl"].get("text"),
                nl_comment = row["nl"].get("comment"),
                nl_colour = row["nl"].get("colour"),
            )
            for key in [
                "en_text",
                "en_comment",
                "en_colour",
                "de_text",
                "de_comment",
                "de_colour",
                "nl_text",
                "nl_comment",
                "nl_colour"
            ]:
                if vars[key] is None:
                    vars[key] = ""
                if "colour" in key:
                    vars[key] = vars[key].replace("#", "")

            row_instance = models.Row(
                category=category,
                en_text=vars["en_text"],
                en_comment=vars["en_comment"],
                en_colour=vars["en_colour"],
                de_text=vars["de_text"],
                de_comment=vars["de_comment"],
                de_colour=vars["de_colour"],
                nl_text=vars["nl_text"],
                nl_comment=vars["nl_comment"],
                nl_colour=vars["nl_colour"],
            )
            row_instance.save()

main()

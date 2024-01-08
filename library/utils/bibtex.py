from django.db.models import QuerySet

from library.models import Paper


def papers_to_bibtex_file(query: QuerySet[Paper])->str:
    code = "% Encoding: UTF-8\n\n"
    for paper in query.order_by("citation_key"):
        code += paper.bibtex + "\n\n"

    code += "@Comment{jabref-meta: databaseType:biblatex;}\n"
    return code

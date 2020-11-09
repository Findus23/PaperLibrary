from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction

from library.models import Author, Paper, AuthorAlias


class Command(BaseCommand):
    help = 'merge multiple authors into one'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        name = options["name"]
        matching_authors: List[Author] = Author.objects.filter(name__icontains=name).order_by("name")
        if len(matching_authors) < 2:
            print("didn't find multiple authors")
            exit()
        for number, author in enumerate(matching_authors, start=1):
            print(f"{number}: {author}")
        picked = int(input("which entry to keep? "))
        if not (0 < picked <= len(matching_authors)):
            raise ValueError("invalid number")
        main_author = matching_authors[picked - 1]
        other_authors = [a for a in matching_authors if a != main_author]
        yesno = input(f"really delete {other_authors}? ")
        if yesno.lower() not in ["y"]:
            print("abort")
            exit()
        with transaction.atomic():
            for other_author in other_authors:
                paper: Paper
                for paper in other_author.papers.all():
                    print(f"reattribute {paper}")
                    main_author.papers.add(paper)
                    other_author.papers.remove(paper)
                for paper in other_author.first_author_papers.all():
                    print(f"reattribute (first author) {paper}")
                    paper.first_author = main_author
                    paper.save()
                print("create alias")
                alias = AuthorAlias.objects.create(name=other_author.name, author=main_author)
                print(f"delete {other_author}")
                other_author.delete()

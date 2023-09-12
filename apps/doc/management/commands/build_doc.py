from django.core.management.base import BaseCommand

from docdundee.docparser import (
    parse_docstrings,
    parse_functions,
    write_docstrings,
)


class Command(BaseCommand):
    help = "Build the doc from docstrings"

    def handle(self, *args, **options):
        print("Processing")
        ds = parse_functions("skii.account.api")
        doc = parse_docstrings(ds)
        # this will write to the docsite assets
        write_docstrings(
            "./docsite/public/doc/account_app/endpoints/docstrings.json", doc
        )
        ds = parse_functions("skii.account.schemas")
        doc = parse_docstrings(ds)
        # this will write to the docsite assets
        write_docstrings(
            "./docsite/public/doc/account_app/schemas/docstrings.json", doc
        )
        ds = parse_functions("skii.base.schemas")
        doc = parse_docstrings(ds)
        # this will write to the docsite assets
        write_docstrings("./docsite/public/doc/base_app/schemas/docstrings.json", doc)
        ds = parse_functions("skii.account.utils.email")
        doc = parse_docstrings(ds)
        # this will write to the docsite assets
        write_docstrings(
            "./docsite/public/doc/account_app/utilities/email/docstrings.json", doc
        )
        ds = parse_functions("skii.account.utils.token")
        doc = parse_docstrings(ds)
        # this will write to the docsite assets
        write_docstrings(
            "./docsite/public/doc/account_app/utilities/token/docstrings.json", doc
        )
        print("done")

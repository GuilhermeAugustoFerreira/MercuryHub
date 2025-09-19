from django.core.management.base import BaseCommand, CommandError

from MaterialGlobal.sap_rfc import (
    get_connection,
    fetch_material_groups_with_texts,
)


class Command(BaseCommand):
    help = "Fetch T023/T023T via RFC and print first results"

    def add_arguments(self, parser):
        parser.add_argument(
            "--langs",
            default="P,E",
            help="Comma-separated languages for T023T (default: P,E)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Number of rows to display (default: 10)",
        )

    def handle(self, *args, **options):
        langs = [l.strip() for l in str(options["langs"]).split(",") if l.strip()]
        limit = int(options["limit"])

        try:
            conn = get_connection()
        except Exception as exc:
            raise CommandError(f"Failed to create SAP connection: {exc}")

        try:
            data = fetch_material_groups_with_texts(langs=langs, connection=conn)
        except Exception as exc:
            raise CommandError(f"RFC_READ_TABLE failed: {exc}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

        count = 0
        for matkl, info in data.items():
            texts = info.get("texts", {})
            spart = info.get("SPART", "")
            # Format: MATKL [SPART] -> {lang:text, ...}
            text_pairs = ", ".join(f"{k}:{v}" for k, v in texts.items())
            self.stdout.write(f"{matkl} [{spart}] -> {text_pairs}")
            count += 1
            if count >= limit:
                break

        self.stdout.write(self.style.SUCCESS(f"Displayed {min(limit, len(data))} entries."))


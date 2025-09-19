from django.core.management.base import BaseCommand, CommandError

from MaterialGlobal.sap_rfc import get_connection, read_table



class Command(BaseCommand):
    help = "Fetch MATKL values from T023 via RFC and print first results"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Number of MATKL values to display (default: 10)",
        )

    def handle(self, *args, **options):
        limit = int(options["limit"]) or 10

        try:
            conn = get_connection()
        except Exception as exc:
            raise CommandError(f"Failed to create SAP connection: {exc}")

        try:
            rows = read_table(
                "T023",
                fields=["MATKL"],
                rowcount=limit,
                connection=conn,
            )
        except Exception as exc:
            raise CommandError(f"RFC_READ_TABLE failed: {exc}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

        for r in rows:
            self.stdout.write(r.get("MATKL", ""))

        self.stdout.write(self.style.SUCCESS(f"Displayed {len(rows)} MATKL values."))


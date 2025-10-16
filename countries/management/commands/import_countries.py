import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from countries.models import Country

class Command(BaseCommand):
    help = "Import countries from Excel (robust, uses pandas)"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "data", "countries_30.xlsx")
        self.stdout.write(f"Looking for file: {file_path}")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found. Put countries_30.xlsx into the data/ folder."))
            return

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel: {e}"))
            return

        self.stdout.write(f"Columns found: {list(df.columns)}")
        total = len(df)
        self.stdout.write(f"Rows in file: {total}")

        created = 0
        skipped = 0

        for idx, row in df.iterrows():
            # moslashuvchan nomlarni tekshiradi (davlat nomi uchun birorta topadi)
            name = row.get('Davlat') or row.get('name') or row.get('Country') or row.get('CountryName')
            capital = row.get('Poytaxt') or row.get('capital') or row.get('Capital')
            population = row.get('Aholi') or row.get('population') or row.get('Population')
            area = row.get('Maydon_km2') or row.get('area') or row.get('Area')

            if not name or str(name).strip() == "":
                self.stdout.write(self.style.WARNING(f"Row {idx+2} skipped — empty name"))
                skipped += 1
                continue

            # tiplarni tozalash
            try:
                population = int(population) if pd.notna(population) else None
            except:
                population = None
            try:
                area = float(area) if pd.notna(area) else None
            except:
                area = None

            obj, was_created = Country.objects.get_or_create(
                name=str(name).strip(),
                defaults={
                    "capital": str(capital).strip() if capital and pd.notna(capital) else "",
                    "population": population,
                    "area": area
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Skipped: {skipped}, Total rows: {total}"))

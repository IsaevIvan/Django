import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with open('phones.csv', 'r', encoding='utf-8') as file:
                phones = list(csv.DictReader(file, delimiter=';'))

            for phone_data in phones:
                try:

                    phone_id = int(phone_data['id'])
                    name = phone_data['name']
                    image = phone_data['image']
                    price = int(phone_data['price'])
                    release_date = phone_data['release_date']
                    lte_exists = phone_data['lte_exists'].lower() == 'true'


                    phone = Phone(
                        id=phone_id,
                        name=name,
                        image=image,
                        price=price,
                        release_date=release_date,
                        lte_exists=lte_exists,
                    )


                    if not phone.slug:
                        phone.slug = slugify(name)

                    phone.save()

                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully imported phone: {name}")
                    )

                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error importing phone: {phone_data}. ValueError: {e}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error importing phone: {phone_data}. Exception: {e}")
                    )

            self.stdout.write(self.style.SUCCESS("Successfully imported all phones."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("The file 'phones.csv' was not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
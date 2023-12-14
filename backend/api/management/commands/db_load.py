from django.core.management.base import BaseCommand
from api.models import DBSongs
import csv

class Command(BaseCommand):
    help = 'My custom management command for DB Load'

    def handle(self, *args, **options):
        
        csv_file_path = 'spotify-2023.csv'
        with open(csv_file_path, 'r', encoding='ISO-8859-1') as file:
            # Create a CSV reader object
            
            csv_reader = csv.reader(file)

            # Iterate through each row in the CSV file
            i=0
            for row in csv_reader:
                # Each 'row' is a list containing the values in that row
                if i==0:
                    pass
                else:
                    entry = DBSongs.objects.create(
                        song_name = row[0],
                        artist_name = row[1],
                        bpm = row[14],
                        key = row[15],
                        mode = row[16],
                        danceability = row[17],
                        valence = row[18],
                        energy = row[19],
                        acousticness = row[20],
                        instrumentalness = row[21],
                        liveness = row[22],
                        speechiness = row[23]
                    )
                    entry.save()
                i=1
        self.stdout.write(self.style.SUCCESS('Successfully ran the command'))
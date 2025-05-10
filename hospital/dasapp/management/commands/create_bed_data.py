from django.core.management.base import BaseCommand
from dasapp.models import Ward, BedType, Bed

class Command(BaseCommand):
    help = 'Creates sample data for bed management system'

    def handle(self, *args, **kwargs):
        # Check if data already exists
        if Ward.objects.count() > 0 or BedType.objects.count() > 0 or Bed.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Sample data already exists, skipping creation'))
            return
        
        self.stdout.write('Creating sample bed management data...')
        
        # Create wards
        wards = [
            Ward(name='General Ward', description='For patients requiring general medical care'),
            Ward(name='Private Ward', description='Private rooms for patients who require privacy'),
            Ward(name='ICU', description='Intensive Care Unit for critically ill patients'),
            Ward(name='Pediatric Ward', description='For children and adolescents'),
            Ward(name='Maternity Ward', description='For expectant and new mothers'),
            Ward(name='Emergency Ward', description='For emergency and trauma patients')
        ]
        
        Ward.objects.bulk_create(wards)
        self.stdout.write(self.style.SUCCESS(f'Created {len(wards)} wards'))
        
        # Create bed types
        bed_types = [
            BedType(name='Standard', description='Standard hospital bed'),
            BedType(name='Deluxe', description='Deluxe bed with additional comfort features'),
            BedType(name='ICU Bed', description='Specialized bed for intensive care'),
            BedType(name='Pediatric Bed', description='Specialized bed for children'),
            BedType(name='Birthing Bed', description='Specialized bed for labor and delivery'),
            BedType(name='Emergency Bed', description='Bed for emergency care')
        ]
        
        BedType.objects.bulk_create(bed_types)
        self.stdout.write(self.style.SUCCESS(f'Created {len(bed_types)} bed types'))
        
        # Get created objects
        wards_dict = {ward.name: ward for ward in Ward.objects.all()}
        bed_types_dict = {bed_type.name: bed_type for bed_type in BedType.objects.all()}
        
        # Create beds
        beds = []
        
        # General Ward - 20 beds
        for i in range(1, 21):
            beds.append(Bed(
                bed_number=f'GW-{i:03d}',
                ward=wards_dict['General Ward'],
                bed_type=bed_types_dict['Standard'],
                is_occupied=i % 3 == 0  # Every 3rd bed is occupied
            ))
        
        # Private Ward - 10 beds
        for i in range(1, 11):
            beds.append(Bed(
                bed_number=f'PW-{i:03d}',
                ward=wards_dict['Private Ward'],
                bed_type=bed_types_dict['Deluxe'],
                is_occupied=i % 2 == 0  # Every 2nd bed is occupied
            ))
        
        # ICU - 8 beds
        for i in range(1, 9):
            beds.append(Bed(
                bed_number=f'ICU-{i:03d}',
                ward=wards_dict['ICU'],
                bed_type=bed_types_dict['ICU Bed'],
                is_occupied=i % 4 != 0  # 3 out of 4 beds are occupied
            ))
        
        # Pediatric Ward - 15 beds
        for i in range(1, 16):
            beds.append(Bed(
                bed_number=f'PED-{i:03d}',
                ward=wards_dict['Pediatric Ward'],
                bed_type=bed_types_dict['Pediatric Bed'],
                is_occupied=i % 5 == 0  # Every 5th bed is occupied
            ))
        
        # Maternity Ward - 12 beds
        for i in range(1, 13):
            beds.append(Bed(
                bed_number=f'MAT-{i:03d}',
                ward=wards_dict['Maternity Ward'],
                bed_type=bed_types_dict['Birthing Bed'],
                is_occupied=i % 3 == 0  # Every 3rd bed is occupied
            ))
        
        # Emergency Ward - 10 beds
        for i in range(1, 11):
            beds.append(Bed(
                bed_number=f'ER-{i:03d}',
                ward=wards_dict['Emergency Ward'],
                bed_type=bed_types_dict['Emergency Bed'],
                is_occupied=i % 2 == 1  # Every odd-numbered bed is occupied
            ))
        
        Bed.objects.bulk_create(beds)
        self.stdout.write(self.style.SUCCESS(f'Created {len(beds)} beds'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed successfully'))
"""Comando de gestión de Django para limpiar migraciones problemáticas de horses"""
from django.core.management.base import BaseCommand
from django.db import connection
import sys

class Command(BaseCommand):
    help = 'Limpia las migraciones problemáticas de la aplicación horses que no existe'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la eliminación sin confirmación',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('🔄 Iniciando limpieza de migraciones problemáticas...')
        )
        
        # Verificar si hay migraciones de horses
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT COUNT(*) FROM django_migrations 
                    WHERE app = 'horses';
                """)
                horses_migrations = cursor.fetchone()[0]
                
                if horses_migrations == 0:
                    self.stdout.write(
                        self.style.SUCCESS('✅ No hay migraciones de horses para limpiar')
                    )
                    return
                
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Encontradas {horses_migrations} migraciones de horses')
                )
                
                # Pedir confirmación si no se usa --force
                if not options['force']:
                    confirm = input('¿Deseas continuar con la limpieza? (s/N): ')
                    if confirm.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                        self.stdout.write(
                            self.style.ERROR('❌ Operación cancelada')
                        )
                        return
                
                # Eliminar migraciones de horses
                cursor.execute("""
                    DELETE FROM django_migrations 
                    WHERE app = 'horses';
                """)
                
                deleted_count = cursor.rowcount
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Eliminadas {deleted_count} migraciones de horses')
                )
                
                # Intentar eliminar tablas relacionadas
                tables_to_check = [
                    'horses_horse',
                    'horses_horse_genealogy',
                    'horses_horse_technologies'
                ]
                
                for table in tables_to_check:
                    try:
                        cursor.execute(f"""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE table_name = '{table}'
                            );
                        """)
                        
                        if cursor.fetchone()[0]:
                            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                            self.stdout.write(
                                self.style.SUCCESS(f'✅ Tabla {table} eliminada')
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'⚠️  No se pudo verificar/eliminar {table}: {e}')
                        )
                
                # Limpiar constraints problemáticas
                try:
                    cursor.execute("""
                        DROP INDEX IF EXISTS horses_horse_internal_id_c019ac91_uniq;
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Constraint problemática eliminada')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'ℹ️  Constraint ya limpia: {e}')
                    )
                
                self.stdout.write(
                    self.style.SUCCESS('🎉 Limpieza completada exitosamente')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error durante la limpieza: {e}')
                )
                sys.exit(1)
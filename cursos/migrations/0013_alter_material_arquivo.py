# Modificado manualmente: removida dependência do cloudinary_storage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0012_material_tipo_alter_aula_ordem_alter_modulo_ordem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='materiais/'),
        ),
    ]
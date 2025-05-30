# Generated by Django 4.2.20 on 2025-05-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('url', models.URLField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
                ('technologies', models.TextField(help_text='Comma-separated list of technologies')),
                ('featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RenameModel(
            old_name='ContactMessage',
            new_name='Contact',
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='service',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='service',
            name='icon',
            field=models.CharField(help_text='Nombre del ícono de Font Awesome', max_length=50),
        ),
    ]

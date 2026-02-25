# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil utilisateur',
                'verbose_name_plural': 'Profils utilisateurs',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('shipping', 'Livraison'), ('billing', 'Facturation')], max_length=10, verbose_name="Type d'adresse")),
                ('full_name', models.CharField(max_length=200, verbose_name='Nom complet')),
                ('phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('address_line1', models.CharField(max_length=250, verbose_name='Adresse ligne 1')),
                ('address_line2', models.CharField(blank=True, max_length=250, verbose_name='Adresse ligne 2')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Code postal')),
                ('country', models.CharField(default='France', max_length=100, verbose_name='Pays')),
                ('is_default', models.BooleanField(default=False, verbose_name='Adresse par défaut')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Adresse',
                'verbose_name_plural': 'Adresses',
                'ordering': ['-is_default', '-created_at'],
            },
        ),
    ]

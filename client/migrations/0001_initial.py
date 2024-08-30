# Generated by Django 5.0.2 on 2024-07-12 15:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=250)),
                ('detail', models.TextField()),
                ('event_logo', models.ImageField(upload_to='event_images/')),
                ('start_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['start_at'],
            },
        ),
        migrations.CreateModel(
            name='NormalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('type_of_account', models.CharField(choices=[('student', 'Student'), ('worker', 'Worker'), ('in_college', 'In College'), ('club', 'Club')], default='student', max_length=100)),
                ('age', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_form', models.URLField()),
                ('number_of_participant', models.IntegerField(null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='No Title', max_length=200)),
                ('content', models.TextField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preuve', models.FileField(upload_to='upload/')),
                ('club_wilaya', models.CharField(choices=[('01', 'Adrar'), ('02', 'Chlef'), ('03', 'Laghouat'), ('04', 'Oum El Bouaghi'), ('05', 'Batna'), ('06', 'Béjaia'), ('07', 'Biskra'), ('08', 'Béchar'), ('09', 'Blida'), ('10', 'Bouira'), ('11', 'Tamanrasset'), ('12', 'Tébessa'), ('13', 'Tlemcen'), ('14', 'Tiaret'), ('15', 'Tizi-Ouzou'), ('16', 'Alger'), ('17', 'Djelfa'), ('18', 'Jijel'), ('19', 'Sétif'), ('20', 'Saïda'), ('21', 'Skikda'), ('22', 'Sidi Bel Abbès'), ('23', 'Annaba'), ('24', 'Guelma'), ('25', 'Constantine'), ('26', 'Médéa'), ('27', 'Mostaganem'), ('28', "M'Sila"), ('29', 'Mascara'), ('30', 'Djelfa'), ('31', 'Oran'), ('32', 'El Bayadh'), ('33', 'Illizi'), ('34', 'Bordj Bou Arreridj'), ('35', 'Boumerdes'), ('36', 'El Tarf'), ('37', 'Tindouf'), ('38', 'Tissemsilt'), ('39', 'El Oued'), ('40', 'Khenchla'), ('41', 'Souk Ahras'), ('42', 'Tipaza'), ('43', 'Tipasa'), ('44', 'Ain Defla'), ('45', 'Naâma'), ('46', 'Ain Témouchent'), ('47', 'Ghardaia'), ('48', 'Relizane'), ('49', 'Timimoun'), ('50', 'Bordj Badji Mokhtar'), ('51', 'Ouled Djellal'), ('52', 'Béni Abbès'), ('53', 'In Salah'), ('54', 'In Guezzam'), ('55', 'Touggourt'), ('56', 'Djanet'), ('57', "El M'Ghair"), ('58', 'El Meniaa')], max_length=100, null=True)),
                ('club_name', models.CharField(default='', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='club_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='client.organizer'),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('image', models.ImageField(upload_to='profile_image/')),
                ('register_in', models.DateTimeField(default=django.utils.timezone.now)),
                ('abonne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonne_normal', to=settings.AUTH_USER_MODEL)),
                ('abonnement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnement_normal', to=settings.AUTH_USER_MODEL)),
                ('event_accepted_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=200)),
                ('sponsor_image', models.ImageField(upload_to='sponsor/')),
                ('sponsor_image2', models.ImageField(upload_to='sponsor2/')),
                ('sponsor_image3', models.ImageField(upload_to='sponsor3/')),
                ('sponsor_location', models.TextField()),
                ('sponsor_detail', models.TextField()),
                ('related_event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
            ],
        ),
        migrations.CreateModel(
            name='Profile2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('logo', models.ImageField(upload_to='logo/')),
                ('register_in', models.DateTimeField(default=django.utils.timezone.now)),
                ('abonne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonne', to=settings.AUTH_USER_MODEL)),
                ('abonnement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnement', to=settings.AUTH_USER_MODEL)),
                ('all_organised_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client.organizer')),
                ('golden_sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.sponsor')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.event')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.team')),
            ],
        ),
    ]

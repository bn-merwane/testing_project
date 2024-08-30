from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class NormalUser(AbstractUser):
    TYPE_CHOICES = [
        ('student', 'Student'),
        ('club', 'Club'),
    ]
    type_of_account = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=False, null=False,default='student')

    age = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def is_club(self):
        return self.type_of_account == 'club'
    def __str__(self):
        return self.username

class Organizer(models.Model):

    WILAYA_CHOICES = [
        ('01', 'Adrar'), ('02', 'Chlef'), ('03', 'Laghouat'), ('04', 'Oum El Bouaghi'), ('05', 'Batna'), ('06', 'Béjaia'),
        ('07', 'Biskra'), ('08', 'Béchar'), ('09', 'Blida'), ('10', 'Bouira'), ('11', 'Tamanrasset'), ('12', 'Tébessa'),
        ('13', 'Tlemcen'), ('14', 'Tiaret'), ('15', 'Tizi-Ouzou'), ('16', 'Alger'), ('17', 'Djelfa'), ('18', 'Jijel'),
        ('19', 'Sétif'), ('20', 'Saïda'), ('21', 'Skikda'), ('22', 'Sidi Bel Abbès'), ('23', 'Annaba'), ('24', 'Guelma'),
        ('25', 'Constantine'), ('26', 'Médéa'), ('27', 'Mostaganem'), ('28', 'M\'Sila'), ('29', 'Mascara'),
        ('30', 'Djelfa'), ('31', 'Oran'), ('32', 'El Bayadh'), ('33', 'Illizi'), ('34', 'Bordj Bou Arreridj'),
        ('35', 'Boumerdes'), ('36', 'El Tarf'), ('37', 'Tindouf'), ('38', 'Tissemsilt'), ('39', 'El Oued'),
        ('40', 'Khenchla'), ('41', 'Souk Ahras'), ('42', 'Tipaza'), ('43', 'Tipasa'), ('44', 'Ain Defla'),
        ('45', 'Naâma'), ('46', 'Ain Témouchent'), ('47', 'Ghardaia'), ('48', 'Relizane'), ('49', 'Timimoun'),
        ('50', 'Bordj Badji Mokhtar'), ('51', 'Ouled Djellal'), ('52', 'Béni Abbès'), ('53', 'In Salah'),
        ('54', 'In Guezzam'), ('55', 'Touggourt'), ('56', 'Djanet'), ('57', 'El M\'Ghair'), ('58', 'El Meniaa'),
    ]
    
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    preuve = models.FileField(upload_to='upload/', blank=False, null=False)
    club_wilaya = models.CharField(max_length=100, choices=WILAYA_CHOICES, blank=False, null=True)
    rank1=models.IntegerField(default=0)
    rank2=models.IntegerField(default=0)
    rank3=models.IntegerField(default=0)
    rank4=models.IntegerField(default=0)
    rank5=models.IntegerField(default=0)
    is_active=models.BooleanField(default=False)

    def ranking(self):
        # Calculate the average of rank1 to rank5
        total_rank = self.rank1 + self.rank2 + self.rank3 + self.rank4 + self.rank5
        if total_rank > 0:
            return total_rank / 5
        else:
            return 0.0  # or any default value you prefer

    def __str__(self):
        return f"{self.user.username}'s Organizer Profile"

class ActiveEventManager(models.Manager):
    def active(self):
        now = timezone.now()
        return self.filter(start_at__lte=now, end_at__gte=now)

class Event(models.Model):
    WILAYA_CHOICES = [
        ('01', 'Adrar'), ('02', 'Chlef'), ('03', 'Laghouat'), ('04', 'Oum El Bouaghi'), ('05', 'Batna'), ('06', 'Béjaia'),
        ('07', 'Biskra'), ('08', 'Béchar'), ('09', 'Blida'), ('10', 'Bouira'), ('11', 'Tamanrasset'), ('12', 'Tébessa'),
        ('13', 'Tlemcen'), ('14', 'Tiaret'), ('15', 'Tizi-Ouzou'), ('16', 'Alger'), ('17', 'Djelfa'), ('18', 'Jijel'),
        ('19', 'Sétif'), ('20', 'Saïda'), ('21', 'Skikda'), ('22', 'Sidi Bel Abbès'), ('23', 'Annaba'), ('24', 'Guelma'),
        ('25', 'Constantine'), ('26', 'Médéa'), ('27', 'Mostaganem'), ('28', 'M\'Sila'), ('29', 'Mascara'),
        ('30', 'Djelfa'), ('31', 'Oran'), ('32', 'El Bayadh'), ('33', 'Illizi'), ('34', 'Bordj Bou Arreridj'),
        ('35', 'Boumerdes'), ('36', 'El Tarf'), ('37', 'Tindouf'), ('38', 'Tissemsilt'), ('39', 'El Oued'),
        ('40', 'Khenchla'), ('41', 'Souk Ahras'), ('42', 'Tipaza'), ('43', 'Tipasa'), ('44', 'Ain Defla'),
        ('45', 'Naâma'), ('46', 'Ain Témouchent'), ('47', 'Ghardaia'), ('48', 'Relizane'), ('49', 'Timimoun'),
        ('50', 'Bordj Badji Mokhtar'), ('51', 'Ouled Djellal'), ('52', 'Béni Abbès'), ('53', 'In Salah'),
        ('54', 'In Guezzam'), ('55', 'Touggourt'), ('56', 'Djanet'), ('57', 'El M\'Ghair'), ('58', 'El Meniaa'),
    ]
    type_choice=[
        ('presentielle','presentielle'),
        ('en_ligne','en_ligne')
    ]
    EVENT_CATEGORIES = [
        ('academic', 'Academic Events'),
        ('competitions', 'Competitions'),
        ('social', 'Social Events'),
        ('cultural', 'Cultural Events'),
        ('sports', 'Sports Events'),
        ('career', 'Career Development'),
        ('club_specific', 'Club-Specific Events'),
        ('community_service', 'Volunteer & Community Service'),
        ('technology_innovation', 'Technology & Innovation'),
        ('educational_workshops', 'Educational Workshops'),
    ]
    categorie = models.CharField(blank=False, null=False, default='social', choices=EVENT_CATEGORIES, max_length=600)
    club_creator = models.ForeignKey('Organizer', on_delete=models.CASCADE, related_name='events' , blank=False,null=False)
    event_title = models.CharField(max_length=250,blank=False,null=False)
    detail = models.TextField()
    wilaya = models.CharField(max_length=100, choices=WILAYA_CHOICES, blank=False, null=False,default='tlemcen')
    event_logo = models.ImageField(upload_to='event_images/')
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(default=timezone.now)
    registration_end = models.BooleanField(default=False)
    typeP= models.CharField(max_length=100,default='presentielle',blank=False,null=False,choices=type_choice)

    objects = ActiveEventManager()

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.event_title

    def is_past_event(self):
        return self.end_at < timezone.now()

    def is_upcoming_event(self):
        return self.start_at > timezone.now()

    def is_ongoing_event(self):
        return self.start_at <= timezone.now() <= self.end_at

class Notification(models.Model):
    receiver = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, default='No Title', null=False)
    content = models.TextField()
    dateandtime=models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['dateandtime']
    def __str__(self) -> str:
        return self.title
class Profile(models.Model):
    bio = models.TextField()
    image = models.ImageField(upload_to='profile_image/')
    event_accepted_in = models.ForeignKey(Event, on_delete=models.CASCADE)
    abonne = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='abonne_normal')
    abonnement = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='abonnement_normal')
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    register_in = models.DateTimeField(default=timezone.now)

    def register_since(self):
        time_difference = timezone.now() - self.register_in
        return time_difference.days  # Example: Return days since registration

    def __str__(self):
        return self.user.username  # Provide a meaningful string representation

class Sponsor(models.Model):
    related_event = models.OneToOneField(Event, on_delete=models.CASCADE,limit_choices_to={'end_at__lt': timezone.now()})
    sponsor_name = models.CharField(max_length=200)
    sponsor_image = models.ImageField(upload_to='sponsor/')
    sponsor_image2 = models.ImageField(upload_to='sponsor2/')
    sponsor_image3 = models.ImageField(upload_to='sponsor3/')
    sponsor_location = models.TextField()
    sponsor_detail = models.TextField()

class Participant(models.Model):
    participant = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,limit_choices_to={'end_at__lt': timezone.now()})

class Team(models.Model):
    team_member = models.ForeignKey(NormalUser, on_delete=models.CASCADE)

class Demand(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,limit_choices_to={'end_at__lt': timezone.now(),'registration_end':False})
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    demande_dateandtime=models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['demande_dateandtime']

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,limit_choices_to={'end_at__lt': timezone.now(),'registration_end':False})
    url_form = models.URLField()
    number_of_participant = models.IntegerField(blank=False, null=True)

class Profile2(models.Model):
    bio = models.TextField()
    logo = models.ImageField(upload_to='logo/')
    abonne = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='abonne')    
    abonnement = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='abonnement')  
    all_organised_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    golden_sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    club = models.OneToOneField(Organizer, on_delete=models.CASCADE)
    register_in = models.DateTimeField(default=timezone.now)

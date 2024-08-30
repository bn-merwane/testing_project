from django.forms import ValidationError
from client.models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
def age_validator(value):
    if value < 14 or value > 100:
        raise ValidationError('Age must be between 14 and 100.')

class UserSignupSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(validators=[age_validator])
    email=serializers.EmailField(validators=[UniqueValidator(queryset=NormalUser.objects.all())])
    
    class Meta:
        model = NormalUser
        fields = ['username', 'email', 'password', 'age', 'type_of_account']
    
    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
class ClubSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organizer
        fields=['club_wilaya','preuve']




class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid username or password.")

        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data

    
class UserSerializer(serializers.ModelSerializer):
    notifications=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model=NormalUser
        fields=['username','type_of_account','notifications']



class ClubSerializer(serializers.ModelSerializer):
    #events=serializers.HyperlinkedRelatedField(many=True,read_only=True)
    events=serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model=Organizer
        fields=['username','type_of_account','club_wilaya','events','ranking']


class EventSerializer(serializers.ModelSerializer):
    club_creator=serializers.StringRelatedField()
    
    class Meta:
        model=Event
        fields='__all__'

class EventGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['categorie','event_title','event_logo','start_at','end_at','registration_end']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        Model=Notification
        fields='__all__'

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude=['register_in']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sponsor
        fields='__all__'

class ParticipentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Participant
        fields='__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields='__all__'

class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Demand
        fields='__all__'
class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventRegistration
        fields='__all__'

class Profile2Serializer(serializers.ModelSerializer):
    class Meta:
        model=Profile2
        fields='__all__'

class ResetPassword(serializers.Serializer):
    email=serializers.EmailField()
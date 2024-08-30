from rest_framework.decorators import api_view, authentication_classes, permission_classes,throttle_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from client.pag import PostCursorPaginationNormal
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .perm import CreateEventPermission 
from client.serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status,filters
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.exceptions import NotFound,PermissionDenied
import random
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.signing import TimestampSigner,SignatureExpired
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
import django_filters
from django.db.models import  Q
from rest_framework.reverse import reverse


@api_view(['POST'])
@authentication_classes([])  # Disable authentication for this endpoint
@permission_classes([AllowAny])   
@throttle_classes([UserRateThrottle,AnonRateThrottle])  # Disable permission checks for this endpoint
def NormalLogin(request):
    if request.method == 'POST':
        user_data = request.data
        user_serialized_data = UserLoginSerializer(data=user_data)
        
        if user_serialized_data.is_valid():
            username = user_serialized_data.validated_data.get('username')
            password = user_serialized_data.validated_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'detail': 'Login succeeded', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Invalid data', 'errors': user_serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@authentication_classes([])  # Disable authentication
@permission_classes([AllowAny]) 
@throttle_classes([UserRateThrottle,AnonRateThrottle])
def signup(request):


    if request.method == 'POST':
        user_data = request.data
        user_serializer = UserSignupSerializer(data=user_data)
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            token=Token.objects.create(user=user)
            if user.type_of_account == 'club':
                club_data = {
                    'club_wilaya': request.data.get('club_wilaya'),
                    'preuve': request.FILES.get('preuve'),

                }
                club_serializer = ClubSignupSerializer(data=club_data)
                if club_serializer.is_valid():
                    Organizer.objects.create(user=user, **club_serializer.validated_data)

                    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
                return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"data":user_serializer.data,"token":token.key} , status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
#@authentication_classes([BasicAuthentication, TokenAuthentication])
#@permission_classes([IsAuthenticated])
#@throttle_classes([UserRateThrottle])
@cache_page(60 * 60)
def home(request):
    if request.method == 'GET':
        # Initialize paginators
        trending_paginator = PostCursorPaginationNormal()
        upcoming_paginator = PostCursorPaginationNormal()
        ongoing_paginator = PostCursorPaginationNormal()

        # Filter and paginate trending events
        trending_events = Event.objects.filter(club_creator__rank5__gte=4)
        paginated_trending_events = trending_paginator.paginate_queryset(trending_events, request)
        trending_events_serialized = EventSerializer(paginated_trending_events, many=True).data

        # Add URL to each trending event
        for event in trending_events_serialized:
            event['url_to'] = reverse('eventdetail', args=[event['id']], request=request)

        # Filter and paginate upcoming events
        upcoming_events = Event.objects.filter(start_at__gt=timezone.now()).order_by('start_at')
        paginated_upcoming_events = upcoming_paginator.paginate_queryset(upcoming_events, request)
        upcoming_events_serialized = EventSerializer(paginated_upcoming_events, many=True).data

        # Filter and paginate ongoing events
        ongoing_events = Event.objects.active()
        paginated_ongoing_events = ongoing_paginator.paginate_queryset(ongoing_events, request)
        ongoing_event_serialized = EventSerializer(paginated_ongoing_events, many=True).data

        # Prepare the response data with pagination links
        data = {
            'trending': {
                'results': trending_events_serialized,
                'next': trending_paginator.get_next_link(),
                'previous': trending_paginator.get_previous_link()
            },
            'upcoming': {
                'results': upcoming_events_serialized,
                'next': upcoming_paginator.get_next_link(),
                'previous': upcoming_paginator.get_previous_link()
            },
            'ongoing': {
                'results': ongoing_event_serialized,
                'next': ongoing_paginator.get_next_link(),
                'previous': ongoing_paginator.get_previous_link()
            }
        }

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CreateEvenet(generics.CreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,CreateEventPermission]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    def perform_create(self, serializer):
      serializer.save(club_creator=self.request.user.organizer)
           
 
class Filter_by_categorie(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    def get(self, request, *args, **kwargs):
        # Access URL parameter from kwargs
        category = self.kwargs.get('categorie')
        print(f"Category from URL: {category}")
        
        # Ensure the category is valid
        if not category:
            return Response({'error': 'Category parameter is required'}, status=400)
        
        # Filter events based on the category
        events = Event.objects.filter(categorie__iexact=category)
        print(f"Filtered events: {events}")
        
        # Check if events are empty
        if not events.exists():
            return Response({'error': 'No events found for the given category'}, status=404)
        
        # Serialize the filtered events
        events_serialized = EventGeneralSerializer(instance=events, many=True).data
        
        # Return the response with serialized data
        return Response({'data': events_serialized})
    
class CategoryFilter(django_filters.FilterSet):
    categorie = django_filters.CharFilter(field_name='categorie', lookup_expr='exact')
    wilaya = django_filters.CharFilter(field_name='wilaya',lookup_expr='exact')


    class Meta:
        model = Event
        fields = ['categorie','wilaya']

    def filter_queryset(self, queryset):
        categorie=self.data.get('categorie')
        wilaya=self.data.get('wilaya')
        if categorie and wilaya:
            queryset=Event.objects.filter( Q(wilaya=wilaya) | Q(categorie=categorie))
        elif categorie:
            queryset=Event.objects.filter(categorie=categorie)
        else:
            queryset=Event.objects.filter(wilaya=wilaya)

        return queryset

# Define the view that uses the filter class
class Filter_by_categorie2(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventGeneralSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # Ensure you are using the correct filter backend
    filterset_class = CategoryFilter  # Use 'filterset_class' instead of 'filter_backends' for the filter class


class EventDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    #authentication_classes=[TokenAuthentication]
    #permission_classes=[IsAuthenticated]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_object(self):
        event_id = self.kwargs.get('id')
        if not event_id:
            raise NotFound("Event ID must be provided as a query parameter.")
        
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise NotFound("Event not found.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Check if the user is the owner of the event
        is_owner = instance.club_creator == self.request.user.organizer

        additional_data = {
            'message': 'Event details retrieved successfully',
            'status': 'success',
            'event': serializer.data,
            'is_owner': is_owner
        }
        return Response(additional_data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.club_creator == self.request.user.organizer:
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to update this event.")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

  
class FilterWilaya(generics.ListAPIView):
    #authentication_classes=[TokenAuthentication]
    #permission_classes=[IsAuthenticated]
    #throttle_classes=[UserRateThrottle,AnonRateThrottle]
    model=Event
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['categorie']

    def get_queryset(self):
      wilaya = self.request.query_params.get('wilaya')
      print("Received Wilaya:", wilaya)
    
      if wilaya:
        try:
            queryset = Event.objects.filter(wilaya__icontains=wilaya)
            print("Filtered Queryset:", queryset)
            return queryset
        except Exception as e:
            print("Error during filtering:", e)
            raise e

class FilterType(generics.ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    serializer_class = EventSerializer

    def get_queryset(self):
        # Retrieve 'wilaya' parameter from query parameters
        wilaya = self.request.query_params.get('type')
        
        # Filter queryset based on the 'wilaya' parameter
        if wilaya:
            return Event.objects.filter(typeP=wilaya)
        return Event.objects.all()
    

    

class ResetPassword(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = [] 
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    def post(self, request):
     # Disable permission checks

        email = request.data.get('email')
        if email:
            try:
                get_user = NormalUser.objects.get(email=email)
                if get_user:
                    # Generate reset code
                    reset_code = random.randint(1000, 9999)
                    cache.set(f'reset_code_{email}', reset_code, timeout=3600)  # Cache for 1 hour

                    # Send email
                    send_mail(
                        'Evently Password Reset Code',
                        f'Your reset code is: {reset_code}',
                        '7arfa2024@gmail.com',
                        [email],
                        fail_silently=False,
                    )

                    # Generate reset URL
                    signer = TimestampSigner(salt="resetpassword")
                    data = f'{email}'
                    data_signed = signer.sign(data)
                    reset_url = f'http://127.0.0.1:8000/new_password/?data={data_signed}'

                    return Response({"reset_url": reset_url}, status=200)
                else:
                    return Response({"error": "User not found"}, status=404)
            except NormalUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        return Response({"error": "Email not provided"}, status=400)
class NewPassword(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = [] 
    throttle_classes=[UserRateThrottle,AnonRateThrottle]     # Disable permission checks

    def post(self, request):
        data = request.data
        signed_data = request.query_params.get('data')
        new_password = data.get('new_password')
        reset_code = data.get('reset_code')

        if not signed_data or not new_password or not reset_code:
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify signature
        signer = TimestampSigner(salt="resetpassword")
        try:
            email = signer.unsign(signed_data, max_age=60*10)  
        except SignatureExpired:
            return Response({"error": "Reset link expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify reset code
        cached_code = cache.get(f'reset_code_{email}')
        if not cached_code or int(reset_code) != cached_code:
            return Response({"error": "Invalid reset code"}, status=status.HTTP_400_BAD_REQUEST)

        # Update password
        try:
            user = NormalUser.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            cache.delete(f'reset_code_{email}')  # Invalidate the reset code after use
            return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)
        except NormalUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GedgetSer
from .models import User,Gadget
# from rest_framework_simplejwt.authentication import JWTAuthentication --> Globally defined in settings.py
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    print("\n Inside list View \n")
    def post(self, request):
        print("\n post req \n")
        try:
            print("\n checking \n")
            e= request.data.get('email')
            p=request.data.get('password')
            if not e or not p:
                return Response({
                    'msg':"Email and passwords are required",
                },status=401)
            logged_user = User.objects.get(email = e,password = p)
        except User.DoesNotExist:
            print("\n No user..something is wrong \n")
            return Response({
                "msg":"Invalid creds",
            },status= 401)
        print("\n Got user.. \n")
        refresh=RefreshToken.for_user(logged_user)
        access = str(refresh.access_token)
        print("\n access token"+ " : " + access +"\n")
        return Response({
            "name": logged_user.username,
            "token":access
        })

class GadgetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        userItems = Gadget.objects.filter(created_by = request.user).order_by("id")

        serializer = GedgetSer(userItems, many = True)

        return Response({
            "count": userItems.count(),
            "items":serializer.data
        },status=200)


class AdminListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not(user.role) or not(user.role.roleName.lower() == 'admin'):
            print("\n Non-admin trying to access admin list \n")
            return Response({
                'msg':"Access Denied"
            },status= 403)
        print("\n Admin authenticated. Fetching all gadgets... \n")
        AllList = Gadget.objects.all().order_by("id")
        ser = GedgetSer(AllList, many = True)
        return Response({
            'admin':user.username,
            'total_items':len(ser.data),
            'items':ser.data,
        },status=200)
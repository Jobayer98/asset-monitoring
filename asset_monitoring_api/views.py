from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import CompanySerializer, EmployeeSerializer, DeviceSerializer, DeviceLogSerializer
from .models import Company, Employee, Device, DeviceLog


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Manager").exists()

class CompanyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        requested_employee = get_object_or_404(Employee, id=user_id)
        company = Company.objects.get(id=requested_employee.company_id)
        serialized_item = self.serializer_class(company)
        return Response(serialized_item.data)
    
    def post(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You are not authorized"}, 403)
        

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user
        requested_employee = get_object_or_404(Employee, id=user.id)
        company = get_object_or_404(Company, id=pk)
        if requested_employee.company_id == company.id:
            serializer = self.serializer_class(company)
            return Response(serializer.data)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            pk = kwargs['pk']
            user_id = request.user.id
            requested_employee = get_object_or_404(Employee, id=user_id)
            company = get_object_or_404(Company, id=pk)
            if requested_employee.company_id == company.id:
                serializer = self.serializer_class(company, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            pk = kwargs['pk']
            user_id = request.user.id
            requested_employee = get_object_or_404(Employee, id=user_id)
            company = get_object_or_404(Company, id=pk)
            if requested_employee.company_id == company.id:
                serializer = self.serializer_class(company, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            pk = kwargs['pk']
            user_id = request.user.id
            requested_employee = get_object_or_404(Employee, id=user_id)
            company = get_object_or_404(Company, id=pk)
            if requested_employee.company_id == company.id:
                company.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
   
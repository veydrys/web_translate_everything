from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import TKMK
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_features(request):
    features = [
        {"title": "TEXT TRANSLATION", "description": "Translate text between languages with high accuracy."},
        {"title": "IMAGE TRANSLATION", "description": "Automatically extract and translate text from images."},
        {"title": "DOCUMENT TRANSLATION", "description": "Translate entire documents including PDFs and DOCX files."},
    ]
    return JsonResponse(features, safe=False)
@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tk = data.get("tk")
            mk = data.get("mk")

            if TKMK.objects.filter(tk=tk).exists():
                return JsonResponse({"error": "The account already exists!"}, status=400)

            user = TKMK(tk=tk, mk=mk)
            user.save()

            return JsonResponse({"message": "Register successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        return render(request, "register.html")

    return JsonResponse({"error": "Not support this method"}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tk = data.get("tk")
            mk = data.get("mk")

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tkmk WHERE tk = %s AND mk = %s", [tk, mk])
                user = cursor.fetchone()

            if user:
                return JsonResponse({"message": "Login successfully", "token": "fake-token"}, status=200)
            else:
                return JsonResponse({"error": "Wrong password or username"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Error"}, status=405)

def logout_user(request):
    request.session.flush()
    return redirect('index')
def home(request):
    return render(request, 'home.html')
def index(request):
    return render(request, 'index.html')
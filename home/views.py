from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

@csrf_exempt
def home(request):
    if request.method=="POST":
        data=request.POST
        text = data.get('text')
        print(text)
        language = data.get('language') 
        print(language)
        
        base_text="I will give an algorithm. Give a fully functional code based on it, without any errors. "
        url = "https://api.textcortex.com/v1/codes"
        api_key=os.environ.get('API_KEY')
        payload = {
            "max_tokens": 4000,
            "mode": language,
            "model": "icortex-1",
            "n": 1,
            "temperature": 0,
            "text": f"{base_text} {text}"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        response_data = json.loads(response.text)
        try:
            output_text = response_data["data"]["outputs"][0]["text"]
            remaining_credits=response_data["data"]["remaining_credits"]
            
            return JsonResponse({"code":output_text, "remaining_credits":remaining_credits})
        except Exception as e:
            return JsonResponse({"code":"Some error occured, try a different question", "remaining_credits":"NaN"})
    return JsonResponse({"message":"Server booted"})
    
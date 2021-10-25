from django.shortcuts import render

# Create your views here.
from testapp.forms import TestForm

import requests
import base64
import io

def TestView(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            eng_text = papago(text)
            result = dall_e(eng_text)
            return render(request, 'testapp/result.html', {'text': text, 'eng_text': eng_text, 'result': result})
    else:
        form = TestForm()
        return render(request, 'testapp/test.html', {'form': form})


def papago(text):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'X-Naver-Client-Id': ,
        'X-Naver-Client-Secret':
    }
    data = {
        'source': 'ko',
        'target': 'en',
        'text': text
    }
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result['message']['result']['translatedText']


def dall_e(eng_text):
    url = 'https://main-dalle-server-scy6500.endpoint.ainize.ai/generate'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = '{"text": "%s", "num_images": 5}' % eng_text
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result
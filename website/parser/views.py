from django.shortcuts import render
from django.http import HttpRequest

from services.parsers import *


def parse_sources(search_text: str):
    return {
        'multicom': parse_multicom(search_text),
        'tehnomax': parse_tehnomax(search_text),
        'datika': parse_datika(search_text),
    }


# Create your views here.
def index(request: HttpRequest):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        sources = parse_sources(search_text)
        context = {
            'parsed_sources': sources,
            'remainder': [str(i) for i in range(len(sources) % 4)],
        }
        return render(request, 'parser/index.html', context=context)
    elif request.method == 'GET':
        return render(request, 'parser/index.html')

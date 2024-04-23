from django.shortcuts import render
from django.http import HttpRequest

from services.parsers import *


def parse_sources(search_text: str, category: str = None):
    united_result = parse_multicom(search_text, category) + parse_tehnomax(search_text, category) + parse_datika(
        search_text, category)

    return united_result


# Create your views here.
# def index(request: HttpRequest):
#     if request.method == 'POST':
#         search_text = request.POST.get('search_text')
#         sources = parse_sources(search_text)
#         context = {
#             'parsed_sources': sources,
#             'remainder': [str(i) for i in range(len(sources) % 4)],
#         }
#         return render(request, 'parser/old_index.html', context=context)
#     elif request.method == 'GET':
#         return render(request, 'parser/old_index.html')


def index(request: HttpRequest):
    return render(request, 'parser/index.html')


def products(request: HttpRequest):
    return render(request, 'parser/products.html')


def search_view(request: HttpRequest):
    search_text = request.GET.get('q', '')
    search_result = []
    if search_text:
        search_result = parse_sources(search_text)

    search_result.sort(key=lambda x: x['price'])

    context = {
        'search_result': search_result,
    }
    return render(request, 'parser/products.html', context)

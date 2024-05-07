from django.shortcuts import render
from django.http import HttpRequest
from django.http import Http404

from services.parsers import *
from services.categories import CATEGORIES


def parse_sources(search_text: str, category: str = None):
    united_result = parse_multicom(search_text, category) + parse_tehnomax(search_text, category) + parse_datika(
        search_text, category)

    for item in united_result:
        if item['picture']:
            continue
        item['picture'] = '/static/parser/images/not_found.png'

    return united_result

def index(request: HttpRequest):
    return render(request, 'parser/test-index.html')


def search_view(request: HttpRequest):
    search_text = request.GET.get('q', '')
    search_result = []
    if search_text:
        search_result = parse_sources(search_text)
    else:
        return render(request, 'parser/test-index.html')

    search_result.sort(key=lambda x: x['price'])

    context = {
        'search_result': search_result,
        'search_query': request.GET.get('q', '')
    }
    return render(request, 'parser/test-products.html', context)


def search_by_category(request: HttpRequest, category_name: str):
    if category_name not in CATEGORIES.keys():
        raise Http404

    search_text = request.GET.get('q', '')
    if not search_text:
        return render(request, 'parser/test-products.html')

    search_result = []
    if search_text:
        search_result = parse_sources(search_text, category_name)

    search_result.sort(key=lambda x: x['price'])

    context = {
        'search_result': search_result,
        'search_query': request.GET.get('q', '')
    }

    return render(request, 'parser/test-products.html', context)

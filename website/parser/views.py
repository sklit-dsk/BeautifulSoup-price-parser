from django.shortcuts import render
from django.http import HttpRequest
from django.http import Http404

from services.parsers import *
from services.categories import CATEGORIES
from parser.forms import SearchForm


def parse_sources(search_text: str, category: str = None):
    united_result = parse_multicom(search_text, category) + parse_tehnomax(search_text, category) + parse_datika(
        search_text, category)

    for item in united_result:
        if item['picture']:
            continue
        item['picture'] = '/static/parser/images/not_found.png'

    return united_result


def index(request: HttpRequest):
    return render(request, 'parser/index.html', {'form': SearchForm()})


def about_view(request: HttpRequest):
    return render(request, 'parser/about.html')


def search_view(request: HttpRequest):
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data['q']
        category = form.cleaned_data['category']
    else:
        raise Http404

    context = {
        'search_result': '',
        'search_query': query,
    }

    if category == 'none':
        search_result = parse_sources(query)
        search_result.sort(key=lambda x: x['price'])
        search_result = search_result[:50]

        context['search_result'] = search_result
        context['form'] = SearchForm()
        return render(request, 'parser/products.html', context)

    elif category in CATEGORIES.keys():

        search_result = parse_sources(query, category)
        if search_result:
            search_result.sort(key=lambda x: x['price'])

        context['search_result'] = search_result
        context['form'] = SearchForm(initial={'category': category})
        return render(request, 'parser/products.html', context)

    else:
        raise Http404

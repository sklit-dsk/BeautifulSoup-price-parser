from django.http import HttpRequest


def category_flag(request: HttpRequest):
    category = None

    try:
        category = request.path.split('/')[-2]
    except:
        pass

    return {
        'category': category
    }
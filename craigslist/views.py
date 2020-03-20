import requests
from bs4 import BeautifulSoup as bs4
from django.shortcuts import render
from requests.compat import quote_plus
from craigslist.models import Search

ROOT_URL = 'https://cosprings.craigslist.org'
BASE_SEARCH_URL = 'https://cosprings.craigslist.org/search/?query={}&sort=rel'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    url = 'https://cosprings.craigslist.org/'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4(res.text, "html.parser")

    linkList = []
    links = soup.select('#center a')
    for link in links:
        link_href = ROOT_URL + link.get('href')
        names = link.find('span').text
        linkList.append((link_href, names))

    firstHalf = linkList[:38]
    secondHalf = linkList[94:]
    newlinkList = firstHalf + secondHalf

    context = {
        'links': newlinkList,
    }

    return render(request, 'base.html', context)


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_SEARCH_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = bs4(data, "html.parser")

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    for i in post_listings:
        post_title = i.find(class_='result-title').text
        post_url = i.find('a').get('href')

        if i.find(class_='result-price'):
            post_price = i.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if i.find(class_='result-image').get('data-ids'):
            post_image_id = i.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    context = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'craigslist/new_search.html', context)

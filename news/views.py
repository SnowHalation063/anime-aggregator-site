import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()
#agg_prime
def scrape(request):
  session = requests.Session()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.animenewsnetwork.com/"
  content = session.get(url, verify=False).content
  soup = BSoup(content, "html.parser")
  News = soup.find_all('div', {"class":"herald box news"})
  for article in News:
    main = article.find_all('h3')[0]
    link = url + main.find('a')['href']
    image_src = url + article.find_all('div', {"class":"thumbnail"})[0]['data-src']
    title = main.get_text()
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.image = image_src
    new_headline.save()
  return redirect("../")


#agg_prime
def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)
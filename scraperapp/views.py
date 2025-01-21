from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        url = request.POST.get("url")
        
        if not url:
            return HttpResponse("Please provide a valid URL", status=400)

        try:
            # Send GET request to the URL
            response = requests.get(url)
            if response.status_code != 200:
                return HttpResponse(f"Failed to retrieve content from {url}", status=response.status_code)
            
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title and paragraphs as example content
            page_title = soup.title.string if soup.title else "No title found"
            paragraphs = soup.find_all('p')

            # Get text of each paragraph
            paragraph_texts = [para.get_text() for para in paragraphs]

            return render(request, 'scraperapp/output.html', {
                'url': url,
                'title': page_title,
                'paragraphs': paragraph_texts
            })
        
        except requests.RequestException as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    return render(request, 'scraperapp/index.html')

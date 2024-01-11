from django.shortcuts import render, redirect
from .scraper_logic import run_scraper


def results_view(request):
    if request.method == 'POST':
        urls = request.POST.get('urls').splitlines()
        keywords = request.POST.get('keywords').splitlines()
        case_sensitive = 'case_sensitive' in request.POST
        prefix_suffix = 'prefix_suffix' in request.POST
        deep_search = 'deep_search' in request.POST
        depth = int(request.POST.get('depth'))  # Get the selected depth

        all_results = []
        for url in urls:
            results = run_scraper(
                url, keywords, case_sensitive, prefix_suffix, deep_search, depth)
            all_results.extend(results)

        return render(request, 'scraper/results.html', {'all_results': all_results})

    else:
        return redirect('search')


def search_view(request):
    # Your code for rendering the search form
    return render(request, 'scraper/search_form.html')

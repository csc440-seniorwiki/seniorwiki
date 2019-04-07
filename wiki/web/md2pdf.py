from flask import render_template
from flask import request
from wiki.web import current_wiki
from flask_weasyprint import HTML
from flask_weasyprint import render_pdf


def md2pdf_single_page(url, pdf_template):
    pages = [current_wiki.get_or_404(url)]
    html = render_template(pdf_template, pages=pages)
    return render_pdf(HTML(string=html))


def md2pdf_multiple_page(pdf_template, select_template):
    links = current_wiki.index()
    if request.method == "POST":
        data = request.form.getlist('page')
        pages = []
        for url in data:
            pages.append(current_wiki.get_or_404(url))
        html = render_template(pdf_template, pages=pages)
        return render_pdf(HTML(string=html))
    return render_template(select_template, pages=links)


def md2pdf_full_wiki(pdf_template):
    pages = current_wiki.index()
    html = render_template(pdf_template, pages=pages)
    return render_pdf(HTML(string=html))

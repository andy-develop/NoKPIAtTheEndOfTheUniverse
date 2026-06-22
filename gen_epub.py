import os
import re
from ebooklib import epub
import markdown2

chapters_dir = r"C:\Users\Administrator\novels\NoKPIAtTheEndOfTheUniverse\chapters"
output_epub = r"C:\Users\Administrator\novels\NoKPIAtTheEndOfTheUniverse\NoKPIAtTheEndOfTheUniverse.epub"

book = epub.EpubBook()
book.set_identifier("nokpi-endofuniverse-apexshaw-2026")
book.set_title("No KPI at the End of the Universe")
book.set_language("en")
book.add_author("Apex Shaw")
book.add_metadata("DC", "description", "A liminal space romance about two broken people who find forever in a train station that doesn't exist.")
book.add_metadata("DC", "subject", "Liminal Space Romance")
book.add_metadata("DC", "subject", "Cozy Existentialism")

style = '''body{font-family:Georgia,serif;line-height:1.6;margin:1em}h1{font-size:1.8em;margin-top:2em;color:#4a2d6e;text-align:center;page-break-before:always}p{margin:0.8em 0;text-indent:1.5em}p:first-of-type{text-indent:0}hr{border:none;border-top:2px solid #c9a0dc;margin:2em auto;width:60%}em{font-style:italic}.center{text-align:center}'''
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
book.add_item(nav_css)

title_html = '<html><body><div style="text-align:center;margin-top:40%"><h1 style="font-size:2.5em;color:#4a2d6e;page-break-before:avoid">No KPI at the End of the Universe</h1><br/><h3 style="color:#8b5fbf">A Liminal Space Romance</h3><br/><p style="font-size:1.2em;text-indent:0">by Apex Shaw</p></div></body></html>'
title_page = epub.EpubHtml(title="Title", file_name="title.xhtml", lang="en")
title_page.content = title_html
title_page.add_item(nav_css)
book.add_item(title_page)

epub_chapters = [title_page]
toc = []

for i in range(1, 41):
    ch_file = os.path.join(chapters_dir, f"ch{i:03d}.md")
    with open(ch_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks", "strike"])
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content)
    ch_title = re.sub(r'<[^>]+>', '', title_match.group(1)) if title_match else f"Chapter {i}"
    full_html = f'<html><body>{html_content}</body></html>'
    chapter = epub.EpubHtml(title=ch_title, file_name=f"ch{i:03d}.xhtml", lang="en")
    chapter.content = full_html
    chapter.add_item(nav_css)
    book.add_item(chapter)
    epub_chapters.append(chapter)
    toc.append(chapter)

book.toc = toc
book.spine = epub_chapters
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
epub.write_epub(output_epub, book, {})
print(f"ePub written: {os.path.getsize(output_epub)} bytes")

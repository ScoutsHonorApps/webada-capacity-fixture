from pathlib import Path
import re,sys
n=int(sys.argv[1]);assert n in (5000,7500)
p=Path(__file__).parent
for i in range(n):
 name='index.html' if i==0 else f'page-{i:04}.html'
 source=(p/name).read_text() if (p/name).exists() else (p/('index.html' if i%4==0 else f'page-000{i%4}.html')).read_text()
 source=re.sub(r'Capacity fixture \d+',f'Capacity fixture {i}',source);source=re.sub(r'Fixture page \d+',f'Fixture page {i}',source)
 links=[]
 for child in range(4*i+1,min(4*i+5,n)):
  links.append(f'<a href="/webada-capacity-fixture/page-{child:04}.html">Fixture page {child}</a>')
 links.append('<a href="/webada-capacity-fixture/">Fixture start</a>')
 source=re.sub(r'<a href=.*?</a>(?:<a href=.*?</a>)*',''.join(links),source)
 (p/name).write_text(source)
seen=set();todo=['index.html']
while todo:
 name=todo.pop()
 if name in seen:continue
 seen.add(name)
 for url in re.findall(r'href="([^"]+)"',(p/name).read_text()):
  assert url.startswith('/webada-capacity-fixture/') and '?' not in url and '#' not in url
  target=url.removeprefix('/webada-capacity-fixture/') or 'index.html';assert (p/target).is_file();todo.append(target)
assert len(seen)==n
print(f'Graph verified: {n} unique pages, bounded four-child tree, root backlinks, no external/query paths')

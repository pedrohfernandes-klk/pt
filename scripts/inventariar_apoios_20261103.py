"""03/11/2026: inventário dos acessos docentes reais; não reescreve HTML."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'tests/fixtures/apoios-paginas-20261103.json'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.current=None;self.links=[];self.menus=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='details':self.menus.append(False)
        if tag=='summary' and self.menus and 'teacher-access' in attrs.get('class','').split():self.menus[-1]=True
        if tag=='a':self.current=[attrs,'']
    def handle_data(self,text):
        if self.current:self.current[1]+=text
    def handle_endtag(self,tag):
        if tag=='a' and self.current:
            attrs,text=self.current;href=attrs.get('href','')
            if any(self.menus) or 'teacher-access' in attrs.get('class','').split() or '/docente/' in href or text.strip().lower().startswith('para o docente'):
                self.links.append({'href':href,'label':text.strip() or attrs.get('aria-label','Materiais do docente')})
            self.current=None
        if tag=='details' and self.menus:self.menus.pop()
def inventory():
    result=[]
    for page in sorted(ROOT.rglob('*.html')):
        rel=page.relative_to(ROOT)
        if any(part in ('.git','tests','docs','demonstracoes','node_modules') for part in rel.parts):continue
        parser=Links();parser.feed(page.read_text('utf-8'))
        if parser.links:result.append({'path':rel.as_posix(),'url':'https://pedrohfernandes-klk.github.io/pt/'+rel.as_posix().removesuffix('index.html'),'links':parser.links})
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    text=json.dumps(inventory(),ensure_ascii=False,indent=2)+'\n'
    if args.check:assert DEST.read_text('utf-8')==text,'Inventário desatualizado'
    else:DEST.write_bytes(text.encode('utf-8'))
    print(f'{len(inventory())} páginas com destinos docentes inventariados')

#!/usr/bin/env python3
"""يعيد توليد assets/search-data.js و assets/exercises.js من ملفات الدروس والتمارين.

    python3 scripts/gen_data.py

يُشغَّل بعد كل إضافة أو تعديل لدرس أو تمرين. الملفان مولَّدان بالكامل،
فلا تُحرَّر يدوياً.
"""
import json, os, re, sys, glob
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.root={'tag':'root','attrs':{},'kids':[]}
        self.cur=self.root
        self.void={'meta','link','br','img','input','source','track','hr'}
    def handle_starttag(self,tag,attrs):
        node={'tag':tag,'attrs':dict(attrs),'kids':[]}
        self.cur['kids'].append(node)
        if tag not in self.void:
            self.stack.append(self.cur); self.cur=node
    def handle_endtag(self,tag):
        if tag in self.void: return
        # unwind to matching
        node=self.cur
        chain=[self.cur]+self.stack[::-1]
        for i,n in enumerate(chain):
            if n['tag']==tag:
                for _ in range(i):
                    self.cur=self.stack.pop()
                self.cur=self.stack.pop() if self.stack else self.root
                return
    def handle_data(self,data):
        self.cur['kids'].append(data)

def text_of(node):
    if isinstance(node,str): return node
    # <pre> هو المثال المحسوب: رياضيات لاتينية تزاحم النص العربي في الفهرس
    if node.get('tag') in ('script','style','pre','canvas'): return ' '
    return ' '.join(text_of(k) for k in node['kids'])

def norm(s):
    return re.sub(r'\s+',' ',s).strip()

def find(node,pred,out=None):
    out=[] if out is None else out
    for k in node['kids']:
        if isinstance(k,str): continue
        if pred(k): out.append(k)
        find(k,pred,out)
    return out

def parse_lesson(path):
    html=open(path,encoding='utf-8').read()
    d=Doc(); d.feed(html)
    body=find(d.root,lambda n:n['tag']=='body')[0]
    lid=body['attrs'].get('data-lesson-id')
    h1=norm(text_of(find(body,lambda n:n['tag']=='h1')[0]))
    enl=find(body,lambda n:'en-line' in n['attrs'].get('class',''))
    en=norm(text_of(enl[0])) if enl else ''
    slug=os.path.basename(path)[:-5]
    rec={'id':lid,'title':h1,'en':en,'url':'lessons/%s.html'%slug,'entries':[]}
    idea=find(body,lambda n:'card idea' in n['attrs'].get('class',''))
    rec['entries'].append({'type':'lesson','title':h1,'en':en,
        'text':norm(text_of(idea[0])).replace('فكرة أساسية ','',1) if idea else '',
        'anchor':'','lesson':lid})
    for sec in find(body,lambda n:n['tag']=='section' and n['attrs'].get('id')):
        sid=sec['attrs']['id']
        if sid=='glossary': continue
        h2=find(sec,lambda n:n['tag']=='h2')
        title=norm(text_of(h2[0])) if h2 else ''
        title=re.sub(r'^[٠-٩0-9]+\s*','',title)
        t=norm(text_of(sec))
        if len(t)>600:
            t=t[:600].rsplit(' ',1)[0]
        rec['entries'].append({'type':'section','title':title,'text':t,'anchor':'#'+sid,'lesson':lid})
    gl=find(body,lambda n:n['tag']=='section' and n['attrs'].get('id')=='glossary')
    if gl:
        for tr in find(gl[0],lambda n:n['tag']=='tr'):
            tds=[c for c in tr['kids'] if not isinstance(c,str) and c['tag']=='td']
            if len(tds)>=3:
                rec['entries'].append({'type':'term','title':norm(text_of(tds[0])),
                    'en':norm(text_of(tds[1])),'text':norm(text_of(tds[2])),
                    'anchor':'#glossary','lesson':lid})
    return rec

def main():
    paths=sorted(glob.glob(os.path.join(ROOT,'lessons','*.html')))
    data=[parse_lesson(p) for p in paths]
    out='window.LINALG_DATA = '+json.dumps(data,ensure_ascii=False)+';\n'
    open(os.path.join(ROOT,'assets','search-data.js'),'w',encoding='utf-8').write(out)
    ex={}
    for p in sorted(glob.glob(os.path.join(ROOT,'practice','*.py'))):
        ex[os.path.basename(p)[:-3]]=open(p,encoding='utf-8').read()
    open(os.path.join(ROOT,'assets','exercises.js'),'w',encoding='utf-8').write(
        'window.LINALG_EXERCISES = '+json.dumps(ex,ensure_ascii=False)+';\n')
    print('lessons',len(data),'exercises',len(ex))

if __name__ == "__main__":
    main()

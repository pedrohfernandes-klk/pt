"""02/11/2026: regras públicas dos tipos F2, sem alterar cartões recebidos.

As regras de raciocínio são sinais para a revisão, não prova automática da
qualidade de uma leitura. A extração enumera só campos que podem ser visíveis.
"""
import re
import unicodedata

VERSAO = '20261102-f2'
ENTROU = {t: VERSAO for t in ('lacunas', 'varias', 'montar', 'intruso', 'razao', 'corrigir')}
CONTEXTOS = {'licao', 'nucleo', 'projecao', 'aquecimento'}
_EXTENSOES = {}


def _texto(v):
    return isinstance(v, str) and bool(v.strip())


def _lista_texto(v):
    return isinstance(v, list) and all(_texto(s) for s in v)


def _palavras(s):
    s = unicodedata.normalize('NFD', str(s).casefold())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return set(re.findall(r'[^\W\d_]{4,}', s))


def _indices(v, n):
    return isinstance(v, list) and all(type(i) is int and 0 <= i < n for i in v) and len(set(v)) == len(v)


def _visivel(s):
    return re.sub(r'<[^>]*>', '', s).replace('_', '').replace('**', '')


def validar(x, contexto='licao'):
    """Erros de estrutura/conteúdo; não modifica x, não lança por dados inválidos."""
    if contexto not in CONTEXTOS:
        return ['contexto desconhecido']
    if not isinstance(x, dict):
        return ['cartão: objeto obrigatório']
    t = x.get('t')
    if t in _EXTENSOES:
        return _EXTENSOES[t].validar(x, contexto)
    if t not in ENTROU:
        return ['tipo adicional desconhecido']
    e = []
    def exigir(ok, msg):
        if not ok: e.append(msg)
    for k in ('id', 'p', 'f'):
        exigir(_texto(x.get(k)), k + ': texto obrigatório')
    exigir(isinstance(x.get('id'),str) and bool(re.fullmatch(r'n106-[a-z0-9-]+',x['id'])), 'id: prefixo n106 e identificador estável')
    for k in ('cita', 'p2'):
        if k in x: exigir(_texto(x[k]), k + ': texto não vazio')
    curto = contexto != 'licao'
    if t == 'lacunas':
        es, ds, tx = x.get('espacos'), x.get('distratores'), x.get('texto')
        if not _lista_texto(es) or not _lista_texto(ds) or not _texto(tx):
            return e + ['lacunas: texto, espaços e distratores obrigatórios']
        n = len(es)
        exigir(1 <= n <= (4 if contexto == 'aquecimento' else 5 if curto else 6), 'espacos: limite do contexto')
        exigir(2 <= len(ds) <= 4 and n + len(ds) <= 8, 'banco: até oito blocos e dois a quatro distratores')
        exigir(re.findall(r'\[(\d+)\]', tx) == [str(i) for i in range(1,n+1)], 'texto: espaços únicos por ordem de 1 a n')
        exigir(len(re.sub(r'\[\d+\]', '',tx).split()) <= (40 if contexto=='aquecimento' else 50 if curto else 70), 'texto: limite de palavras')
        exigir(not set(es)&set(ds), 'distratores: não podem ser certos')
        exigir(len(set(ds))==len(ds), 'distratores: sem duplicados')
        for s in es+ds:
            exigir(len(s)<=14 and len(s.split())<=2, 'bloco: até 14 carateres e duas palavras')
        fe = x.get('fe_bloco', {})
        exigir(isinstance(fe,dict), 'fe_bloco: objeto obrigatório')
        for s in ds:
            f=fe.get(s) if isinstance(fe,dict) else None
            exigir(_texto(f) or isinstance(f,dict) and all(_texto(f.get(str(i), f.get('*'))) for i in range(1,n+1)), 'fe_bloco: retorno de cada distrator em cada espaço')
        if 'fe_espaco' in x:
            exigir(_lista_texto(x['fe_espaco']) and len(x['fe_espaco'])==n, 'fe_espaco: um retorno por espaço')
        aceita=x.get('aceita',{})
        exigir(isinstance(aceita,dict), 'aceita: objeto por espaço')
        if isinstance(aceita,dict):
            for k,vs in aceita.items():
                exigir(k in [str(i) for i in range(1,n+1)] and _lista_texto(vs) and all(v in es+ds for v in vs), 'aceita: espaço existente e blocos do banco')
    elif t == 'varias':
        o,cs,fe=x.get('o'),x.get('certas'),x.get('fe')
        if not _lista_texto(o):return e+['o: opções textuais obrigatórias']
        exigir(4<=len(o)<=(4 if contexto=='aquecimento' else 6), 'o: quatro a seis opções, quatro no aquecimento')
        exigir(len(set(o))==len(o), 'o: opções distintas')
        exigir(_indices(cs,len(o)) and 2<=len(cs)<len(o), 'certas: duas a n menos uma, índices únicos')
        exigir(_lista_texto(fe) and len(fe)==len(o), 'fe: retorno para todas as opções')
        exigir(not any(re.search(r'\b(?:todas|nenhuma)\b.*\banteriores\b', s,re.I) for s in o), 'o: sem todas/nenhuma das anteriores')
        if 'diz_quantas' in x:exigir(type(x['diz_quantas']) is bool,'diz_quantas: booleano')
    elif t == 'montar':
        bs,ds=x.get('blocos'),x.get('distratores',[])
        if not _lista_texto(bs) or not _lista_texto(ds):return e+['blocos e distratores: listas de texto']
        exigir(3<=len(bs)<=(6 if curto else 8),'blocos: limite do contexto')
        exigir(len(ds)<=2,'distratores: até dois')
        exigir(not set(bs)&set(ds),'distratores: não podem repetir blocos certos')
        exigir(x.get('fim') in ('.','?','!','…'),'fim: pontuação final obrigatória')
        proprios=x.get('proprios',[])
        exigir(_lista_texto(proprios),'proprios: lista de nomes')
        for s in bs+ds:
            exigir(len(s.split())<=4,'bloco: até quatro palavras')
            exigir(not re.search(r'[.!?…]$',s),'bloco: sem pontuação final')
            exigir(not s[0].isupper() or isinstance(proprios,list) and any(s==p or s.startswith(p+' ') for p in proprios if isinstance(p,str)), 'bloco: maiúscula só em nome próprio declarado')
        exigir(_texto(x.get('fe_ordem')),'fe_ordem: retorno obrigatório')
        fe=x.get('fe_bloco',{})
        for d in ds:exigir(isinstance(fe,dict) and _texto(fe.get(d)),'fe_bloco: retorno de cada distrator')
        ordens=x.get('aceita',[])
        exigir(isinstance(ordens,list),'aceita: lista de ordens')
        if isinstance(ordens,list):
            for a in ordens:
                ordem=a
                if isinstance(a,list) and len(a)==2 and isinstance(a[0],list):
                    ordem=a[0];exigir(_texto(a[1]),'aceita: frase alternativa escrita')
                    if _texto(a[1]):exigir(a[1].endswith(x.get('fim','\0')),'aceita: conservar a pontuação final')
                exigir(_indices(ordem,len(bs)) and len(ordem)==len(bs),'aceita: permutação de todos os blocos')
    elif t in ('intruso','razao'):
        itens,rs,pares=x.get('itens'),x.get('razoes'),x.get('certos')
        if not isinstance(itens,list) or not _lista_texto(rs):return e+['itens e razões: listas obrigatórias']
        exigir((4<=len(itens)<=6) if t=='intruso' else (2<=len(itens)<=3),'itens: limite do tipo')
        exigir(len(rs)==3 if t=='intruso' else len(rs)>=3,'razoes: três no intruso, pelo menos três na razão')
        exigir(len(set(rs))==len(rs),'razoes: distintas')
        imagens=any(isinstance(i,dict) for i in itens)
        exigir(not imagens or t=='intruso' and len(itens)<=4,'imagens: até quatro, apenas no intruso')
        for i in itens:
            if isinstance(i,str):exigir(_texto(i) and len(_visivel(i))<=90,'item: texto até 90 carateres')
            elif isinstance(i,dict):
                for k in ('img','alt','autor','obra','data','origem','licenca'):
                    exigir(_texto(i.get(k)), 'imagem: '+k+' obrigatório')
                lic=i.get('licenca','')
                exigir(bool(re.fullmatch(r'(?:domínio público|CC0(?: 1\.0)?|CC BY(?:-SA)?(?: [1-4]\.0)?)',str(lic),re.I)), 'imagem: licença livre permitida')
                exigir(str(i.get('origem','')).startswith('https://'),'imagem: origem com ligação HTTPS')
            else:exigir(False,'item: texto ou objeto de imagem')
        ps=[]
        if isinstance(pares,list):
            for p in pares:
                if isinstance(p,list) and len(p)==2 and type(p[0]) is int and type(p[1]) is int and 0<=p[0]<len(itens) and 0<=p[1]<len(rs):ps.append(tuple(p))
                else:exigir(False,'certos: par de índices válido')
        exigir(bool(ps) and len(ps)==len(set(ps)),'certos: pelo menos um par, sem duplicados')
        for field,items,ok in [('fe_item',itens,{p[0] for p in ps}),('fe_razao',rs,{p[1] for p in ps})]:
            fs=x.get(field)
            exigir(isinstance(fs,list) and len(fs)==len(items) and all(isinstance(s,str) and (bool(s.strip()) or n in ok) for n,s in enumerate(fs)),field+': alinhado, vazio apenas nos certos')
        if t=='intruso':
            for _,ri in ps:exigir(not _palavras(x.get('p',''))&_palavras(rs[ri]),'p: não revelar o critério da razão certa')
        else:
            for rr in rs:
                for i in itens:
                    if isinstance(i,str):exigir(not _palavras(rr)&_palavras(i),'razao: indício não repete palavras da leitura')
    elif t == 'corrigir':
        parts=x.get('partes') if 'partes' in x else x.get('texto','').split() if isinstance(x.get('texto'),str) else None
        if not _lista_texto(parts) or not parts:return e+['texto/partes: material obrigatório']
        exigir(len(parts)<=(30 if curto else 40),'partes: limite do contexto')
        es=x.get('erros')
        if not isinstance(es,list):return e+['erros: lista obrigatória']
        exigir(1<=len(es)<=(2 if curto else 3),'erros: limite do contexto')
        inds=[]
        for err in es:
            if not isinstance(err,dict):exigir(False,'erro: objeto obrigatório');continue
            em,op,c=err.get('em'),err.get('o'),err.get('c')
            valid=type(em) is int and 0<=em<len(parts)
            exigir(valid,'em: índice válido')
            if valid:inds.append(em)
            exigir(_lista_texto(op) and len(op)==3 and len(set(op))==3,'erro.o: três opções distintas')
            exigir(type(c) is int and 0<=c<3,'erro.c: índice válido')
            exigir(_texto(err.get('fe')),'erro.fe: explicação obrigatória')
            if valid and _lista_texto(op):exigir(all(v!=parts[em].rstrip('.,;:!?…') for v in op),'erro.o: sem repetir a palavra errada')
        exigir(len(inds)==len(set(inds)),'erros: sem índices repetidos')
        arm=x.get('armadilhas',{})
        exigir(isinstance(arm,dict),'armadilhas: objeto')
        if isinstance(arm,dict):
            for k,v in arm.items():exigir(isinstance(k,str) and k.isdigit() and int(k)<len(parts) and int(k) not in inds and _texto(v),'armadilha: palavra certa existente e explicação')
    return e


# IDs, índices, URLs, licenças e chaves de dados não são prosa mostrada ao aluno.
_CAMPOS = {'p','p2','f','fe','texto','partes','espacos','distratores','fe_bloco','fe_espaco','o','blocos','cita','fe_ordem','itens','razoes','fe_item','fe_razao','armadilhas','alt','autor','obra','data','marcas','fe_parte','fe_corte','fica'}


def textos_de(x):
    """Enumera o texto visível, incluindo correções, sem confundir URLs com prosa."""
    out=[]
    def walk(v):
        if isinstance(v,str):out.append(v)
        elif isinstance(v,list):
            for s in v:walk(s)
        elif isinstance(v,dict):
            for s in v.values():walk(s)
    if not isinstance(x,dict):return out
    if x.get('t') in _EXTENSOES:return _EXTENSOES[x['t']].textos_de(x)
    for k in sorted(_CAMPOS):
        if k not in x:continue
        if k=='itens':
            for it in x[k] if isinstance(x[k],list) else []:
                if isinstance(it,str):out.append(it)
                elif isinstance(it,dict):
                    for field in ('alt','autor','obra','data'):walk(it.get(field))
        else:walk(x[k])
    for err in x.get('erros',[]) if isinstance(x.get('erros'),list) else []:
        if isinstance(err,dict):walk(err.get('o'));walk(err.get('fe'))
    for a in x.get('aceita',[]) if isinstance(x.get('aceita'),list) else []:
        if isinstance(a,list) and len(a)==2 and isinstance(a[0],list):walk(a[1])
    return out


def verificar_recursos(html, cartoes):
    """Falha se um tipo é usado sem JS/CSS, antes do motor, ou com versão antiga."""
    tipos={c.get('t') for c in cartoes if isinstance(c,dict)} & ENTROU.keys()
    if not tipos:return []
    erros=[]
    for nome,tag in [('tipos-mais.js','script'),('tipos-mais.css','link')]:
        m=re.search(r'<'+tag+r'\b[^>]*(?:src|href)=[\"\']([^\"\']*'+re.escape(nome)+r'\?v=([^\"\'&]+))[^>]*>',html,re.I)
        if not m:erros.append(nome+': recurso com versão obrigatório');continue
        for t in tipos:
            if m.group(2)<ENTROU[t]:erros.append(nome+': versão anterior à entrada de '+t)
    js=re.search(r'<script\b[^>]*src=[\"\'][^\"\']*tipos-mais\.js',html,re.I)
    montar=html.find('EPIJogo.montar(')
    if js and montar>=0 and js.start()>montar:erros.append('tipos-mais.js: carregar antes de montar')
    if any(c.get('t')=='intruso' and any(isinstance(i,dict) for i in c.get('itens',[])) for c in cartoes):
        for nome in ('ampliar-documentos.js','ampliar-documentos.css'):
            if nome not in html:erros.append(nome+': visor obrigatório para imagens')
    return erros

DICAS_PAPEL = {
 'lacunas':'No caderno, escreve o número de cada espaço e o bloco que lá vai.',
 'varias':'No caderno, escreve as letras de todas as certas.',
 'montar':'No caderno, escreve a frase pela ordem certa.',
 'intruso':'No caderno, escreve a letra do intruso e o número da razão.',
 'razao':'No caderno, escreve a letra da leitura e o número do indício.',
 'corrigir':'No caderno, identifica os erros e escreve as formas corretas.',
}


def campos_opcoes(x):
    """Conjuntos visíveis e índices certos, para as duas medições existentes."""
    t=x.get('t');out=[]
    if t in _EXTENSOES:return _EXTENSOES[t].campos_opcoes(x)
    if t=='lacunas':
        bank=x['espacos']+x['distratores']
        for i,s in enumerate(x['espacos']):
            aceites=[s]+x.get('aceita',{}).get(str(i+1),[])
            out.append({'onde':f'espaço {i+1}','opcoes':bank[:],'certas':[j for j,b in enumerate(bank) if b in aceites]})
    elif t=='varias':out.append({'onde':'afirmações','opcoes':x['o'][:],'certas':x['certas'][:]})
    elif t in ('intruso','razao'):
        out.append({'onde':'razões','opcoes':x['razoes'][:],'certas':sorted({p[1] for p in x['certos']})})
        if all(isinstance(i,str) for i in x['itens']):out.append({'onde':'elementos','opcoes':x['itens'][:],'certas':sorted({p[0] for p in x['certos']})})
    elif t=='corrigir':
        for n,e in enumerate(x['erros'],1):out.append({'onde':f'correção {n}','opcoes':e['o'][:],'certas':[e['c']]})
    return out


def material_publico(x, semente=''):
    """Lista permitida explícita: nunca inclui solução, índices certos ou retornos."""
    if x.get('t') in _EXTENSOES:return _EXTENSOES[x['t']].material_publico(x)
    import copy,hashlib
    def misturar(xs):
        return sorted(copy.deepcopy(xs),key=lambda s:hashlib.sha256((semente+'|'+repr(s)).encode()).hexdigest())
    t=x['t'];m={}
    if 'cita' in x:m['cita']=x['cita']
    if t=='lacunas':m.update(texto=x['texto'],banco=misturar(x['espacos']+x['distratores']))
    elif t=='varias':m['o']=copy.deepcopy(x['o'])
    elif t=='montar':
        bank=misturar(x['blocos']+x.get('distratores',[]))
        if bank==x['blocos']:bank=bank[1:]+bank[:1]
        m.update(banco=bank,fim=x['fim'])
    elif t in ('intruso','razao'):m.update(itens=copy.deepcopy(x['itens']),razoes=x['razoes'][:])
    elif t=='corrigir':m['texto']=' '.join(x['partes']) if 'partes' in x else x['texto']
    return m


def material_html(x,semente=''):
    """Material inicial escapado, sem inferir marcação a partir de HTML recebido."""
    if x.get('t') in _EXTENSOES:return _EXTENSOES[x['t']].material_html(x)
    from html import escape
    def fmt(s):
        s=escape(s)
        s=re.sub(r'\*\*([^*\n]{1,80})\*\*',r'<b>\1</b>',s)
        return re.sub(r'(^|[^\w/])_([^_\n<>]{1,100})_(?!\w)',r'\1<i>\2</i>',s)
    m=material_publico(x,semente);out=[]
    for k in ('cita','texto'):
        if k in m:out.append('<p>'+fmt(m[k])+'</p>')
    for k in ('banco','o','itens','razoes'):
        if k in m:
            values=[]
            for v in m[k]:
                if isinstance(v,str):values.append(fmt(v))
                else:
                    # 03/11/2026: a imagem e o crédito acompanham o material em papel.
                    src=v['img']
                    if re.match(r'(?i)\s*(?:javascript|vbscript):',src):
                        raise ValueError('Endereço de imagem não permitido')
                    values.append('<figure><img src="'+escape(src,quote=True)+'" alt="'+escape(v['alt'],quote=True)+'">'
                                  '<figcaption>'+fmt(v['autor'])+'; '+fmt(v['obra'])+'; '+fmt(v['data'])+'; '
                                  '<a href="'+escape(v['origem'],quote=True)+'">Fonte</a>; '+escape(v['licenca'])+'</figcaption></figure>')
            titulo={'banco':'Blocos disponíveis','o':'Afirmações','itens':'Elementos','razoes':'Razões'}[k]
            tipo=' type="A"' if k in ('o','itens') else ''
            out.append('<p><b>'+titulo+'</b></p><ol'+tipo+'>'+''.join('<li>'+v+'</li>' for v in values)+'</ol>')
    return ''.join(out)


def integrar_extensao(modulo, versao):
    """F3 chama explicitamente este ponto ao integrar; F2 não ativa tipos ausentes."""
    if not isinstance(versao,str) or versao<=VERSAO:
        raise ValueError('A versão da extensão tem de ser posterior à F2')
    for tipo in modulo.TIPOS:
        if tipo in ENTROU:raise ValueError('Tipo já registado: '+tipo)
    for metodo in ('validar','textos_de','material_publico','material_html','campos_opcoes'):
        if not callable(getattr(modulo,metodo,None)):raise ValueError('Interface incompleta: '+metodo)
    if any(t not in modulo.DICAS_PAPEL for t in modulo.TIPOS):raise ValueError('Dica de papel em falta')
    for tipo in modulo.TIPOS:
        _EXTENSOES[tipo]=modulo;ENTROU[tipo]=versao;DICAS_PAPEL[tipo]=modulo.DICAS_PAPEL[tipo]

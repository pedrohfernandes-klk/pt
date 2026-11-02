"""Documentos visuais inspecionados em 01/11/2026, com direitos verificados."""
from html import escape

IMAGENS = {
 'eugenio': dict(autor='Bottelho', obra='Eugénio de Andrade', data='2010',
  instituicao='Publicação do autor no Flickr; reprodução no Wikimedia Commons. Coleção não indicada.',
  licenca='CC BY-SA 2.0', direitos='https://creativecommons.org/licenses/by-sa/2.0/',
  fonte='https://commons.wikimedia.org/wiki/File:Eug%C3%A9nio_de_Andrade.jpg',
  alt='Retrato pintado de Eugénio de Andrade, com pinceladas claras e escuras sobre o rosto.'),
 'amaral': dict(autor='Mattias Blomgren', obra='Ana Luísa Amaral na Feira do Livro de Gotemburgo', data='27 de setembro de 2013',
  instituicao='Wikimedia Commons, publicação do fotógrafo.',
  licenca='CC BY-SA 3.0', direitos='https://creativecommons.org/licenses/by-sa/3.0/',
  fonte='https://commons.wikimedia.org/wiki/File:Ana_Lu%C3%ADsa_Amaral_at_G%C3%B6teborg_Book_Fair_2013_01.JPG',
  alt='Ana Luísa Amaral fotografada na Feira do Livro de Gotemburgo, com um lenço coral.'),
 'piranesi': dict(autor='Giovanni Battista Piranesi', obra='Vista interior da Basílica de São Pedro, da série Vedute di Roma', data='Cerca de 1748',
  instituicao='The Metropolitan Museum of Art, inventário 1972.620.1. Oferta de Mrs. Otto F. Langmann, 1972.',
  licenca='Domínio público', direitos='https://www.metmuseum.org/art/collection/search/353966',
  fonte='https://www.metmuseum.org/art/collection/search/353966',
  alt='Gravura do interior da Basílica de São Pedro: pequenas figuras humanas entre colunas e abóbadas monumentais.'),
}

USOS = {
 'm8-f13': ('eugenio', 'Eugénio de Andrade, num retrato de Bottelho (2010).'),
 'm8-f14': ('amaral', 'Ana Luísa Amaral na Feira do Livro de Gotemburgo, em 2013.'),
 'm9-f14': ('piranesi', 'A escala das figuras humanas permite comparar dimensão e grandeza. A gravura representa a basílica, não a miniatura do rei nem a cena do romance.'),
}

def aplicar_imagens(bancos):
    for item in bancos:
        if item['id'] not in USOS:
            continue
        nome,legenda=USOS[item['id']];d=IMAGENS[nome]
        rows=''.join('<tr><th scope="row">'+label+'</th><td>'+(escape(d[key]).replace('Vedute di Roma','<i>Vedute di Roma</i>'))+'</td></tr>' for label,key in
                     [('Autor','autor'),('Obra','obra'),('Data','data'),('Instituição ou acervo','instituicao')])
        rows+='<tr><th scope="row">Licença</th><td><a href="'+d['direitos']+'">'+d['licenca']+'</a></td></tr>'
        opening=item['cards'][0]['html']
        item['cards'][0]['html'] = ('<figure class="fig documento"><a href="../../img/fontes/licoes-20261101/'+nome+'.jpg" aria-label="Abrir a imagem inteira">'
          '<img src="../../img/fontes/licoes-20261101/'+nome+'.jpg" alt="'+escape(d['alt'],quote=True)+'"></a>'
          '<figcaption><p>'+legenda+'</p><p>'+d['licenca']+'; <a href="'+d['fonte']+'">Fonte ↗</a></p><details><summary>Créditos e fonte da imagem</summary><table><caption>Identificação do documento visual</caption>'+rows+'</table>'
          '<p><a href="'+d['fonte']+'">Consultar a fonte e os direitos ↗</a>. Reprodução redimensionada, sem recorte.</p></details></figcaption></figure>')+opening

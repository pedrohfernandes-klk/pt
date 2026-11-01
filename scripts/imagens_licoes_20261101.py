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

# 01/11/2026: documentos existentes, inspecionados antes da integração no pedido B.
def documento(nome, autor, obra, data, instituicao, fonte, alt, obra_html=None):
    IMAGENS[nome] = dict(autor=autor, obra=obra, data=data, instituicao=instituicao,
        fonte=fonte, direitos=fonte, licenca='Domínio público', alt=alt,
        ficheiro='../../img/fontes/'+nome+'.jpg', obra_html=obra_html)

documento('cancioneiro-ajuda-21r', 'Iluminador não identificado',
 'Iluminura do Cancioneiro da Ajuda, fólio 21r', 'Manuscrito medieval',
 'Biblioteca da Ajuda; reprodução no Wikimedia Commons, a partir do projeto Cantigas Medievais Galego-Portuguesas.',
 'https://commons.wikimedia.org/wiki/File:Cancioneiro_da_Ajuda_folio_21r.jpg',
 'Iluminura com uma figura sentada, um músico de pé e uma figura com pandeiro.',
 'Iluminura do <i>Cancioneiro da Ajuda</i>, fólio 21r')
documento('gil-vicente-copilacam-1562', 'Gil Vicente; impressão de João Álvares; reprodução de Victorcouto',
 'Copilacam de todalas obras de Gil Vicente, página de título', '1562',
 'Wikimedia Commons. Coleção do exemplar não indicada na fonte da reprodução.',
 'https://commons.wikimedia.org/wiki/File:Imagem160_Gil_Vicente._Compila%C3%A7am_de_todalas_obras._Joam_Alvarez_impressor._Lisboa,_1562.jpg',
 'Página de título com as armas reais portuguesas e a indicação da impressão em Lisboa, em 1562.',
 '<i>Copilacam de todalas obras de Gil Vicente</i>, página de título')
documento('camoes-rimas-1595', 'Luís de Camões; impressão de Manuel de Lira; reprodução anónima',
 'Rhythmas, página de título', '1595',
 'Wikimedia Commons. Coleção do exemplar não indicada na fonte da reprodução.',
 'https://commons.wikimedia.org/wiki/File:Cam%C3%B5es_-_Rimas_1595.jpg',
 'Página de título de Rhythmas, com uma árvore e a data de 1595 em numeração romana.',
 '<i>Rhythmas</i>, página de título')
documento('os-maias-1888', 'Eça de Queirós; edição da Livraria Internacional de Ernesto Chardron',
 'Os Maias, volume I, página de título', '1888',
 'Wikimedia Commons. Coleção do exemplar não indicada na fonte da reprodução.',
 'https://commons.wikimedia.org/wiki/File:Os_Maias_Book_Cover.jpg',
 'Página de título de Os Maias, volume I, com o nome de Eça de Queirós e a edição do Porto de 1888.',
 '<i>Os Maias</i>, volume I, página de título')
documento('camilo-1882', 'União, Photographia da Casa Real, Porto',
 'Retrato de Camilo Castelo Branco', '7 de março de 1882',
 'Wikimedia Commons. Coleção original não indicada.',
 'https://commons.wikimedia.org/wiki/File:Camilo_Castelo_Branco_(1882)_-_Uni%C3%A3o_%E2%80%93_Photographia_da_Casa_Real-Porto.png',
 'Fotografia de Camilo Castelo Branco sentado, com óculos e bigode.')
documento('antero-de-quental-1887', 'Fotógrafo não identificado',
 'Retrato de Antero de Quental', 'Cerca de 1887; publicado em In Memoriam, 1896',
 'Biblioteca Nacional de Portugal; reprodução no Wikimedia Commons.',
 'https://commons.wikimedia.org/wiki/File:Antero_de_Quental_(ca._1887).jpg',
 'Retrato fotográfico de Antero de Quental, de barba e perfil a três quartos.')
documento('cesario-verde-columbano-1887', 'Columbano Bordalo Pinheiro',
 'Retrato de Cesário Verde', '1887',
 'Publicado em O Livro de Cesário Verde; reprodução no Wikimedia Commons.',
 'https://commons.wikimedia.org/wiki/File:CesarioVerde_Columbano.jpg',
 'Retrato desenhado de Cesário Verde, com bigode, assinado por Columbano.')
USOS.update({
 'm1-f21': ('cancioneiro-ajuda-21r', 'Iluminura do <i>Cancioneiro da Ajuda</i>: um documento da cultura das cantigas. Não representa Pero da Ponte nem identifica os versos lidos nesta lição.'),
 'm2-f14': ('gil-vicente-copilacam-1562', 'A compilação das obras de Gil Vicente foi impressa em Lisboa em 1562.'),
 'm2-f16': ('gil-vicente-copilacam-1562', 'Página de título da compilação das obras de Gil Vicente, de 1562. Não é uma imagem da representação da farsa.'),
 'm3-f19': ('camoes-rimas-1595', 'Página de título de <i>Rhythmas</i>, de 1595, uma edição póstuma da poesia de Camões.'),
 'm5-f16': ('os-maias-1888', 'O primeiro volume de <i>Os Maias</i>, na edição de 1888.'),
 'm5-f17': ('camilo-1882', 'Camilo Castelo Branco, fotografado em 1882. O retrato identifica o autor, não a personagem de Simão.'),
 'm6-f14': ('antero-de-quental-1887', 'Antero de Quental num retrato de cerca de 1887, posterior à conferência de 1871.'),
 'm6-f15': ('cesario-verde-columbano-1887', 'Cesário Verde retratado por Columbano em 1887.'),
})
IMAGENS['antero-de-quental-1887']['data_html'] = 'Cerca de 1887; publicado em <i>In Memoriam</i>, 1896'
IMAGENS['cesario-verde-columbano-1887']['instituicao_html'] = 'Publicado em <i>O Livro de Cesário Verde</i>; reprodução no Wikimedia Commons.'

def aplicar_imagens(bancos):
    for item in bancos:
        if item['id'] not in USOS:
            continue
        nome,legenda=USOS[item['id']];d=IMAGENS[nome]
        rows=''.join('<tr><th scope="row">'+label+'</th><td>'+(d.get(key+'_html') or escape(d[key]).replace('Vedute di Roma','<i>Vedute di Roma</i>'))+'</td></tr>' for label,key in
                     [('Autor','autor'),('Obra','obra'),('Data','data'),('Instituição ou acervo','instituicao')])
        rows+='<tr><th scope="row">Licença</th><td><a href="'+d['direitos']+'">'+d['licenca']+'</a></td></tr>'
        ficheiro=d.get('ficheiro','../../img/fontes/licoes-20261101/'+nome+'.jpg')
        opening=item['cards'][0]['html']
        item['cards'][0]['html'] = ('<figure class="fig documento"><a href="'+ficheiro+'" aria-label="Abrir a imagem inteira">'
          '<img src="'+ficheiro+'" alt="'+escape(d['alt'],quote=True)+'"></a>'
          '<figcaption><p>'+legenda+'</p><p>'+d['licenca']+'; <a href="'+d['fonte']+'">Fonte ↗</a></p><details><summary>Créditos e fonte da imagem</summary><table><caption>Identificação do documento visual</caption>'+rows+'</table>'
          '<p><a href="'+d['fonte']+'">Consultar a fonte e os direitos ↗</a>. Reprodução redimensionada, sem recorte.</p></details></figcaption></figure>')+opening

# Mapa de Português e circunflexo com cor

Baseline `ab8deafb5fba917e141fe5b4ed2efff7546c7404`. Mapa de orientação em `/mapa/`, acessível da entrada: três anos, nove módulos e respetivas coleções, Atlas, ajuda e ligações ao LENTE. Os módulos abrem por escolha; não são repetidas as 101 lições numa lista extensa. As ligações entre mapas serão confirmadas após os dois deployments.

O título original mantém o texto «Português» e esse nome acessível explícito. Uma camada tipográfica decorativa, oculta à acessibilidade, pinta apenas o circunflexo; a letra original permanece intacta e selecionável. Vermelho terroso em tema claro, mostarda no esquema escuro e camada removida em cores forçadas. Cor também nos sinais de orientação do mapa, sem novas imagens, fontes ou JavaScript.

## Verificações

- Seis scripts raw idênticos (finais de linha incluídos); nove linhas de módulos, IDs, atributos de estado e todos os destinos anteriores preservados. Revisão independente favorável. O mapa não tem scripts, ligações aninhadas ou destinos inventados; 42 destinos PT únicos confirmados nas fontes locais; os restantes são ligações explícitas ao LENTE.
- Navegador real: os nove módulos do mapa abrem com Enter e fecham com Espaço. Mapa aberto e recolhido em 320, 390, 768 e 1440 px, larguras CSS confirmadas, sem overflow. Verificação adicional chegou a 264 px sem overflow. Foco visível e captura antes da publicação guardada.
- Circunflexo inspecionado em computador e telemóvel; correção do recorte para não pintar o topo da letra E. Título DOM e nome acessível «Português» confirmados, com refluxo sem overflow nas mesmas quatro larguras. Estado local de continuação, contagens e progresso igual antes/depois.
- Mapa ligou-se a partir da entrada em navegador. Folha CSS dos mapas limita as regras de página a `.site-map` e classes próprias, preservando as páginas existentes. Contrastes usam a paleta já verificada.

## Limites e manutenção

Não executados leitor de ecrã real, dispositivos físicos, mudança real do esquema escuro, zoom real 200% ou benchmark de rede/desempenho; verificações complementares pendentes. Não foram repetidos os exercícios, cujo código não mudou. A pintura depende da métrica da fonte carregada; a letra original assegura legibilidade mesmo sem a camada decorativa. Não é certificação integral do site.

Ao adicionar/remover coleções, rever também `/mapa/` e verificar os destinos. Guardar o mapa como orientação, sem criar páginas ou fragmentos só para aparentar uma estrutura inexistente. Deployments e percursos públicos finais registados no PR.

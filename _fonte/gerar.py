"""Gera as páginas do site a partir de um modelo único (topo, rodapé e faixa de contato iguais em todas).
Rode: python3 _fonte/gerar.py  (na raiz do repositório)"""
import os, html
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORES = [("Preto", "#1C1C1E"), ("Cinza Grafite", "#3C3F44"), ("Cinza Claro", "#A8ACB0"), ("Branco Dental", "#ECE7DC"),
         ("Marrom", "#5E3B25"), ("Vermelho", "#C3161F"), ("Laranja", "#EF6A1C"), ("Amarelo", "#F2C300"), ("Azul", "#1F5BC4"),
         ("Verde", "#1F8A40"), ("Natural Translúcido", "#E6ECEE"), ("Azul Marinho Translúcido", "#1A2D69"),
         ("Verde Neon Translúcido", "#5FD43A"), ("Laranja Neon Translúcido", "#FF6B1E"), ("Branco Blackout", "#F6F6F3"),
         ("Fibra de Carbono", "#2C2C2E")]

PAGINAS = [("index.html", "Início"), ("pecas.html", "Peças"), ("como-funciona.html", "Como funciona"), ("a-marca.html", "A marca")]

def fio(ponto=True):
    c = '<circle cx="50%" cy="102" r="5"/>' if ponto else ''
    return f'<div class="fio" aria-hidden="true"><svg><path d=""/>{c}</svg></div>'

def trecho(classe, conteudo, id_=None, ponto=True):
    i = f' id="{id_}"' if id_ else ''
    return f'<section class="trecho {classe}"{i}>\n  {fio(ponto)}\n  <div class="conteudo">\n{conteudo}\n  </div>\n</section>'

def pagina(arquivo, titulo, descricao, corpo, extra_head='', extra_fim=''):
    nav = '\n    '.join(f'<a href="{a}"' + (' aria-current="page"' if a == arquivo else '') + f'>{n}</a>' for a, n in PAGINAS)
    contato = trecho('faixa-contato', '''    <h2>Vamos criar a sua peça</h2>
    <p>Conte o que você precisa. Respondemos com ideias, cores e orçamento.</p>
    <div class="acoes"><a class="botao cheio" data-whatsapp href="#contato">Chamar no WhatsApp</a></div>
    <dl>
      <dt>WhatsApp</dt><dd data-whatsapp-texto>[NÚMERO A DEFINIR]</dd>
      <dt>Instagram</dt><dd><a href="https://www.instagram.com/radix.atelie/" target="_blank" rel="noopener">@radix.atelie</a></dd>
      <dt>Ateliê</dt><dd>Florianópolis, SC. Enviamos para todo o Brasil.</dd>
    </dl>''', 'contato')
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{html.escape(descricao)}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:image" content="img/compartilhar.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#000000">
<link rel="icon" href="img/icone-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="img/icone-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra_head}</head>
<body>

<header class="topo">
  <a class="nome" href="index.html">RADIX ATELIÊ</a>
  <button class="menu" type="button" aria-expanded="false" aria-controls="navegacao">Menu</button>
  <nav id="navegacao" aria-label="Páginas">
    {nav}
    <a href="#contato">Contato</a>
  </nav>
</header>

<main>
{corpo}
{contato}
</main>

<footer>
  <img src="img/icone-180.png" width="180" height="180" alt="">
  Radix Ateliê, impressão 3D personalizada
</footer>
{extra_fim}<script src="site.js"></script>
</body>
</html>
'''

def amostras():
    return '\n'.join(f'      <span role="listitem" title="{n}" style="background:{h}"></span>' for n, h in CORES)

# ---------------- INÍCIO ----------------
escolha = '\n'.join(f'          <button type="button" title="{n}" data-cor="{h}" style="background:{h}" aria-pressed="{str(n == "Laranja").lower()}"><span class="sr">{n}</span></button>'
                    for n, h in CORES if n not in ("Natural Translúcido",))
inicio = '\n'.join([
trecho('abertura', '''    <div>
      <h1>Peças em impressão 3D com a identidade da sua marca</h1>
      <p class="sub">Chaveiros, mimos e brindes personalizados para a sua empresa, do primeiro desenho à peça pronta.<br>Produção em Florianópolis.</p>
      <div class="acoes">
        <a class="botao cheio" data-whatsapp href="#contato">Pedir orçamento no WhatsApp</a>
        <a class="botao contorno" href="pecas.html">Ver as peças</a>
      </div>
    </div>
    <div class="marca"><img src="img/logo-radix-atelie.webp" width="1000" height="1107" alt="Logo Radix Ateliê: uma árvore cujos galhos saem de um bico de impressora 3D, que imprime o nome Radix com raízes."></div>
    <ul class="fatos" aria-label="Em resumo">
      <li><strong>A partir de 1 peça</strong>Sem molde, sem lote mínimo de fábrica</li>
      <li><strong>Simulação em 3D</strong>Você aprova o desenho antes de imprimir</li>
      <li><strong>16 cores</strong>Sólidas, translúcidas e especiais</li>
      <li><strong>Até 25 cm</strong>Do chaveiro à peça de decoração</li>
    </ul>''', ponto=False),
trecho('secao', f'''    <h2>Veja antes de imprimir</h2>
    <p>Todo pedido começa assim: você recebe a peça em 3D, vê de todos os ângulos e escolhe a cor antes de qualquer impressão. Experimente com um dos nossos chaveiros.</p>
    <div class="vitrine">
      <figure class="palco-moldura">
        <div class="palco" id="palco" aria-label="Chaveiro em 3D. Arraste para ver de outros ângulos.">
          <img src="img/mandala.webp" width="900" height="956" alt="Chaveiro em forma de mandala laranja com argola de metal.">
        </div>
        <figcaption>Arraste para ver de outros ângulos</figcaption>
      </figure>
      <div class="ficha">
        <h3>Chaveiro de armário</h3>
        <dl>
          <dt>Tamanho</dt><dd>4 cm de diâmetro</dd>
          <dt>Material</dt><dd>PETG</dd>
          <dt>Verso</dt><dd>Número em outra cor, nivelado com a peça</dd>
        </dl>
        <div class="lado" role="group" aria-label="Lado da peça">
          <button type="button" id="ver-frente" aria-pressed="true">Frente</button>
          <button type="button" id="ver-verso" aria-pressed="false">Verso</button>
        </div>
        <p class="rotulo">Cor <span class="nome-cor">Laranja</span></p>
        <div class="escolha" role="group" aria-label="Cor do chaveiro">
{escolha}
        </div>
      </div>
    </div>''', 'veja'),
trecho('secao', '''    <h2>O que fazemos</h2>
    <div class="destaques">
      <a href="pecas.html#chaveiros"><img src="img/mandala.webp" width="900" height="956" loading="lazy" alt=""><h3>Chaveiros personalizados</h3><p>Com o seu logo, o nome da empresa ou um número para cada armário.</p></a>
      <a href="pecas.html#mimos"><img src="img/boca.webp" width="900" height="731" loading="lazy" alt=""><h3>Mimos para clientes</h3><p>Ímã de geladeira, abridor de latinha ou etiqueta NFC que abre o seu Instagram.</p></a>
      <a href="pecas.html#sob-medida"><img src="img/marcador.webp" width="900" height="956" loading="lazy" alt=""><h3>Peças sob medida</h3><p>Se você tem uma ideia de até 25 cm, a gente desenha.</p></a>
    </div>
    <div class="acoes"><a class="botao contorno" href="pecas.html">Ver peças, cores e acabamentos</a></div>'''),
trecho('secao', '''    <div class="manifesto">
      <blockquote>Abrace o seu cliente.</blockquote>
      <p>Não é só um brinde. É um jeito de mostrar ao seu cliente que você se importa com ele, num detalhe que ele leva para casa.</p>
      <a href="a-marca.html">Conheça a história da Radix</a>
    </div>'''),
])

# ---------------- PEÇAS ----------------
pecas = '\n'.join([
trecho('cabeca-pagina', '''    <h1>Peças</h1>
    <p>Cada peça é desenhada para o seu pedido. Você vê a simulação em 3D antes de qualquer impressão.</p>''', ponto=False),
trecho('secao', '''    <article class="peca" id="chaveiros">
      <div class="foto"><img src="img/mandala.webp" width="900" height="956" loading="lazy" alt="Chaveiro em forma de mandala laranja com argola de metal."></div>
      <div>
        <h3>Chaveiros personalizados</h3>
        <p>Com o seu logo, o nome da empresa ou um número para cada armário. Leves e resistentes para o uso diário.</p>
        <p class="detalhe">Dá para combinar duas cores na mesma peça, como o número em preto no verso de um chaveiro laranja.</p>
      </div>
    </article>
    <article class="peca" id="mimos">
      <div class="foto"><img src="img/boca.webp" width="900" height="731" loading="lazy" alt="Peça vermelha em forma de lábios."></div>
      <div>
        <h3>Mimos para clientes</h3>
        <p>Lembranças para entregar aos seus clientes, em eventos ou em datas especiais. Podem virar ímã de geladeira, abridor de latinha ou levar uma etiqueta NFC: o cliente encosta o celular e abre o seu Instagram ou WhatsApp.</p>
      </div>
    </article>
    <article class="peca" id="sob-medida">
      <div class="foto"><img src="img/marcador.webp" width="900" height="956" loading="lazy" alt="Marcador de livro em forma de dragão cinza com asas abertas."></div>
      <div>
        <h3>Peças sob medida</h3>
        <p>Marcadores de livro, enfeites, suportes e o que mais você imaginar, em peças de até 25 cm. Se você tem uma ideia, a gente desenha.</p>
      </div>
    </article>''', 'o-que-fazemos', ponto=False),
trecho('secao', '''    <h2>Para quem</h2>
    <p>Qualquer negócio que queira ser lembrado por um detalhe bem feito. Alguns exemplos:</p>
    <dl class="usos">
      <div><dt>Clínicas, salões e consultórios</dt><dd>Mimos de atendimento, chaveiros de armário numerados, suportes com a marca no balcão.</dd></div>
      <div><dt>Empresas e escritórios</dt><dd>Brindes com o logo para clientes e kits de boas-vindas para a equipe.</dd></div>
      <div><dt>Eventos e celebrações</dt><dd>Lembranças personalizadas com nome ou data, marcadores de mesa, peças para decoração.</dd></div>
      <div><dt>Lojas e marcas</dt><dd>Brindes na compra, chaveiros da marca, pequenos expositores sob medida.</dd></div>
      <div><dt>Escolas, academias e clubes</dt><dd>Chaveiros numerados, identificação de armários e lembranças de turma ou de equipe.</dd></div>
      <div><dt>Para presentear</dt><dd>Uma peça única, desenhada a partir de uma ideia sua.</dd></div>
    </dl>''', 'para-quem'),
trecho('secao', f'''    <h2>Cores e acabamentos</h2>
    <p>Trabalhamos com PETG, um plástico resistente da mesma família do usado em garrafas de água. São 16 opções, entre sólidas, translúcidas e especiais.</p>
    <div class="amostras" role="list" aria-label="Cores disponíveis">
{amostras()}
    </div>
    <a class="botao contorno" href="cores.html">Abrir a cartela de cores</a>
    <h3 class="subtitulo">Acabamentos e extras</h3>
    <dl class="usos extras">
      <div><dt>Duas cores na mesma peça</dt><dd>Como um número preto encaixado, nivelado, no verso de uma peça laranja.</dd></div>
      <div><dt>Etiqueta NFC</dt><dd>Embutida na peça. Com um toque do celular, abre o seu Instagram, WhatsApp ou site.</dd></div>
      <div><dt>Ímã</dt><dd>Para a peça virar ímã de geladeira ou de painel.</dd></div>
      <div><dt>Argola e corrente</dt><dd>Para chaveiros e pingentes.</dd></div>
      <div><dt>Abridor de latinha</dt><dd>Embutido no próprio desenho, sem peça de metal.</dd></div>
      <div><dt>Tem outra ideia?</dt><dd>Um encaixe, um suporte, uma peça que se mexe ou um detalhe que não está nesta lista. Conte o que você imaginou e a gente estuda junto.</dd></div>
    </dl>''', 'cores'),
])

# ---------------- COMO FUNCIONA ----------------
como = '\n'.join([
trecho('cabeca-pagina', '''    <h1>Como funciona</h1>
    <p>Da ideia à peça na sua mão, você acompanha cada etapa.</p>''', ponto=False),
trecho('secao', '''    <ol class="passos">
      <li><div><h3>Você conta a ideia</h3><p>Pelo WhatsApp, com o seu logo, uma foto ou uma referência que você goste. Diga também quantas peças precisa e para quando.</p></div></li>
      <li><div><h3>Desenhamos a peça</h3><p>Você recebe a simulação em 3D, com medidas e cores, e aprova antes de imprimir.</p></div></li>
      <li><div><h3>Amostra</h3><p>Em pedidos maiores, imprimimos uma peça de teste para você ver e pegar na mão.</p></div></li>
      <li><div><h3>Produção e entrega</h3><p>Com o desenho aprovado, produzimos o lote e combinamos a entrega.</p></div></li>
    </ol>''', 'etapas', ponto=False),
trecho('secao', '''    <h2>Por que impressão 3D</h2>
    <div class="vantagens">
      <div><h3>Sem molde</h3><p>A peça é construída camada por camada direto do arquivo. Sem custo de molde, um pedido pequeno também fica viável.</p></div>
      <div><h3>Cada peça pode ser diferente</h3><p>Nome, número ou data em cada unidade, no mesmo lote, sem custo extra de ferramenta.</p></div>
      <div><h3>Você vê antes</h3><p>Antes de imprimir, você recebe a simulação em 3D. Em pedidos maiores, também uma amostra.</p></div>
      <div><h3>Material resistente</h3><p>PETG: um plástico firme e durável, que aguenta o dia a dia no chaveiro, na bolsa ou na geladeira.</p></div>
    </div>''', 'por-que-3d'),
trecho('secao', '''    <h2>Preço e entrega</h2>
    <div class="vantagens">
      <div><h3>Preço por quantidade</h3><p>O valor por peça diminui conforme o tamanho do pedido. Mande quantas peças você precisa e respondemos com o orçamento.</p></div>
      <div><h3>Entrega em Florianópolis</h3><p>Retirada ou entrega combinadas no orçamento.</p></div>
      <div><h3>Envio para todo o Brasil</h3><p>Pelos Correios. O frete depende do peso e do CEP de destino, então calculamos antes de você fechar o pedido e ele já vem no orçamento.</p></div>
      <div><h3>Prazo</h3><p>Entregas a partir de 1 dia útil.</p><p class="obs">O prazo varia conforme o tamanho e a quantidade de peças, a complexidade do desenho e o local de entrega. Ele é confirmado no orçamento, antes de você fechar.</p></div>
    </div>''', 'entrega'),
trecho('secao', '''    <h2>Dúvidas frequentes</h2>
    <div class="faq">
      <details><summary>Preciso ter o desenho pronto?</summary><p>Não. Pode mandar o seu logo, uma foto ou só a ideia. A gente desenha a peça e envia a simulação em 3D para você aprovar.</p></details>
      <details><summary>Dá para ver a peça antes de fazer o pedido todo?</summary><p>Sim. Você aprova a simulação em 3D antes de qualquer impressão, e em pedidos maiores imprimimos uma amostra.</p></details>
      <details><summary>Qual a quantidade mínima?</summary><p>A partir de 1 peça. O preço por unidade cai conforme a quantidade, por isso vale contar quantas você precisa no pedido de orçamento.</p></details>
      <details><summary>Qual o prazo?</summary><p>Entregas a partir de 1 dia útil. O prazo varia conforme o tamanho e a quantidade de peças, a complexidade do desenho e o local de entrega, e é confirmado no orçamento.</p></details>
      <details><summary>Cada peça pode ter um nome ou número diferente?</summary><p>Pode. Na impressão 3D cada unidade pode ser diferente, no mesmo lote.</p></details>
      <details><summary>Vocês enviam para outras cidades?</summary><p>Sim, para todo o Brasil pelos Correios. O frete é calculado pelo peso e pelo CEP e vem junto no orçamento.</p></details>
      <details><summary>A peça aguenta uso no dia a dia?</summary><p>Sim. O PETG é firme e resistente a quedas e ao uso no chaveiro ou na bolsa. Só evite deixar a peça em lugares muito quentes, como o painel do carro ao sol.</p></details>
    </div>''', 'duvidas'),
])

# ---------------- A MARCA ----------------
marca = '\n'.join([
trecho('cabeca-pagina', '''    <h1>A marca</h1>
    <p>Toda árvore começa embaixo da terra, muito antes da primeira folha.</p>''', ponto=False),
trecho('secao', '''    <div class="carta-bloco">
    <figure class="retrato"><img src="img/pedro.webp" width="560" height="700" alt="Pedro, fundador da Radix Ateliê, sorrindo num jardim."></figure>
    <div class="carta">
      <p class="abre">A Radix nasceu de uma vontade antiga: criar raiz.</p>
      <p>Foram quase vinte anos na área comercial. Vendi de tudo, de tecnologia a roupa esportiva, de consultorias a projetos de estrutura, sempre com a mão na massa. Dediquei boa parte da vida a fazer outras empresas crescerem. Chegou a hora de construir algo meu: algo que faça sentido, que faça parte de mim e que não fique só na memória.</p>
      <p>Em todos esses anos, sempre me apresentei como alguém que resolve problemas. E um problema eu vi de perto, muitas e muitas vezes: o atendimento. É ali, num momento sensível e muitas vezes delicado, que o cliente decide se fica ou se vai embora. E é ali que tanta empresa falha, às vezes por muito pouco.</p>
      <p>A Radix existe para esse pouco. Uma peça feita para o seu cliente não é só um brinde nem só um mimo. É um gesto. É o jeito de dizer, sem precisar de palavras, que você se importa com quem escolheu você.</p>
      <p>Abrace o seu cliente. Deixe que ele se sinta abraçado.</p>
      <p class="assina">Pedro<span>Fundador da Radix Ateliê</span></p>
    </div>
    </div>''', 'historia', ponto=False),
trecho('secao', '''    <h2>O que a logo conta</h2>
    <div class="historia">
      <div class="texto">
        <h3>O nome</h3>
        <p>Radix quer dizer raiz, em latim. É de onde tudo nasce e o que mantém tudo de pé, mesmo quando ninguém vê. Ateliê porque aqui nada sai de uma linha de produção: cada peça é pensada, desenhada e feita para alguém.</p>
        <h3>O símbolo</h3>
        <p>O desenho une duas formas que geram vida: a árvore e a anatomia feminina. As duas se ramificam do mesmo jeito, e não por acaso: no colo do útero existe uma estrutura que a medicina chama de <i>arbor vitae</i>, "árvore da vida" em latim.</p>
        <h3>O caminho de cada peça</h3>
        <p>Na logo, a copa cresce, as fibras se unem e passam pelo bico de uma impressora 3D. O fio que sai dele escreve o nome, e o nome cria raízes. É o caminho de tudo o que fazemos: uma ideia que ganha forma, vira matéria e permanece.</p>
      </div>
      <figure class="simbolo"><img src="img/simbolo.webp" width="900" height="654" loading="lazy" alt="Símbolo da Radix: galhos com folhas que se unem e descem até um bico de impressora 3D, de onde sai um fio."></figure>
    </div>''', 'logo'),
])

TRES = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n'
saidas = {
 'index.html': pagina('index.html', 'Radix Ateliê | Impressão 3D personalizada', 'Chaveiros, mimos, brindes e peças personalizadas em impressão 3D para empresas e marcas. Desenho próprio, produção em Florianópolis.', inicio, extra_fim=TRES),
 'pecas.html': pagina('pecas.html', 'Peças | Radix Ateliê', 'Chaveiros, mimos e peças sob medida em impressão 3D, em 16 cores de PETG, com NFC, ímã, argola e duas cores na mesma peça.', pecas),
 'como-funciona.html': pagina('como-funciona.html', 'Como funciona | Radix Ateliê', 'Da ideia à peça pronta: simulação em 3D, amostra, produção e envio para todo o Brasil.', como),
 'a-marca.html': pagina('a-marca.html', 'A marca | Radix Ateliê', 'A história da Radix Ateliê e o que a nossa logo conta.', marca),
}
for nome, conteudo in saidas.items():
    open(os.path.join(RAIZ, nome), 'w', encoding='utf-8').write(conteudo)
print('ok', list(saidas))

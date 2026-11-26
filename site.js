{
// WhatsApp: preencha o número (55 + DDD + número, só dígitos) para ativar todos os botões do site.
const WHATSAPP = '';            // exemplo: '5548999999999'
const MENSAGEM = 'Olá! Quero um orçamento de peças em impressão 3D.';
if (WHATSAPP) {
  const link = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(MENSAGEM);
  document.querySelectorAll('[data-whatsapp]').forEach(a => { a.href = link; a.target = '_blank'; a.rel = 'noopener'; });
  const n = WHATSAPP.replace(/^55(\d{2})(\d{4,5})(\d{4})$/, '($1) $2-$3');
  document.querySelectorAll('[data-whatsapp-texto]').forEach(el => el.textContent = n);
}

// Contador de visitas (GoatCounter, gratuito e sem cookies). Crie a conta em goatcounter.com e coloque o código aqui.
const CONTADOR = '';            // exemplo: 'radixatelie'  (vira radixatelie.goatcounter.com)
if (CONTADOR) {
  const sc = document.createElement('script');
  sc.async = true; sc.src = 'https://gc.zgo.at/count.js';
  sc.dataset.goatcounter = 'https://' + CONTADOR + '.goatcounter.com/count';
  document.head.appendChild(sc);
}

// Menu no celular
const menu = document.querySelector('.menu'), nav = document.querySelector('.topo nav');
if (menu) menu.addEventListener('click', () => {
  const aberto = nav.classList.toggle('aberto');
  menu.setAttribute('aria-expanded', aberto);
});

// Fio: linha ondulada contínua na margem, recalculada para a altura de cada seção.
function desenhaFio() {
  let lado = 1;
  document.querySelectorAll('.fio').forEach((col, i) => {
    const path = col.querySelector('path'); const h = col.offsetHeight; const w = col.offsetWidth;
    const cx = w / 2, amp = Math.min(w * 0.32, 14);
    const y0 = i === 0 ? Math.min(h * 0.08, 60) : 0, n = Math.max(1, Math.round((h - y0) / 260)), passo = (h - y0) / n;
    let d = `M ${cx} ${y0}`, y = y0;
    for (let k = 0; k < n; k++) {
      const y2 = y + passo;
      d += ` C ${cx + amp * lado} ${y + passo * 0.35}, ${cx + amp * lado} ${y + passo * 0.65}, ${cx} ${y2}`;
      y = y2; lado = -lado;
    }
    path.setAttribute('d', d);
    path.style.setProperty('--len', path.getTotalLength());
  });
}
desenhaFio();
addEventListener('resize', desenhaFio);
addEventListener('load', desenhaFio);

// Peça 3D: chaveiro de mandala com número no verso. Arraste para girar, escolha a cor.
const palco = document.getElementById('palco');
if (palco && window.THREE) {
  const T = THREE, calmo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  fetch('img/chaveiro-3d.json').then(r => r.json()).then(dados => {
    const renderer = new T.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.outputEncoding = T.sRGBEncoding;
    palco.querySelector('img')?.remove();
    palco.prepend(renderer.domElement);

    const cena = new T.Scene();
    const camera = new T.PerspectiveCamera(30, 1, 1, 1000);
    camera.position.set(0, 0, 118);
    cena.add(new T.HemisphereLight(0xfff4dd, 0x201a10, 0.85));
    const sol = new T.DirectionalLight(0xffffff, 0.9); sol.position.set(-40, 60, 90); cena.add(sol);
    const contra = new T.DirectionalLight(0xD3AE41, 0.55); contra.position.set(50, -30, -60); cena.add(contra);

    const linear = hex => new T.Color(hex).convertSRGBToLinear();
    const malha = (m, cor, rugosidade) => {
      const g = new T.BufferGeometry();
      g.setAttribute('position', new T.Float32BufferAttribute(m.p, 3));
      g.setIndex(m.i);
      const plana = g.toNonIndexed(); plana.computeVertexNormals();   // faces planas: arestas vivas como na peça impressa
      return new T.Mesh(plana, new T.MeshStandardMaterial({ color: linear(cor), roughness: rugosidade, metalness: 0.02 }));
    };
    const peca = new T.Group();
    const corpo = malha(dados.corpo, 0xEF6A1C, 0.42);
    const numero = malha(dados.numero, 0x1C1C1E, 0.5);
    peca.add(corpo, numero);
    // argola de metal passando pelo furo da alça
    const argola = new T.Mesh(new T.TorusGeometry(9, 0.6, 16, 96), new T.MeshStandardMaterial({ color: linear(0xcfd2d6), metalness: 0.9, roughness: 0.28 }));
    argola.position.set(dados.alca[0], dados.alca[1] + 9 - dados.furo * 0.4, 2.3);
    argola.rotation.y = Math.PI / 2.6;
    peca.add(argola);
    peca.position.set(0, -6, -2.3);
    const giro = new T.Group(); giro.add(peca); cena.add(giro);
    giro.rotation.x = -0.25;

    let alvoY = 0.5, alvoX = -0.25, arrastando = false, px = 0, py = 0, parado = 0;
    palco.addEventListener('pointerdown', e => { arrastando = true; px = e.clientX; py = e.clientY; palco.setPointerCapture(e.pointerId); });
    palco.addEventListener('pointermove', e => {
      if (!arrastando) return;
      alvoY += (e.clientX - px) * 0.012; alvoX += (e.clientY - py) * 0.008;
      alvoX = Math.max(-1.2, Math.min(1.2, alvoX)); px = e.clientX; py = e.clientY; parado = 0;
    });
    const solta = () => { arrastando = false; };
    palco.addEventListener('pointerup', solta); palco.addEventListener('pointercancel', solta);

    // Frente e verso: gira até o lado escolhido pelo caminho mais curto
    const btFrente = document.getElementById('ver-frente'), btVerso = document.getElementById('ver-verso');
    const lado = verso => {
      const volta = 2 * Math.PI, base = verso ? Math.PI : 0;
      alvoY = base + Math.round((alvoY - base) / volta) * volta; alvoX = -0.15; parado = -400;
      btFrente?.setAttribute('aria-pressed', !verso); btVerso?.setAttribute('aria-pressed', verso);
    };
    btFrente?.addEventListener('click', () => lado(false));
    btVerso?.addEventListener('click', () => lado(true));

    document.querySelectorAll('.escolha button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('.escolha button').forEach(x => x.setAttribute('aria-pressed', x === b));
      corpo.material.color.copy(linear(b.dataset.cor));
      const nome = document.querySelector('.nome-cor'); if (nome) nome.textContent = b.title;
    }));

    function tamanho() {
      const w = palco.clientWidth, h = palco.clientHeight;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    }
    new ResizeObserver(tamanho).observe(palco); tamanho();

    (function quadro() {
      parado++;
      if (!arrastando && !calmo && parado > 120) alvoY += 0.006;   // gira sozinho depois de uns segundos parado
      giro.rotation.y += (alvoY - giro.rotation.y) * 0.12;
      giro.rotation.x += (alvoX - giro.rotation.x) * 0.12;
      renderer.render(cena, camera);
      requestAnimationFrame(quadro);
    })();
  }).catch(() => {});   // sem 3D, fica a foto
}
}

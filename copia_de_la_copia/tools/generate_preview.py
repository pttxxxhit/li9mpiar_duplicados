"""Genera un HTML preview simplificado que muestra cómo quedaría el layout minimal.
No requiere ejecutar la UI — solo muestra visualmente la disposición.
"""
import os
from pathlib import Path

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\"> 
  <title>Eliminar Archivos Duplicados - Preview</title>
  <style>
    :root{ --cyan: #9ed0ff; --btn: #1a73e8; }
    body {{ margin:0; font-family: Arial, Helvetica, sans-serif; background:#000; color:#ddd; }}
    .stack {{ position:relative; width:100vw; height:100vh; overflow:hidden; }}
    /* Fondo menos opaco (se ve más) */
    .bg {{ position:absolute; inset:0; opacity:0.25; background-image: url('{bg_src}'); background-size:cover; filter:brightness(0.45); }}
    .content {{ position:relative; display:flex; height:100%; padding:20px; gap:18px; }}
    .left {{ width:360px; background: rgba(10,10,10,0.12); padding:16px; border-radius:8px; }}
    .right {{ flex:1; background: rgba(20,20,20,0.08); padding:16px; border-radius:8px; overflow:auto; }}
    .btn {{ display:inline-block; padding:8px 12px; border-radius:8px; background:var(--btn); color:#fff; margin-right:8px; text-decoration:none }}
    .transparent-box {{ background: rgba(255,255,255,0.02); padding:10px; border-radius:8px; border:1px solid rgba(255,255,255,0.06) }}
    .cyan-text {{ color: var(--cyan); }}
    .card {{ background: rgba(255,255,255,0.02); padding:10px; border-radius:6px; margin-bottom:10px; }}
    .file {{ color:var(--cyan); font-family: monospace; font-size:12px }}
    .preview {{ display:flex; gap:12px; align-items:center }}
    .preview img {{ max-width:220px; max-height:140px; border:1px solid rgba(255,255,255,0.06); border-radius:6px }}
  </style>
</head>
<body>
  <div class="stack"> 
    <div class="bg"></div>
    <div class="content"> 
      <div class="left"> 
        <h1 class="cyan-text">🗑️ Eliminar Archivos Duplicados</h1>
        <div style="height:8px"></div>
        <div style="display:flex;gap:8px"> 
          <a class="btn" href="#">📁 Seleccionar carpeta</a>
          <a class="btn" href="#">🔍 Buscar duplicados</a>
        </div>
        <div style="height:12px"></div>
        <div class="transparent-box"> <span class="cyan-text">No se ha seleccionado ninguna carpeta</span> </div>
        <div style="height:12px"></div>
        <div class="card">Estado: <span class="cyan-text">listo</span></div>
        <div style="height:12px"></div>
        <div style="display:flex;gap:8px;align-items:center"> 
          <a class="btn" href="#">Seleccionar todos</a>
          <a class="btn" style="background:#555" href="#">Deseleccionar</a>
        </div>
        <div style="height:12px"></div>
        <div class="card"><a class="btn" style="background:#b00020" href="#">🗑️ ELIMINAR TODOS</a></div>

        <div style="height:12px"></div>
        <div class="transparent-box"> 
          <div class="preview"> 
            <img id="pvimg" src="" alt="preview" />
            <div id="pvtxt" class="cyan-text">Ningún archivo seleccionado</div>
          </div>
        </div>
      </div>
      <div class="right" id="list"> 
        <!-- items -->
      </div>
    </div>
  </div>
  <script>
    // Generar items de ejemplo con comportamiento: mostrar preview solo si checkbox está marcado y hover
    const list = document.getElementById('list');
    const pvimg = document.getElementById('pvimg');
    const pvtxt = document.getElementById('pvtxt');
    for(let i=1;i<=12;i++){
      const card = document.createElement('div'); card.className='card';
      const fname = `/ruta/archivo_${i}.jpg`;
      card.innerHTML = `<div style=\\"display:flex;justify-content:space-between;align-items:center\\"><div style=\\"display:flex;align-items:center;gap:10px\\"><input type=\\"checkbox\\" id=\\"chk_${i}\\"/> <span class=\\"file\\">${fname}</span></div><div style=\\"display:flex;gap:8px\\"><button class=\\"btn\\" style=\\"background:#ff5555\\">Eliminar</button></div></div>`;
      list.appendChild(card);
      const chk = card.querySelector('input[type=checkbox]');
      // hover handler: show preview only if checkbox.checked
      card.addEventListener('mouseover', ()=>{
        if(chk.checked){
          pvimg.src = 'assets/fondo.png'; // placeholder image
          pvtxt.textContent = fname;
        }
      });
      card.addEventListener('mouseout', ()=>{
        // clear preview on mouseout
        pvimg.src = '';
        pvtxt.textContent = 'Ningún archivo seleccionado';
      });
    }
  </script>
</body>
</html>
"""


def create_preview(output_path='preview.html', bg_src='assets/fondo.png'):
    p = Path(output_path)
    # Usar replace para evitar que las llaves en el CSS sean interpretadas por str.format
    html = HTML_TEMPLATE.replace('{bg_src}', bg_src)
    # El template usó dobles llaves para escapar; convertir a llaves simples para CSS válido
    html = html.replace('{{', '{').replace('}}', '}')
    p.write_text(html, encoding='utf-8')
    return str(p.resolve())


if __name__ == '__main__':
    print(create_preview())

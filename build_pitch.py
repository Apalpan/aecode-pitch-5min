# -*- coding: utf-8 -*-
"""
AECODE — Pitch Deck 5 minutos · 21 slides (minimalista + storytelling)
Design system OFICIAL AECODE (Manrope · navy #0E1121 · violeta #4A3AC1 · verde #17B14E · azul #4465EE).
Minimalista para pitch presencial · light+dark combinado · logos reales · gráficas · responsive · MODO GUION (tecla N).
Ejecutar:  python build_pitch.py
"""
import html, datetime, pathlib

def esc(s): return html.escape(str(s))

# ---------- helpers ----------
def chip(t): return f'<span class="chip reveal">{t}</span>'
def chiprow(items):
    return '<div class="chiprow reveal">'+''.join(f'<span class="chip2">{esc(i)}</span>' for i in items)+'</div>'
def kicker(t): return f'<div class="kicker reveal">{esc(t)}</div>'
def title(t): return f'<h2 class="s-title reveal">{t}</h2>'
def big(t): return f'<h2 class="big-title reveal">{t}</h2>'
def lead(t): return f'<p class="lead reveal">{t}</p>'
def note(t): return f'<div class="vnote reveal">{t}</div>'
def quote(t): return f'<blockquote class="bigquote reveal">{t}</blockquote>'

def _isnum(v):
    s=str(v).replace(",","").replace(".","").replace("-","")
    return s.isdigit()
def stat(value, label, sub="", suffix="", prefix="", tone="violet"):
    cnt=f'data-count="{value}"' if _isnum(value) else ""
    sub_h=f'<div class="stat-sub">{esc(sub)}</div>' if sub else ""
    return (f'<div class="stat reveal stat-{tone}"><div class="stat-num">'
            f'<span class="stat-pre">{esc(prefix)}</span>'
            f'<span class="stat-val" {cnt}>{esc(value)}</span>'
            f'<span class="stat-suf">{esc(suffix)}</span></div>'
            f'<div class="stat-label">{esc(label)}</div>{sub_h}</div>')
def card(head, body, num="", tag="", tone="violet"):
    num_h=f'<div class="card-num">{esc(num)}</div>' if num else ""
    tag_h=f'<div class="card-tag">{esc(tag)}</div>' if tag else ""
    return (f'<div class="card reveal card-{tone}">{num_h}{tag_h}'
            f'<div class="card-head">{head}</div><div class="card-body">{body}</div></div>')
def bullets(items):
    return '<ul class="bullets">'+"".join(f'<li class="reveal">{b}</li>' for b in items)+'</ul>'
def grid(items, cols=3, extra=""):
    return f'<div class="grid grid-{cols} {extra}">{"".join(items)}</div>'
def eqs(rows):
    out='<div class="eqs reveal">'
    for l,op,r,tone in rows:
        out+=f'<div class="eq eq-{tone}"><span>{l}</span><i>{op}</i><span>{r}</span></div>'
    return out+'</div>'
def flow(steps):
    out='<div class="flow reveal">'
    for i,(t,k) in enumerate(steps):
        out+=f'<div class="flow-step {k}">{t}</div>'
        if i<len(steps)-1: out+='<i class="flow-arr">→</i>'
    return out+'</div>'
def barchart(rows):
    out='<div class="barchart reveal">'
    for r in rows:
        label,pct,disp=r[0],r[1],r[2]; tone=r[3] if len(r)>3 else "violet"
        out+=(f'<div class="bar bar-{tone}"><div class="bar-top"><span>{label}</span>'
              f'<b>{disp}</b></div><div class="bar-track"><i style="--w:{pct:.1f}%"></i></div></div>')
    return out+'</div>'
def stackbar(years, segdefs, maxtotal):
    cols=""
    for label,vals,tot in years:
        total=sum(vals); h=total/maxtotal*100
        segs=""
        for i,v in enumerate(vals):
            ph=(v/total*100) if total else 0
            segs+=f'<span class="sb-seg" style="height:{ph:.2f}%;background:{segdefs[i][1]}"></span>'
        cols+=(f'<div class="sb-col"><div class="sb-bar" style="height:{h:.1f}%">{segs}</div>'
               f'<div class="sb-tot">{tot}</div><div class="sb-lab">{label}</div></div>')
    legend="".join(f'<span class="sb-leg"><i style="background:{c}"></i>{n}</span>' for n,c in segdefs)
    return f'<div class="stackbar reveal"><div class="sb-cols">{cols}</div><div class="sb-legend">{legend}</div></div>'
def tamsamsom(items):
    legend="".join(
        f'<div class="tss-leg reveal"><span class="dot d{i}"></span><div><b>{l}</b> · {v}<small>{d}</small></div></div>'
        for i,(l,v,d) in enumerate(items))
    return f'''<div class="tss reveal"><div class="tss-rings">
        <div class="ring r0"><span>TAM</span></div><div class="ring r1"><span>SAM</span></div>
        <div class="ring r2"><span>SOM</span></div></div>
      <div class="tss-legend">{legend}</div></div>'''
def donut(segs):
    stops=[]; acc=0
    for l,p,c in segs: stops.append(f"{c} {acc}% {acc+p}%"); acc+=p
    grad=",".join(stops)
    legend="".join(f'<div class="dn-leg reveal"><span style="background:{c}"></span><b>{p}%</b> {l}</div>' for l,p,c in segs)
    return f'''<div class="donut-wrap reveal"><div class="donut" style="background:conic-gradient({grad})"><div class="donut-hole"></div></div>
      <div class="donut-legend">{legend}</div></div>'''
def demoframe(inner):
    return (f'<div class="demo-frame reveal"><div class="demo-bar"><span></span><span></span><span></span>'
            f'<span class="demo-url">app.aecode.io / dashboard</span></div>'
            f'<div class="demo-body">{inner}<p class="demo-note">▶ Reemplazar por el video / GIF del flujo real</p></div></div>')

# ---------- slides ----------
SLIDES=[]
def S(theme, chapter, layout, content, notes=""):
    SLIDES.append(dict(theme=theme, chapter=chapter, layout=layout, content=content, notes=notes))

LOGO='<div class="cover-logo reveal"><img class="logo-dark" src="brand/assets/logos/aecode-logo-principal-fondo-oscuro.png" alt="AECODE"><img class="logo-light" src="brand/assets/logos/aecode-logo-principal-fondo-blanco.png" alt="AECODE"></div>'

# 01 HOOK
S("dark","Hook","statement",f"""
  {kicker("01 · Hook")}
  {title('La tecnología avanza <span class="grad">más rápido</span> que nuestra capacidad de adoptarla.')}
  {eqs([("Herramientas","≠","adopción","neq"),("Aprender","≠","aplicar","neq"),("Adopción","=","productividad","eq")])}
""",
"La tecnología avanza más rápido que la capacidad de las personas para adoptarla. Una cosa es conocer una herramienta. Otra cosa es adoptarla en el trabajo real. Y en construcción, esa diferencia impacta directamente en productividad. AECODE nace para cerrar esa brecha.")

# 02 OPORTUNIDAD + PROBLEMA MACRO
S("dark","Oportunidad","statement",f"""
  {kicker("02 · Oportunidad")}
  {title('Construcción mueve el mundo, pero <span class="grad">pierde productividad</span>.')}
  <div class="statrow" style="grid-template-columns:1fr 1fr">
    {stat("280","Personas trabajan en construcción","", suffix="M+")}
    {stat("92","De proyectos con sobrecostos o retrasos","", suffix="%", tone="green")}
  </div>
""",
"La construcción no se detiene. Se seguirán construyendo viviendas, hospitales, carreteras, puentes e infraestructura. Pero hay una paradoja: es una de las industrias más grandes del mundo y, al mismo tiempo, una de las que más sufre por retrasos, sobrecostos y baja productividad. Ahí está la oportunidad: formar mejor al talento que construye.")

# 03 POR QUÉ AHORA
S("dark","Por qué ahora","statement",f"""
  {kicker("03 · Por qué ahora")}
  {quote('Adoptar tecnología <span class="grad">ya no es opcional</span>.')}
  {flow([("Digitalización BIM",""),("Automatización",""),("IA aplicada","hot"),("Productividad","win")])}
  {chip("44% de las habilidades cambiarán en los próximos 5 años")}
""",
"La construcción está entrando a una etapa donde la digitalización BIM, la automatización y la IA ya no son innovación lejana. Empiezan a ser condiciones para competir. El reto ya no es solo tener herramientas. Es que los equipos sepan usarlas para coordinar mejor, ahorrar tiempo y reducir errores.")

# 04 PROBLEMA CENTRAL
S("light","Problema central","statement",f"""
  {kicker("04 · Problema central")}
  {title('No falta contenido.<br>Falta una <span class="grad">ruta clara</span> para aplicar.')}
  {chiprow(["Cursos infinitos","Poca claridad","Poca práctica","Baja adopción"])}
""",
"Hoy no faltan cursos, tutoriales, webinars, comunidades ni respuestas con IA. El problema es que el aprendizaje está fragmentado. El profesional no sabe qué aprender primero, qué realmente le sirve para crecer o cómo aplicarlo en su trabajo. Y la empresa capacita, pero no siempre logra que esa capacitación cambie la forma de trabajar.")

# 05 DOLOR REAL
S("light","Dolor real","cards",f"""
  {kicker("05 · Dolor real")}
  {title('Cuando el aprendizaje no se aplica, <span class="grad">todos pagan</span> el costo.')}
  {grid([
    card("Profesional","Aprende, pero no demuestra mejora.", num="01"),
    card("Empresa","Capacita, pero no logra adopción.", num="02", tone="green"),
    card("Proyecto","Errores, retrabajo y baja productividad.", num="03", tone="blue"),
  ],3)}
""",
"El dolor se ve en tres niveles. Para el profesional: invierte tiempo y dinero, pero no siempre mejora su trabajo, salario o empleabilidad. Para la empresa: invierte en capacitación y tecnología, pero no siempre cambia el comportamiento del equipo. Y para el proyecto: esa brecha se convierte en errores, retrabajo, baja coordinación y pérdida de productividad.")

# 06 SOLUCIÓN
S("dark","Solución","statement",f"""
  {kicker("06 · Solución")}
  {title('AECODE acelera la <span class="grad">adopción tecnológica</span> en construcción.')}
  {flow([("Aprende tecnología",""),("Aplícala en proyectos reales","hot"),("Construye mejor","win")])}
""",
"AECODE es una plataforma de aprendizaje para arquitectura, ingeniería y construcción. Ayudamos a profesionales y empresas a aprender y aplicar digitalización BIM, automatización, IA y herramientas digitales en el trabajo real. No vendemos solo cursos. Convertimos aprendizaje en adopción tecnológica.")

# 07 PRODUCTO / VIDEO DEMO
S("light","Producto / Video Demo","demo",f"""
  {kicker("07 · Producto / Video Demo")}
  {title('Rutas prácticas <span class="grad">por rol</span>')}
  {demoframe(flow([("Diagnóstico",""),("Ruta",""),("Microlearning",""),("Práctica","hot"),("Evidencia","hot"),("Progreso","win")]))}
""",
"El usuario identifica su nivel, elige un rol o especialidad y avanza por una ruta práctica. Puede aprender BIM, planificación, costos, coordinación, gestión de obra, automatización o IA aplicada. Aprende con cápsulas cortas, practica con casos reales y genera evidencia de avance.")

# 08 INNOVACIÓN TECNOLÓGICA
S("dark","Innovación tecnológica","statement",f"""
  {kicker("08 · Innovación tecnológica")}
  {title('AI Coach entrenado con <span class="grad">criterio experto AEC</span>')}
  {chiprow(["+200 expertos","Diagnóstico adaptativo","Rutas personalizadas","Sistema multiagente"])}
  {chip("No es un chatbot encima de cursos: es un motor de IA adaptativa")}
""",
"Nuestra innovación no es poner un chatbot encima de una plataforma. Estamos construyendo un motor de IA adaptativa alimentado por contenido validado y criterio de más de 200 expertos del sector. El sistema diagnostica, recomienda rutas, entiende la necesidad del usuario y lo guía con un enfoque multiagente hacia habilidades aplicables.")

# 09 MERCADO
S("light","Mercado","tss",f"""
  {kicker("09 · Mercado")}
  {title('Formación digital para <span class="grad">construcción en LATAM</span>')}
  {tamsamsom([("TAM","US$360 M","Formación digital AEC LATAM"),("SAM","US$87.5 M","Mercado servible"),("SOM 3 años","US$2.5 M","Meta · menos del 3% del SAM")])}
""",
"Nuestro mercado inicial es la formación digital especializada para construcción en Latinoamérica. Estimamos un TAM de 360 millones de dólares, un SAM de 87.5 millones y una meta de capturar 2.5 millones en tres años. Es menos del 3% del mercado servible.")

# 10 MODELO B2C2B
S("dark","Modelo B2C2B","statement",f"""
  {kicker("10 · Modelo B2C2B")}
  {quote('Profesional adopta.<br>Empresa escala.<br><span class="grad">Proyecto mejora.</span>')}
  {flow([("B2C","hot"),("Equipos",""),("B2B","hot"),("B2C2B","win")])}
""",
"Nuestro modelo empieza con el profesional. Construimos comunidad, confianza y adopción con personas que ya quieren mejorar su trabajo. Cuando esos profesionales aplican lo aprendido, la empresa ve valor y puede escalarlo a equipos completos. Así pasamos de adquisición individual a expansión empresarial.")

# 11 MODELO DE NEGOCIO
S("dark","Modelo de negocio","statement",f"""
  {kicker("11 · Modelo de negocio")}
  {quote('<span class="grad">Live valida.<br>B2B ancla.<br>On-demand AI escala.</span>')}
  {chiprow(["Live Training: caja + comunidad","B2B: ticket alto + recurrencia","On-demand AI: margen + escala"])}
""",
"Tenemos tres motores. Live Training genera caja, comunidad y validación. B2B aporta contratos de mayor valor y expansión por cuenta. On-demand AI convierte el conocimiento validado en rutas digitales escalables, con mayor margen y menor costo marginal.")

# 12 TRACCIÓN
S("light","Tracción","chart",f"""
  {kicker("12 · Tracción")}
  {title('El mercado <span class="grad">ya paga</span> por esta necesidad')}
  {barchart([("2024 · validación",13.6,"US$30K","ink"),("2025 · ×4 crecimiento",54.5,"US$120K","violet"),("2026E · expansión",100,"US$220K","green")])}
""",
"En 2024 vendimos 30 mil dólares. En 2025 crecimos a 120 mil dólares, cuatro veces más. Para 2026 proyectamos 220 mil dólares. La tracción muestra que el mercado ya paga por esta necesidad.")

# 13 COMUNIDAD Y VALIDACIÓN
S("dark","Comunidad y validación","chart",f"""
  {kicker("13 · Comunidad y validación")}
  {title('No partimos <span class="grad">desde cero</span>')}
  <div class="statrow">
    {stat("95","Comunidad","8k WhatsApp activo", suffix="K+", tone="blue")}
    {stat("14","Países","alcance regional", tone="violet")}
    {stat("200","Expertos conectados","ecosistema AEC", suffix="+", tone="green")}
    {stat("12","Clientes B2B","tracción enterprise", suffix="+", tone="violet")}
  </div>
  {chiprow(["+100 alianzas","15% ventas internacionales"])}
""",
"No partimos desde cero. Tenemos una comunidad de más de 95 mil profesionales, presencia en 14 países, más de 100 alianzas y más de 200 expertos conectados al ecosistema. Además, ya tenemos más de 12 clientes B2B y 15% de ventas internacionales.")

# 14 GO TO MARKET
S("light","Go To Market","statement",f"""
  {kicker("14 · Go To Market")}
  {title('El B2C da entrada. El <span class="grad">B2B da expansión</span>.')}
  {flow([("Comunidad","hot"),("Diagnóstico",""),("Live",""),("On-demand",""),("B2B","win")])}
  {chiprow(["CAC bajo","NPS alto","Expansión por cuenta"])}
""",
"Nuestro go-to-market parte de comunidad y contenido especializado. Atraemos profesionales, los llevamos a diagnóstico, activamos con programas live, convertimos lo validado en microlearning y escalamos hacia empresas. El B2C nos da entrada. El B2B nos da expansión.")

# 15 NSM
S("light","NSM","statement",f"""
  {kicker("15 · NSM")}
  {title('Medimos <span class="grad">adopción real</span>')}
  {chiprow(["Producto: prácticas aplicadas / mes","Negocio: % revenue B2B + On-demand AI"])}
""",
"Medimos dos cosas. En producto, no queremos solo usuarios viendo videos. Queremos prácticas aplicadas completadas. En negocio, queremos que cada vez más revenue venga de B2B y On-demand AI, porque ahí está la escalabilidad.")

# 16 DIFERENCIACIÓN
S("dark","Diferenciación","statement",f"""
  {kicker("16 · Diferenciación")}
  {quote('No competimos por más cursos.<br>Competimos por <span class="grad">adopción tecnológica</span>.')}
  {chiprow(["Vertical AEC","Rutas por rol","IA sectorial","+200 expertos","Comunidad"])}
""",
"Las plataformas horizontales venden contenido. AECODE compite desde la profundidad vertical. Tenemos comunidad AEC, expertos, rutas por rol, prácticas aplicadas, IA sectorial y un modelo que conecta aprendizaje con productividad.")

# 17 ROADMAP
S("light","Roadmap","timeline",f"""
  {kicker("17 · Roadmap")}
  {title('De operación validada a <span class="grad">plataforma regional</span>')}
  <div class="tl reveal">
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2024</div><div class="tl-what"><b>Live</b> + comunidad.</div></div>
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2025</div><div class="tl-what">Primer <b>B2B</b> + ×4 crecimiento.</div></div>
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2026</div><div class="tl-what"><b>Microlearning + IA</b>.</div></div>
    <div class="tl-item win"><div class="tl-dot"></div><div class="tl-when">2027</div><div class="tl-what"><b>LATAM</b> + AI Talent.</div></div>
  </div>
""",
"En 2024 validamos comunidad y programas en vivo. En 2025 hicimos nuestro primer piloto B2B y crecimos cuatro veces. En 2026 lanzamos microlearning e IA aplicada, empezando con programas como IA para ingeniería civil. En 2027 buscamos expansión regional, apoyados en eventos, alianzas y programas como AI Talent.")

# 18 ESCALABILIDAD
S("light","Escalabilidad","chart",f"""
  {kicker("18 · Escalabilidad")}
  {title('Mismo conocimiento. Más usuarios. <span class="grad">Menor costo marginal.</span>')}
  {stackbar([("2024",[30,0,0],"100% Live"),("2026E",[132,55,33],"40% escalable"),("2027 Target",[160,140,120],"62% escalable")],
            [("B2C Live","#4465EE"),("B2B","#17B14E"),("On-demand AI","#6D70F9")], 420)}
""",
"La clave es cambiar el mix. Hoy Live valida y genera caja. Pero cada programa validado se convierte en cápsulas, rutas, prácticas y activos digitales reutilizables. Así crece el margen, la recurrencia y la capacidad de escalar sin depender solo de horas humanas.")

# 19 EQUIPO
S("dark","Equipo","statement",f"""
  {kicker("19 · Equipo")}
  {title('Equipo completo para <span class="grad">construir, vender y escalar</span>')}
  {stat("12","Personas · equipo multidisciplinario","", suffix="+", tone="green")}
  {chiprow(["Producto","Tech","IA","Comercial","Growth","Académico","Finanzas"])}
""",
"Tenemos un equipo multidisciplinario de más de 12 personas. Cubrimos producto, desarrollo, sistemas, data, IA, comercial, growth, coordinación académica, administración y finanzas. No es un equipo que recién va a validar. Es el equipo que ya construyó comunidad, vendió y creció.")

# 20 ASK
S("dark","Ask","ask",f"""
  {kicker("20 · Ask")}
  {title('US$125K para <span class="grad">escalar lo validado</span>')}
  <div class="ask-grid reveal">
    <div class="ask-left">{donut([("IA + plataforma",60,"#6D70F9"),("Growth B2C2B / LATAM",30,"#17B14E"),("Microlearning",10,"#4465EE")])}</div>
    <div class="ask-right">{bullets(["<b>60%</b> — IA + plataforma","<b>30%</b> — growth B2C2B / LATAM","<b>10%</b> — microlearning"])}</div>
  </div>
""",
"Buscamos 125 mil dólares. El 60% irá a IA y plataforma. El 30% a growth B2C2B y expansión LATAM. El 10% a producción de microlearning. El capital no financia una idea. Financia la conversión de una operación validada en una plataforma escalable.")

# 21 CIERRE
S("dark","Cierre","close",f"""
  {LOGO}
  <div class="close-cta reveal">Aprende · Aplica · <span class="grad">Construye mejor</span></div>
  <div class="close-mail reveal">apalpan@genplusdesign.com · AECODE</div>
""",
"La construcción no se transforma solo con más herramientas ni más cursos. Se transforma cuando su gente aprende a aplicar tecnología en el trabajo real. AECODE existe para acelerar esa adopción tecnológica en construcción. Aprende, aplica, construye mejor.")

# ---------- render ----------
def render_slide(i,s):
    return (f'<section class="slide" data-base="{s["theme"]}" data-ch="{esc(s["chapter"])}" data-notes="{esc(s["notes"])}" data-idx="{i}">'
            f'<div class="slide-inner layout-{s["layout"]}">{s["content"]}</div>'
            f'<img class="slide-mark" src="brand/assets/logos/aecode_isotipo_principal.png" alt="">'
            f'<div class="slide-foot"><span class="foot-ch">{esc(s["chapter"])}</span>'
            f'<span class="foot-n">{i+1:02d}<i>/</i>{len(SLIDES):02d}</span></div></section>')
slides_html="\n".join(render_slide(i,s) for i,s in enumerate(SLIDES))
total=len(SLIDES)
toc_items="".join(
   f'<button class="toc-item" data-go="{i}"><span class="toc-n">{i+1:02d}</span>'
   f'<span class="toc-t">{esc(s["chapter"])}</span></button>' for i,s in enumerate(SLIDES))

CSS = r"""
:root{
  --violet:#4A3AC1; --blue:#4465EE; --violet2:#6D70F9; --green:#17B14E; --lavender:#A6A7FF;
  --ease:cubic-bezier(.22,.61,.36,1); --ease-out:cubic-bezier(.16,1,.3,1);
}
.is-light{
  --bg:#F5F5F6; --bg2:#EDEBF9; --surface:#FFFFFF; --fg:#202231; --muted:#3A4065;
  --line:#C7C2EC; --card:#FFFFFF; --card-line:#E3E0F5;
  --accent:#4A3AC1; --accent2:#4465EE; --accent3:#17B14E; --ink-soft:#4A3AC1;
  --grad:linear-gradient(100deg,#4465EE,#6D12E3);
  --grad3:linear-gradient(100deg,#17B14E,#4A3AC1);
  --mesh-a:rgba(74,58,193,.10); --mesh-b:rgba(23,177,78,.10); --chip-bg:#EDEBF9;
}
.is-dark{
  --bg:#0E1121; --bg2:#1B1E3C; --surface:#13172F; --fg:#EEF3F8; --muted:#A2B4CB;
  --line:rgba(124,126,223,.24); --card:rgba(27,30,60,.72); --card-line:rgba(124,126,223,.32);
  --accent:#A6A7FF; --accent2:#7E97FF; --accent3:#2FD06E; --ink-soft:#C9D0F5;
  --grad:linear-gradient(100deg,#7E97FF,#9A5CFF);
  --grad3:linear-gradient(100deg,#2FD06E,#8C97DC);
  --mesh-a:rgba(74,58,193,.46); --mesh-b:rgba(23,177,78,.20); --chip-bg:rgba(124,126,223,.16);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:#05060f;color:#fff;overflow:hidden;font-family:Manrope,"Plus Jakarta Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.deck{position:fixed;inset:0;display:grid;place-items:center}
.stage{width:1280px;height:720px;position:relative;transform-origin:center}
.slide{position:absolute;inset:0;display:grid;place-items:center;background:var(--bg);color:var(--fg);
  opacity:0;visibility:hidden;pointer-events:none;transition:opacity .5s var(--ease),transform .55s var(--ease-out);overflow:hidden}
.slide::before{content:"";position:absolute;inset:-12%;z-index:0;
  background:radial-gradient(38% 50% at 14% 12%,var(--mesh-a),transparent 70%),radial-gradient(44% 52% at 88% 90%,var(--mesh-b),transparent 72%)}
.slide.active{opacity:1;visibility:visible;pointer-events:auto}
.slide-inner{position:relative;z-index:2;width:100%;height:100%;padding:58px 72px 66px;display:flex;flex-direction:column;justify-content:center;gap:20px}
.slide-foot{position:absolute;z-index:3;left:72px;right:72px;bottom:24px;display:flex;justify-content:space-between;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.foot-ch{font-weight:700} .foot-n{font-variant-numeric:tabular-nums;font-weight:700} .foot-n i{opacity:.4;font-style:normal;margin:0 3px}
.reveal{opacity:0;transform:translateY(16px);transition:opacity .55s var(--ease-out),transform .55s var(--ease-out)}
.slide.active .reveal{opacity:1;transform:none}
.kicker{font-weight:800;font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:11px}
.kicker::before{content:"";width:30px;height:3px;border-radius:3px;background:var(--grad)}
.s-title{font-weight:800;font-size:clamp(32px,4.4vw,56px);line-height:1.02;letter-spacing:-.025em;text-wrap:balance;max-width:20ch}
.lead{font-size:clamp(16px,1.5vw,21px);line-height:1.5;color:var(--muted);max-width:64ch}
.lead b{color:var(--fg);font-weight:700} .lead i{font-style:italic;color:var(--accent)}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
.chip{display:inline-flex;align-items:center;gap:9px;align-self:flex-start;font-size:14px;font-weight:700;padding:9px 17px;border-radius:100px;border:1px solid var(--card-line);background:var(--chip-bg);color:var(--fg)}
.chip::before{content:"◆";color:var(--accent3);font-size:10px}
.chiprow{display:flex;gap:10px;flex-wrap:wrap}
.chip2{font-weight:700;font-size:15px;padding:10px 17px;border-radius:100px;background:var(--chip-bg);border:1px solid var(--card-line);color:var(--fg)}
.vnote{font-size:13.5px;line-height:1.45;color:var(--muted);padding:12px 16px;border-radius:12px;background:var(--bg2);border:1px dashed var(--card-line)}
.vnote b{color:var(--accent)}
/* cover/close */
.layout-cover,.layout-close{align-items:flex-start;justify-content:center;gap:20px}
.cover-logo img{height:54px;width:auto;display:block}
.logo-light{display:none}.slide.is-light .logo-light{display:block} .slide.is-light .logo-dark{display:none}
.slide-mark{position:absolute;top:30px;right:34px;height:30px;width:auto;z-index:3;opacity:.92;pointer-events:none}
.layout-close .slide-mark{display:none}
.close-cta{font-weight:800;font-size:clamp(22px,2.6vw,34px);color:var(--fg);letter-spacing:.02em}
.close-cta::before{content:"";display:inline-block;width:30px;height:3px;background:var(--grad);border-radius:3px;vertical-align:middle;margin-right:14px}
.close-mail{font-weight:700;font-size:15px;color:var(--muted);margin-top:4px}
/* statement */
.layout-statement{gap:26px}
.bigquote{font-weight:800;line-height:1.12;letter-spacing:-.025em;font-size:clamp(30px,4.2vw,54px);text-wrap:balance;max-width:24ch;border-left:4px solid var(--accent3);padding-left:28px}
.big-title{font-weight:800;font-size:clamp(34px,5vw,62px);line-height:1.03;letter-spacing:-.03em;text-wrap:balance;max-width:20ch}
/* eqs */
.eqs{display:flex;flex-direction:column;gap:13px}
.eq{display:flex;align-items:center;gap:16px;font-weight:800;font-size:clamp(20px,2.6vw,32px)}
.eq span{color:var(--fg)} .eq i{font-style:normal;font-weight:800;font-size:1.05em}
.eq-neq i{color:var(--muted)} .eq-eq i{color:var(--accent3)} .eq-eq span:last-child{color:var(--accent3)}
/* split */
.split{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center;margin-top:2px}
.split-l,.split-r{display:flex;flex-direction:column;gap:14px}
/* stat */
.statrow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat{display:flex;flex-direction:column;gap:3px;padding:18px 20px;border-radius:16px;background:var(--card);border:1px solid var(--card-line)}
.stat-num{font-weight:800;line-height:1;font-size:clamp(34px,4.4vw,56px);letter-spacing:-.02em;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:1px;color:var(--accent)}
.stat-green .stat-num{color:var(--accent3)} .stat-blue .stat-num{color:var(--accent2)}
.stat-pre,.stat-suf{font-size:.5em;font-weight:700}
.stat-label{font-size:15px;font-weight:700;color:var(--fg);line-height:1.25}
.stat-sub{font-size:13px;color:var(--muted);line-height:1.3}
.statrow[style] .stat-num{font-size:clamp(40px,5.4vw,68px)}
/* cards */
.grid{display:grid;gap:14px}
.grid-1{grid-template-columns:1fr}.grid-2{grid-template-columns:repeat(2,1fr)}.grid-3{grid-template-columns:repeat(3,1fr)}
.card{position:relative;padding:20px 20px 18px;border-radius:16px;background:var(--card);border:1px solid var(--card-line);display:flex;flex-direction:column;gap:8px;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;width:100%;height:3px;background:var(--accent)}
.card-green::before{background:var(--accent3)} .card-blue::before{background:var(--accent2)}
.card-num{font-weight:800;font-size:22px;color:var(--accent)}
.card-tag{font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.card-green .card-tag,.card-green .card-num{color:var(--accent3)} .card-blue .card-tag,.card-blue .card-num{color:var(--accent2)}
.card-head{font-weight:800;font-size:19px;line-height:1.2;color:var(--fg)}
.card-body{font-size:15px;line-height:1.45;color:var(--muted)} .card-body b{color:var(--fg)}
.cards-sm .card-head{font-size:16.5px} .cards-sm .card-body{font-size:13.5px}
/* bullets */
.bullets{list-style:none;display:flex;flex-direction:column;gap:9px}
.bullets li{position:relative;padding-left:22px;font-size:15.5px;line-height:1.4;color:var(--muted)}
.bullets li b{color:var(--fg);font-weight:700}
.bullets li::before{content:"";position:absolute;left:2px;top:7px;width:8px;height:8px;border-radius:2px;background:var(--accent3);transform:rotate(45deg)}
/* flow */
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:9px}
.flow-step{font-weight:700;font-size:16px;padding:12px 18px;border-radius:12px;background:var(--card);border:1px solid var(--card-line);color:var(--fg)}
.flow-step.hot{border-color:var(--accent2);color:var(--accent2);box-shadow:0 0 22px rgba(68,101,238,.18)}
.flow-step.win{background:var(--grad3);color:#fff;border:none}
.flow-arr{color:var(--accent);font-weight:800;font-size:18px;font-style:normal}
/* barchart */
.barchart{display:flex;flex-direction:column;gap:13px;width:100%}
.bar-top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;font-size:14.5px}
.bar-top span{color:var(--fg);font-weight:600} .bar-top b{color:var(--accent);font-weight:800;font-variant-numeric:tabular-nums}
.bar-track{height:12px;border-radius:100px;background:var(--bg2);overflow:hidden;border:1px solid var(--card-line)}
.bar-track i{display:block;height:100%;width:var(--w);border-radius:100px;background:var(--grad);transform:scaleX(0);transform-origin:left;transition:transform .9s var(--ease-out)}
.slide.active .bar-track i{transform:scaleX(1)}
.bar-green .bar-top b{color:var(--accent3)} .bar-green .bar-track i{background:linear-gradient(100deg,var(--green),#43d98f)}
.bar-blue .bar-top b{color:var(--accent2)} .bar-blue .bar-track i{background:linear-gradient(100deg,var(--blue),#6f8cff)}
.bar-ink .bar-top b{color:var(--muted)} .bar-ink .bar-track i{background:var(--muted);opacity:.7}
/* stackbar */
.stackbar{display:flex;flex-direction:column;gap:16px;width:100%}
.sb-cols{display:flex;align-items:flex-end;justify-content:space-around;gap:26px;height:236px;padding:0 6px;border-bottom:2px solid var(--card-line)}
.sb-col{flex:1;max-width:130px;display:flex;flex-direction:column;align-items:center;gap:7px;height:100%;justify-content:flex-end}
.sb-bar{width:66px;border-radius:8px 8px 0 0;overflow:hidden;display:flex;flex-direction:column-reverse;transform:scaleY(0);transform-origin:bottom;transition:transform .85s var(--ease-out)}
.slide.active .sb-bar{transform:scaleY(1)}
.sb-seg{width:100%;display:block} .sb-tot{font-weight:800;font-size:15px;color:var(--fg)} .sb-lab{font-size:12.5px;font-weight:700;color:var(--muted)}
.sb-legend{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.sb-leg{display:flex;align-items:center;gap:7px;font-size:13.5px;color:var(--muted);font-weight:600} .sb-leg i{width:13px;height:13px;border-radius:4px}
/* tss */
.tss{display:flex;gap:26px;align-items:center}
.tss-rings{position:relative;width:230px;height:230px;flex:none}
.ring{position:absolute;border-radius:50%;display:grid;place-items:start center;padding-top:10px;font-weight:800;font-size:13px;left:50%;top:50%;transform:translate(-50%,-50%)}
.ring span{color:#fff;letter-spacing:.1em}
.ring.r0{width:230px;height:230px;background:rgba(74,58,193,.20);border:1px solid var(--violet)}
.ring.r1{width:158px;height:158px;background:rgba(68,101,238,.28);border:1px solid var(--blue)}
.ring.r2{width:88px;height:88px;background:var(--green);border:1px solid var(--green);place-items:center;padding:0}
.is-light .ring.r0 span,.is-light .ring.r1 span{color:#2a2470}
.tss-legend{display:flex;flex-direction:column;gap:12px}
.tss-leg{display:flex;gap:11px;align-items:flex-start;font-size:14px}
.tss-leg .dot{width:14px;height:14px;border-radius:4px;margin-top:3px;flex:none}
.tss-leg .d0{background:var(--violet)} .tss-leg .d1{background:var(--blue)} .tss-leg .d2{background:var(--green)}
.tss-leg b{color:var(--fg);font-weight:800} .tss-leg small{display:block;color:var(--muted);font-size:12.5px}
/* donut */
.donut-wrap{display:flex;align-items:center;gap:24px}
.donut{width:184px;height:184px;border-radius:50%;position:relative;flex:none}
.donut-hole{position:absolute;inset:30px;border-radius:50%;background:var(--bg)}
.donut-legend{display:flex;flex-direction:column;gap:11px}
.dn-leg{display:flex;align-items:center;gap:9px;font-size:14.5px;color:var(--muted)} .dn-leg span{width:13px;height:13px;border-radius:4px;flex:none} .dn-leg b{color:var(--fg);font-weight:800}
/* demo */
.layout-demo{gap:16px}
.demo-frame{border-radius:16px;overflow:hidden;border:1px solid var(--card-line);background:var(--bg2);box-shadow:0 26px 60px rgba(0,0,0,.32)}
.demo-bar{display:flex;align-items:center;gap:7px;padding:11px 16px;background:var(--card);border-bottom:1px solid var(--card-line)}
.demo-bar>span{width:11px;height:11px;border-radius:50%;background:var(--line)}
.demo-url{margin-left:14px;font-size:13px;color:var(--muted);background:var(--bg);padding:5px 14px;border-radius:6px;flex:1;max-width:280px}
.demo-body{padding:26px 22px;display:flex;flex-direction:column;gap:14px;align-items:center}
.demo-note{font-size:13.5px;color:var(--muted);font-style:italic}
/* timeline */
.tl{display:grid;grid-template-columns:repeat(4,1fr);position:relative;margin:14px 0}
.tl::before{content:"";position:absolute;left:6%;right:6%;top:9px;height:2px;background:var(--line)}
.tl-item{position:relative;padding:0 13px;display:flex;flex-direction:column;gap:8px}
.tl-dot{width:18px;height:18px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 5px var(--bg),0 0 18px rgba(74,58,193,.4);z-index:2}
.tl-item.win .tl-dot{background:var(--accent3);box-shadow:0 0 0 5px var(--bg),0 0 18px rgba(38,185,111,.45)}
.tl-when{font-weight:800;font-size:18px;color:var(--accent)} .tl-item.win .tl-when{color:var(--accent3)}
.tl-what{font-size:14.5px;line-height:1.4;color:var(--muted)} .tl-what b{color:var(--fg)}
/* ask */
.layout-ask{gap:16px}
.ask-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:34px;align-items:center;margin-top:4px}
.ask-left{display:flex;justify-content:center}.ask-right{display:flex;flex-direction:column;gap:14px}
/* chrome */
.chrome{position:fixed;inset:0;z-index:50;pointer-events:none}
.ctrl{position:absolute;bottom:20px;right:24px;display:flex;gap:8px;pointer-events:auto}
.ctrl button{width:39px;height:39px;border-radius:11px;border:1px solid rgba(255,255,255,.16);background:rgba(20,26,61,.62);color:#fff;backdrop-filter:blur(10px);cursor:pointer;font-size:15px;display:grid;place-items:center;transition:transform .15s,background .2s}
.ctrl button:hover{background:rgba(74,58,193,.7)} .ctrl button:active{transform:scale(.92)}
.ctrl button:focus-visible{outline:2px solid var(--green);outline-offset:2px}
.counter{position:absolute;bottom:28px;left:24px;font-weight:700;font-size:13px;letter-spacing:.1em;color:#fff;opacity:.6;font-variant-numeric:tabular-nums;background:rgba(20,26,61,.5);padding:7px 13px;border-radius:9px;backdrop-filter:blur(8px)}
.arrow-zone{position:fixed;top:0;bottom:0;width:13%;z-index:40;cursor:pointer}
.arrow-zone.left{left:0}.arrow-zone.right{right:0}
/* notas / guion */
.notes{position:fixed;left:0;right:0;bottom:0;z-index:55;background:rgba(10,12,30,.97);backdrop-filter:blur(14px);border-top:2px solid rgba(124,126,223,.45);padding:18px 30px 24px;transform:translateY(101%);transition:transform .35s var(--ease);pointer-events:auto;max-height:44vh;overflow:auto}
.notes.open{transform:none}
.notes-h{font-weight:800;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#A6A7FF;margin-bottom:9px;display:flex;justify-content:space-between;align-items:center}
.notes-h span{color:#8C97DC}
.notes p{font-size:clamp(15px,1.5vw,18px);line-height:1.6;color:#e7eaff;max-width:96ch}
/* toc */
.toc{position:fixed;inset:0;z-index:60;background:rgba(8,10,28,.96);backdrop-filter:blur(14px);padding:54px 64px;overflow:auto;display:none}
.toc.open{display:block}
.toc h3{font-weight:800;font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:#8b7df0;margin-bottom:22px}
.toc-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:9px}
.toc-item{display:flex;flex-direction:column;gap:4px;padding:12px 14px;border-radius:11px;background:rgba(30,37,78,.7);border:1px solid rgba(255,255,255,.08);color:#fff;cursor:pointer;text-align:left;transition:transform .15s,border-color .2s}
.toc-item:hover{transform:translateY(-3px);border-color:#43d98f}
.toc-n{font-weight:800;font-size:16px;color:#43d98f} .toc-t{font-size:12px;color:#a9b2da;line-height:1.25}
.toc-close{position:absolute;top:26px;right:36px;font-size:22px;background:none;border:none;color:#fff;cursor:pointer}
/* interactividad */
.card,.stat{transition:transform .2s var(--ease),box-shadow .25s,border-color .25s}
.slide.active .card:hover,.slide.active .stat:hover{transform:translateY(-4px);border-color:var(--accent);box-shadow:0 16px 34px rgba(8,10,30,.22)}
.flow-step{transition:transform .18s var(--ease),border-color .2s}
.slide.active .flow-step:hover{transform:translateY(-2px);border-color:var(--accent2)}
.segbar{position:absolute;top:0;left:0;right:0;height:6px;display:flex;gap:2px;pointer-events:auto}
.seg{flex:var(--c) 1 0;height:5px;align-self:flex-start;background:rgba(140,151,220,.24);position:relative;cursor:pointer;transition:height .2s,background .25s}
.seg:hover,.seg.cur{height:8px;background:rgba(140,151,220,.4)}
.seg i{position:absolute;left:0;top:0;height:100%;width:var(--f,0%);background:linear-gradient(90deg,#4465EE,#17B14E);transition:width .45s var(--ease)}
.seg .lab{position:absolute;top:12px;left:0;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#e7eaff;background:rgba(14,17,33,.94);border:1px solid rgba(124,126,223,.4);padding:4px 9px;border-radius:7px;white-space:nowrap;opacity:0;transform:translateY(-4px);transition:opacity .2s,transform .2s;pointer-events:none;z-index:6}
.seg:hover .lab{opacity:1;transform:none}
#btn-play.playing,#btn-notes.on{background:rgba(74,58,193,.85);color:#fff;box-shadow:0 0 18px rgba(124,126,223,.6)}
/* responsive móvil */
body.mobile .deck{place-items:stretch}
body.mobile .stage{width:100vw;height:100dvh;transform:none!important}
body.mobile .slide{display:block;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch}
body.mobile .slide-inner{position:static;height:auto;min-height:100%;justify-content:flex-start;padding:56px clamp(18px,5.5vw,30px) 82px;gap:clamp(14px,3.6vw,20px)}
body.mobile .slide-foot{left:clamp(18px,5.5vw,30px);right:clamp(18px,5.5vw,30px);bottom:18px}
body.mobile .slide-mark{top:18px;right:18px;height:24px}
body.mobile .split,body.mobile .ask-grid,body.mobile .statrow,body.mobile .grid-2,body.mobile .grid-3,body.mobile .tss,body.mobile .donut-wrap{display:flex;flex-direction:column;gap:13px}
body.mobile .statrow[style]{display:grid;grid-template-columns:1fr 1fr!important}
body.mobile .s-title{font-size:clamp(25px,7vw,36px);max-width:none}
body.mobile .big-title,body.mobile .bigquote{font-size:clamp(26px,7.2vw,40px);max-width:none}
body.mobile .lead{font-size:clamp(15px,4vw,18px);max-width:none}
body.mobile .eq{font-size:clamp(18px,5vw,26px)}
body.mobile .tss-rings{margin:0 auto}
body.mobile .stackbar{overflow-x:auto} body.mobile .sb-cols{gap:14px;height:200px} body.mobile .sb-bar{width:48px}
body.mobile .ctrl{bottom:14px;right:11px;gap:7px} body.mobile .ctrl button{width:42px;height:42px}
body.mobile .counter{bottom:18px;left:11px} body.mobile .arrow-zone{display:none}
body.mobile .donut{width:154px;height:154px} body.mobile .donut-hole{inset:26px}
body.mobile .toc{padding:48px 22px} body.mobile .toc-grid{grid-template-columns:repeat(2,1fr)}
body.mobile .notes{max-height:55vh}
@media (prefers-reduced-motion:reduce){
  .reveal{transition:none!important;opacity:1!important;transform:none!important}
  .slide{transition:opacity .2s!important}
  .bar-track i,.sb-bar,.seg i{transition:none!important}
  .slide.active .bar-track i{transform:scaleX(1)} .slide.active .sb-bar{transform:scaleY(1)}
}
"""

JS = r"""
const slides=[...document.querySelectorAll('.slide')];const total=slides.length;let cur=0;
const stage=document.querySelector('.stage'),counter=document.querySelector('.counter'),segbar=document.querySelector('#segbar');
const notes=document.querySelector('#notes'),notesBody=document.querySelector('#notes-body'),notesN=document.querySelector('#notes-n');
let mode=localStorage.getItem('aecode-pitch-mode')||'mix';
const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
const chapters=[];
slides.forEach((s,i)=>{const c=s.dataset.ch,last=chapters[chapters.length-1];
  if(last&&last.name===c){last.count++}else{chapters.push({name:c,start:i,count:1})}});
chapters.forEach(ch=>{const seg=document.createElement('div');seg.className='seg';seg.style.setProperty('--c',ch.count);
  seg.innerHTML='<i></i><span class="lab">'+ch.name+'</span>';seg.title=ch.name;
  seg.onclick=()=>{stopPlay();go(ch.start)};segbar.appendChild(seg);ch.el=seg;ch.fill=seg.querySelector('i');});
function updateSeg(){chapters.forEach(ch=>{const endEx=ch.start+ch.count;let f=0;
  if(cur>=endEx)f=100;else if(cur<ch.start)f=0;else f=((cur-ch.start+1)/ch.count)*100;
  ch.fill.style.width=f+'%';ch.el.classList.toggle('cur',cur>=ch.start&&cur<endEx);});}
function applyTheme(){slides.forEach(s=>{const b=s.dataset.base,e=mode==='mix'?b:mode;
  s.classList.toggle('is-dark',e==='dark');s.classList.toggle('is-light',e==='light');});}
function isMobile(){return matchMedia('(max-width:820px),(orientation:portrait) and (max-width:1024px)').matches}
function fit(){if(isMobile()){document.body.classList.add('mobile');stage.style.transform='none';}
  else{document.body.classList.remove('mobile');stage.style.transform='scale('+Math.min(innerWidth/1280,innerHeight/720)+')';}}
function countUp(s){s.querySelectorAll('[data-count]').forEach(el=>{const t=parseFloat(el.dataset.count);
  if(isNaN(t))return;const dec=(el.dataset.count.split('.')[1]||'').length,d=850,t0=performance.now();
  (function st(n){const p=Math.min((n-t0)/d,1),e=1-Math.pow(1-p,3);el.textContent=(t*e).toFixed(dec);
  p<1?requestAnimationFrame(st):el.textContent=t.toFixed(dec);})(t0);});}
function updateNotes(){notesBody.textContent=slides[cur].dataset.notes||'';notesN.textContent=(cur+1)+' / '+total;}
function go(n){n=Math.max(0,Math.min(total-1,n));if(n===cur&&slides[cur].classList.contains('active')){countUp(slides[cur]);return}
  const dir=n>cur?1:-1,mob=document.body.classList.contains('mobile');
  const out=slides[cur];out.classList.remove('active');
  if(!reduced&&!mob)out.style.transform='translateX('+(-dir*34)+'px)';
  cur=n;const s=slides[cur];
  if(!reduced&&!mob){s.style.transition='none';s.style.transform='translateX('+(dir*34)+'px)';void s.offsetWidth;s.style.transition='';}
  s.classList.add('active');s.style.transform='';if(mob)s.scrollTop=0;
  [...s.querySelectorAll('.reveal')].forEach((el,i)=>el.style.transitionDelay=(reduced?0:Math.min(i*48,560))+'ms');
  counter.textContent=String(cur+1).padStart(2,'0')+' / '+String(total).padStart(2,'0');
  updateSeg();updateNotes();if(!reduced)countUp(s);location.hash=cur+1;}
function next(){go(cur+1)}function prev(){go(cur-1)}
addEventListener('keydown',e=>{const k=e.key.toLowerCase();
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();stopPlay();next()}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();stopPlay();prev()}
  else if(e.key==='Home'){stopPlay();go(0)}else if(e.key==='End'){stopPlay();go(total-1)}
  else if(k==='t')cycleMode();else if(k==='f')toggleFs();else if(k==='o')toggleToc();else if(k==='p')togglePlay();else if(k==='n')toggleNotes();
  else if(e.key==='Escape'){document.querySelector('.toc').classList.remove('open');notes.classList.remove('open');}});
let wlock=false;
addEventListener('wheel',e=>{if(document.body.classList.contains('mobile')||wlock)return;
  const d=Math.abs(e.deltaY)>=Math.abs(e.deltaX)?e.deltaY:e.deltaX;if(Math.abs(d)<26)return;
  wlock=true;setTimeout(()=>wlock=false,720);stopPlay();d>0?next():prev();},{passive:true});
function cycleMode(){mode=mode==='mix'?'dark':mode==='dark'?'light':'mix';localStorage.setItem('aecode-pitch-mode',mode);
  applyTheme();document.querySelector('#mode-ico').textContent=mode==='mix'?'◐':mode==='dark'?'●':'○';}
function toggleFs(){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}
function toggleToc(){document.querySelector('.toc').classList.toggle('open')}
function toggleNotes(){const o=notes.classList.toggle('open');document.querySelector('#btn-notes').classList.toggle('on',o);}
let timer=null;
function setPlay(p){const b=document.querySelector('#btn-play');b.classList.toggle('playing',p);b.querySelector('#play-ico').textContent=p?'❚❚':'▶';}
function togglePlay(){timer?stopPlay():(timer=setInterval(()=>{cur>=total-1?stopPlay():next()},14000),setPlay(true));}
function stopPlay(){if(timer){clearInterval(timer);timer=null;setPlay(false);}}
document.querySelector('.left').onclick=()=>{stopPlay();prev()};
document.querySelector('.right').onclick=()=>{stopPlay();next()};
document.querySelector('#btn-prev').onclick=()=>{stopPlay();prev()};
document.querySelector('#btn-next').onclick=()=>{stopPlay();next()};
document.querySelector('#btn-mode').onclick=cycleMode;document.querySelector('#btn-fs').onclick=toggleFs;
document.querySelector('#btn-toc').onclick=toggleToc;document.querySelector('#btn-play').onclick=togglePlay;
document.querySelector('#btn-notes').onclick=toggleNotes;document.querySelector('.toc-close').onclick=toggleToc;
document.querySelectorAll('.toc-item').forEach(b=>b.onclick=()=>{stopPlay();go(+b.dataset.go);toggleToc()});
let tx=0,ty=0;addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY},{passive:true});
addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx,dy=e.changedTouches[0].clientY-ty;
  if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4){stopPlay();dx<0?next():prev()}});
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(fit,120)});
applyTheme();fit();go(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));
document.querySelector('#mode-ico').textContent=mode==='mix'?'◐':mode==='dark'?'●':'○';
"""

HTML=f"""<!DOCTYPE html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AECODE · Pitch Deck 5 min</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="deck"><div class="stage">{slides_html}</div></div>
<div class="chrome"><div class="segbar" id="segbar"></div><div class="counter">01 / {total:02d}</div>
<div class="ctrl">
<button id="btn-toc" title="Índice (O)" aria-label="Índice">☰</button>
<button id="btn-notes" title="Guion (N)" aria-label="Guion">✎</button>
<button id="btn-play" title="Auto-play (P)" aria-label="Auto-play"><span id="play-ico">▶</span></button>
<button id="btn-mode" title="Tema (T)" aria-label="Tema"><span id="mode-ico">◐</span></button>
<button id="btn-prev" title="Anterior (←)" aria-label="Anterior">‹</button>
<button id="btn-next" title="Siguiente (→)" aria-label="Siguiente">›</button>
<button id="btn-fs" title="Pantalla completa (F)" aria-label="Pantalla completa">⛶</button>
</div></div>
<div class="arrow-zone left"></div><div class="arrow-zone right"></div>
<div class="notes" id="notes"><div class="notes-h">Guion del orador <span id="notes-n"></span></div><p id="notes-body"></p></div>
<div class="toc"><button class="toc-close" aria-label="Cerrar">✕</button>
<h3>Índice · {total} slides</h3><div class="toc-grid">{toc_items}</div></div>
<script>{JS}</script></body></html>"""

out=pathlib.Path(__file__).parent/"index.html"
out.write_text(HTML,encoding="utf-8")
print(f"OK -> {out} ({total} slides, {len(HTML):,} bytes)")

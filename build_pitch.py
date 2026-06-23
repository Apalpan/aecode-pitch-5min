# -*- coding: utf-8 -*-
"""
AECODE — Pitch Deck Premium · 5 minutos · 20 slides
Minimalista, elegante, gráficas interactivas (mapa LATAM, motor IA, 2x2 competitivo, donut SVG,
barras/apiladas con tooltips, bloques de pricing). Sin rótulos de sección.
Design system OFICIAL AECODE (Manrope · navy #0E1121 · violeta #4A3AC1 · verde #17B14E · azul #4465EE · rojo dolor).
Light+dark combinado · logos reales · responsive · MODO GUION (tecla N).
Ejecutar:  python build_pitch.py
"""
import html, math, datetime, pathlib

def esc(s): return html.escape(str(s))
def _a(s): return html.escape(str(s), quote=True)

# ---------- helpers ----------
def chip(t): return f'<span class="chip reveal">{t}</span>'
def chiprow(items):
    return '<div class="chiprow reveal">'+''.join(f'<span class="chip2">{esc(i)}</span>' for i in items)+'</div>'
def title(t, cls=""): return f'<h2 class="s-title reveal {cls}">{t}</h2>'
def lead(t): return f'<p class="lead reveal">{t}</p>'
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
def card(head, body, num="", tone="violet"):
    num_h=f'<div class="card-num">{esc(num)}</div>' if num else ""
    return (f'<div class="card reveal card-{tone}">{num_h}'
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
        out+=(f'<div class="bar bar-{tone}" data-tip="{_a(label+" · "+disp)}"><div class="bar-top"><span>{label}</span>'
              f'<b>{disp}</b></div><div class="bar-track"><i style="--w:{pct:.1f}%"></i></div></div>')
    return out+'</div>'

def stackbar(years, segdefs, maxtotal):
    cols=""
    for label,vals,tot in years:
        total=sum(vals); h=total/maxtotal*100
        segs=""
        for i,v in enumerate(vals):
            ph=(v/total*100) if total else 0
            tip=f"{segdefs[i][0]} · US${v}K · {ph:.0f}%"
            segs+=f'<span class="sb-seg" data-tip="{_a(tip)}" style="height:{ph:.2f}%;background:{segdefs[i][1]}"></span>'
        cols+=(f'<div class="sb-col"><div class="sb-bar" style="height:{h:.1f}%">{segs}</div>'
               f'<div class="sb-tot">{tot}</div><div class="sb-lab">{label}</div></div>')
    legend="".join(f'<span class="sb-leg"><i style="background:{c}"></i>{n}</span>' for n,c in segdefs)
    return f'<div class="stackbar reveal"><div class="sb-cols">{cols}</div><div class="sb-legend">{legend}</div></div>'

def tamsamsom(items):
    t=[f"{l} · {v}" for l,v,d in items]
    legend="".join(
        f'<div class="tss-leg reveal" data-tip="{_a(t[i])}"><span class="dot d{i}"></span><div><b>{l}</b> · {v}<small>{d}</small></div></div>'
        for i,(l,v,d) in enumerate(items))
    return f'''<div class="tss reveal"><div class="tss-rings">
        <div class="ring r0" data-tip="{_a(t[0])}"><span>TAM</span></div>
        <div class="ring r1" data-tip="{_a(t[1])}"><span>SAM</span></div>
        <div class="ring r2" data-tip="{_a(t[2])}"><span>SOM</span></div></div>
      <div class="tss-legend">{legend}</div></div>'''

def donut(segs):
    r=52; C=2*math.pi*r; off=0; arcs=""
    for l,p,col in segs:
        dash=C*p/100
        arcs+=(f'<circle class="dn-arc" r="{r}" cx="60" cy="60" fill="none" stroke="{col}" stroke-width="15" '
               f'stroke-dasharray="{dash:.2f} {C-dash:.2f}" stroke-dashoffset="{-off:.2f}" '
               f'data-tip="{_a(l+" · "+str(p)+"%")}" data-lab="{_a(l)}" data-pct="{p}"></circle>')
        off+=dash
    legend="".join(f'<div class="dn-leg reveal" data-tip="{_a(l+" · "+str(p)+"%")}"><span style="background:{c}"></span><b>{p}%</b> {l}</div>' for l,p,c in segs)
    return f'''<div class="donut-wrap reveal">
      <div class="donut-svg"><svg viewBox="0 0 120 120"><g transform="rotate(-90 60 60)">{arcs}</g></svg>
        <div class="dn-center"><b class="dn-c-pct">{segs[0][1]}%</b><span class="dn-c-lab">{esc(segs[0][0])}</span></div></div>
      <div class="donut-legend">{legend}</div></div>'''

def latam(countries):
    pins="".join(f'<div class="lt-pin reveal" data-tip="{_a(c+" · "+t)}"><span class="lt-dot"></span><div class="lt-txt"><b>{c}</b><small>{t}</small></div></div>' for c,t in countries)
    return f'<div class="latam reveal"><div class="lt-grid-bg"></div>{pins}</div>'

def map2x2(points, xlab, ylab):
    dots=""
    for x,y,l,t,big in points:
        dots+=(f'<div class="mp-dot {"mp-big" if big else ""} mp-{t} reveal" data-tip="{_a(l)}" '
               f'style="left:{x}%;top:{y}%"><span>{l}</span></div>')
    return f'''<div class="map2x2 reveal">
      <div class="mp-axis-y">{ylab[0]}<i></i>{ylab[1]}</div>
      <div class="mp-plane">{dots}</div>
      <div class="mp-axis-x">{xlab[0]}<i></i>{xlab[1]}</div></div>'''

def pblock(tag, role, icon, price_html, tone):
    return (f'<div class="pblock reveal pblock-{tone}" data-tip="{_a(tag+" — "+role)}">'
            f'<div class="pb-head"><span class="pb-tag">{tag}</span><span class="pb-role">{role}</span></div>'
            f'<div class="pb-icon">{icon}</div><div class="pb-price">{price_html}</div></div>')

def member(name, role, tone="violet"):
    parts=name.split(); ini=(parts[0][0]+(parts[1][0] if len(parts)>1 else "")).upper()
    return (f'<div class="mem reveal mem-{tone}"><div class="mem-av">{ini}</div>'
            f'<div class="mem-n">{esc(name)}</div><div class="mem-r">{esc(role)}</div></div>')

def demoframe(inner):
    return (f'<div class="demo-frame reveal"><div class="demo-bar"><span></span><span></span><span></span>'
            f'<span class="demo-url">app.aecode.io / mi-ruta</span></div>'
            f'<div class="demo-body">{inner}</div></div>')

# ---------- slides ----------
SLIDES=[]
def S(theme, chapter, layout, content, notes=""):
    SLIDES.append(dict(theme=theme, chapter=chapter, layout=layout, content=content, notes=notes))

LOGO_BIG='<div class="cover-logo reveal big"><img class="logo-dark" src="brand/assets/logos/aecode-logo-principal-fondo-oscuro.png" alt="AECODE"><img class="logo-light" src="brand/assets/logos/aecode-logo-principal-fondo-blanco.png" alt="AECODE"></div>'
LOGO='<div class="cover-logo reveal"><img class="logo-dark" src="brand/assets/logos/aecode-logo-principal-fondo-oscuro.png" alt="AECODE"><img class="logo-light" src="brand/assets/logos/aecode-logo-principal-fondo-blanco.png" alt="AECODE"></div>'

# 01 HOOK
S("dark","Hook","statement",f"""
  {title('La tecnología avanza <span class="grad">más rápido</span> que nuestra capacidad de adoptarla.')}
  {eqs([("Herramientas","≠","adopción","neq"),("Aprender","≠","aplicar","neq"),("Adopción","=","productividad","eq")])}
""",
"La tecnología avanza más rápido que la capacidad de las personas para adoptarla. Una cosa es conocer una herramienta. Otra es adoptarla en el trabajo real. Y en construcción, esa diferencia impacta directamente en productividad. AECODE nace para cerrar esa brecha.")

# 02 OPORTUNIDAD
S("dark","Oportunidad","statement",f"""
  {title('El sector que <span class="grad">mueve el mundo</span> — y necesita reaprender')}
  <div class="statrow statrow-2 bare">
    {stat("280","Personas trabajan en construcción","", suffix="M+")}
    {stat("44","De las habilidades cambian en 5 años","", suffix="%", tone="blue")}
  </div>
""",
"La construcción no se detiene. Se seguirán construyendo viviendas, hospitales, carreteras, puentes e infraestructura. Más de 280 millones de personas trabajan en construcción en el mundo. Pero las habilidades están cambiando rápido. La oportunidad está en formar talento capaz de aprender, aplicar y adaptarse a la velocidad que el sector exige.")

# 03 POR QUÉ AHORA — LATAM
S("dark","Por qué ahora","split-latam",f"""
  <div class="split-latam">
   <div class="sl-left">
     {quote('Adoptar tecnología <span class="grad">ya no es opcional</span>.')}
     {lead('Latinoamérica ya impulsa <b>BIM</b> e <b>IA</b> en construcción.')}
     {chiprow(["Digitalización BIM","Automatización","Productividad","IA"])}
   </div>
   <div class="sl-right">{latam([("México","Programas BIM · IA"),("Colombia","Programas BIM · IA"),("Costa Rica","Transformación digital"),("Perú","Programas BIM · IA"),("Brasil","Transformación digital"),("Chile","Programas BIM · IA"),("Uruguay","Programas BIM"),("Argentina","Programas BIM · IA")])}</div>
  </div>
""",
"La construcción está entrando a una nueva etapa digital. Digitalización BIM, automatización, IA y herramientas digitales ya no son una ventaja futura: empiezan a ser condición para competir. Y Latinoamérica ya se está moviendo: México, Colombia, Perú, Brasil, Chile y más impulsan BIM e IA en sus proyectos. El reto no es solo tener herramientas, es que las personas sepan usarlas.")

# 04 PROBLEMA CENTRAL — RED
S("light","Problema central","statement",f"""
  {title('No falta contenido.<br>Falta <span class="red">aplicarlo</span>.')}
  <div class="statrow statrow-2 bare">
    {stat("92","De proyectos terminan con sobrecostos o retrasos","el costo de no adoptar tecnología", suffix="%", tone="danger")}
    {stat("0","Rutas claras para pasar de aprender a aplicar","aprendizaje fragmentado", tone="danger")}
  </div>
  {chiprow(["Cursos infinitos","Poca claridad","Poca práctica","Baja adopción"])}
""",
"Hoy no faltan cursos, tutoriales, webinars, comunidades ni respuestas con IA. El problema es que el aprendizaje está fragmentado. El profesional no siempre sabe qué aprender primero, qué le sirve realmente para crecer o cómo aplicarlo en su trabajo. Y la empresa capacita, pero no siempre logra que esa capacitación cambie la forma de trabajar. El costo se ve en los proyectos: 92% terminan con sobrecostos o retrasos.")

# 05 DOLOR REAL — RED
S("light","Dolor real","cards",f"""
  {title('Cuando el aprendizaje no se aplica, <span class="red">todos pagan</span> el costo.')}
  {grid([
    card("Profesional","Aprende, pero no mejora ni demuestra.", num="01", tone="danger"),
    card("Empresa","Capacita, pero no logra adopción.", num="02", tone="danger"),
    card("Proyecto","Errores, retrabajo y baja productividad.", num="03", tone="danger"),
  ],3)}
  {chip("No es un problema educativo: es un problema de productividad")}
""",
"El dolor se ve en tres niveles. Para el profesional: invierte tiempo y dinero, pero no siempre mejora su trabajo, salario o empleabilidad. Para la empresa: invierte en capacitación y tecnología, pero no siempre cambia el comportamiento del equipo. Y para el proyecto: esa brecha se convierte en errores, retrabajo, baja coordinación y pérdida de productividad.")

# 06 SOLUCIÓN — MARCA AECODE
S("dark","Solución","brand",f"""
  {LOGO_BIG}
  {title('Acelera la <span class="grad">adopción tecnológica</span> en construcción.')}
  {flow([("Aprende tecnología",""),("Aplícala en proyectos reales","hot"),("Construye mejor","win")])}
  {lead('No vendemos solo cursos. Convertimos aprendizaje en <b>adopción tecnológica y productividad</b> para profesionales, empresas y proyectos.')}
""",
"AECODE es una plataforma de aprendizaje para arquitectura, ingeniería y construcción. Ayudamos a profesionales y empresas a aprender y aplicar digitalización BIM, automatización, IA y herramientas digitales en el trabajo real. No vendemos solo cursos. Convertimos aprendizaje en adopción tecnológica y productividad.")

# 07 PRODUCTO / DEMO
S("light","Producto / Video Demo","demo",f"""
  <div class="prod">
   <div class="prod-l">
     {title('La plataforma que te guía desde tu <span class="grad">nivel actual</span> hasta el rol que buscas.')}
     <div class="prod-steps reveal">
       <div class="ps"><span>1</span> Aprende</div>
       <div class="ps"><span>2</span> Aplica</div>
       <div class="ps"><span>3</span> Demuestra</div>
     </div>
   </div>
   <div class="prod-r">{demoframe('<div class="mock"><div class="mock-orb"></div><div class="mock-play">▶</div><div class="mock-h">Tu ruta está lista</div><div class="mock-s">Inteligencia artificial aplicada al sector AEC</div><div class="mock-meta">3 módulos · 24 skills · evidencia real</div></div>')}</div>
  </div>
""",
"El usuario identifica su nivel, elige un rol o especialidad y avanza por una ruta práctica. Puede aprender BIM, planificación, costos, coordinación, gestión de obra, automatización o IA aplicada. Aprende con cápsulas cortas, practica con casos reales y genera evidencia de avance. Así pasamos de aprendizaje disperso a progreso guiado.")

# 08 INNOVACIÓN — MOTOR IA
S("dark","Innovación tecnológica","engine",f"""
  {title('Motor de <span class="grad">IA adaptativa</span>', "eng-title")}
  {lead('Se entrena con el criterio de <b>+200 expertos AEC</b>.')}
  <div class="engine reveal">
    <div class="eng-col">
      <div class="eng-h">INPUT</div>
      <div class="eng-item">◍ +200 expertos AEC</div>
      <div class="eng-item">▣ Contenido validado</div>
      <div class="eng-item">⬡ Comunidad · datos</div>
    </div>
    <div class="eng-core">
      <div class="eng-ring"><div class="eng-formula">s* = argmax<br>[α·preparación<br>+ β·relevancia<br>− γ·solape]</div></div>
      <div class="eng-cap">Recomendador · decide qué aprender ahora</div>
    </div>
    <div class="eng-col eng-out">
      <div class="eng-h">RESULTADO</div>
      <div class="eng-item">✓ Ruta personalizada por rol</div>
      <div class="eng-item">✓ Skill verificada con evidencia</div>
      <div class="eng-item">✓ Progreso demostrable</div>
    </div>
  </div>
  <div class="eng-methods reveal">
    <div class="em" data-tip="IRT · ubica tu nivel real"><b>IRT</b> · Diagnóstico</div>
    <div class="em" data-tip="Knowledge Tracing · se ajusta con cada evidencia"><b>Knowledge Tracing</b> · Aprendizaje</div>
    <div class="em" data-tip="Clasificador · valida tu evidencia"><b>Clasificador</b> · Verificación</div>
  </div>
""",
"Nuestra innovación no es poner un chatbot encima de una plataforma. Estamos construyendo un motor de IA adaptativa alimentado por contenido validado y criterio de más de 200 expertos del sector. El sistema diagnostica con modelos tipo IRT, aprende de cada evidencia con knowledge tracing, recomienda la ruta óptima y verifica la evidencia con un clasificador. Entra: expertos, contenido y datos. Sale: ruta personalizada, skill verificada y progreso demostrable.")

# 09 MERCADO
S("light","Mercado","tss",f"""
  {title('Formación digital para <span class="grad">construcción en LATAM</span>')}
  <div class="split">
   <div class="split-l">{tamsamsom([("TAM","US$360 M","Formación digital AEC LATAM"),("SAM","US$87.5 M","Mercado servible"),("SOM 3 años","US$2.5 M","Meta a capturar")])}</div>
   <div class="split-r">{lead('Apuntamos a <b>US$2.5M en 3 años</b> — menos del <b>3%</b> del mercado servible. No necesitamos dominar el mercado: basta capturar una porción de una vertical con alto dolor.')}</div>
  </div>
""",
"Nuestro mercado inicial es formación digital especializada para construcción en Latinoamérica. Estimamos un TAM de 360 millones de dólares, un SAM de 87.5 millones y una meta de capturar 2.5 millones en tres años. Eso representa menos del 3% del mercado servible.")

# 10 MODELO B2C2B
S("dark","Modelo B2C2B","statement",f"""
  {quote('Profesional adopta.<br>Empresa escala.<br><span class="grad">Proyecto mejora.</span>')}
  {flow([("B2C","hot"),("Equipos",""),("B2B","hot"),("B2C2B","win")])}
""",
"Nuestro modelo empieza con el profesional. Construimos comunidad, confianza y adopción con personas que ya quieren mejorar su trabajo. Cuando esos profesionales aplican lo aprendido, la empresa ve valor y puede escalarlo a equipos completos. Así pasamos de adquisición individual a expansión empresarial.")

# 11 MODELO DE NEGOCIO — BLOQUES PRICING
S("dark","Modelo de negocio","blocks",f"""
  {title('Tres líneas clave', "blk-title")}
  {lead('<b>Live valida · On-demand escala · B2B ancla.</b>')}
  <div class="pblocks reveal">
    {pblock("1 · LIVE","valida","🎓",'<b>USD 200</b><small>ticket promedio</small>',"violet")}
    {pblock("2 · ON-DEMAND (B2C)","escala","📚",'<b>USD 40</b><small>microlearning / curso</small><b class="pb-2">USD 250</b><small>suscripción anual</small>',"green")}
    {pblock("3 · B2B","ancla","🏢",'<b>A medida</b><small>planes corporativos</small>',"blue")}
  </div>
""",
"Tenemos tres motores. Live Training genera caja, comunidad y validación, con un ticket promedio de unos 200 dólares. On-demand B2C escala: microlearning desde 40 dólares por curso y suscripción anual de 250. Y B2B ancla con planes corporativos a medida, de mayor valor y recurrencia.")

# 12 TRACCIÓN & COMUNIDAD
S("light","Tracción & comunidad","chart",f"""
  {title('El mercado <span class="grad">ya paga</span> — y la comunidad ya está')}
  <div class="trac">
   <div class="trac-l">{barchart([("2024 · validación",13.6,"US$30K","ink"),("2025 · ×4",54.5,"US$120K","violet"),("2026E",100,"US$220K","green")])}</div>
   <div class="trac-r">
     <div class="statrow bare st-mini">
       {stat("95","Comunidad", suffix="K+", tone="blue")}
       {stat("14","Países", tone="violet")}
       {stat("100","Alianzas", suffix="+", tone="green")}
       {stat("50","Convenios", suffix="+", tone="violet")}
     </div>
   </div>
  </div>
""",
"En 2024 vendimos 30 mil dólares. En 2025 crecimos a 120 mil, cuatro veces más. Para 2026 proyectamos 220 mil. Y no partimos de cero: somos la comunidad más grande en tecnología aplicada a construcción, con más de 95 mil profesionales, presencia en 14 países, más de 100 alianzas y más de 50 convenios. El mercado ya paga por esta necesidad.")

# 13 GO TO MARKET
S("light","Go To Market","statement",f"""
  {title('El B2C da entrada. El <span class="grad">B2B da expansión</span>.')}
  {flow([("Comunidad","hot"),("Diagnóstico",""),("Live",""),("On-demand",""),("B2B","win")])}
  {chiprow(["CAC bajo","NPS alto","Expansión por cuenta"])}
""",
"Nuestro go-to-market parte de comunidad y contenido especializado. Atraemos profesionales, los llevamos a diagnóstico, activamos con programas live, convertimos lo validado en microlearning y escalamos hacia empresas. El B2C nos da entrada. El B2B nos da expansión.")

# 14 MÉTRICA NORTE
S("light","Métrica norte","statement",f"""
  {title('Métrica norte: medimos <span class="grad">adopción real</span>')}
  {grid([
    card("Producto","<b>Prácticas aplicadas completadas / mes.</b><br>No medimos videos vistos: medimos quién <i>aplica</i>.", num="◎", tone="green"),
    card("Negocio","<b>% de revenue de B2B + On-demand AI.</b><br>Mientras más alto, más escalable y recurrente.", num="◷", tone="blue"),
  ],2)}
""",
"Medimos dos cosas. En producto, no queremos solo usuarios viendo videos: queremos prácticas aplicadas completadas por mes, porque eso refleja adopción real. En negocio, medimos qué porcentaje del revenue viene de líneas escalables: B2B y On-demand AI. Esas son nuestras dos métricas norte.")

# 15 DIFERENCIACIÓN — 2x2
S("dark","Diferenciación","map",f"""
  {title('Profundidad <span class="grad">vertical AEC</span> + IA')}
  {map2x2([
    (74,16,"AECODE · ×3/año","green",True),
    (40,22,"Udemy","ink",False),
    (16,64,"Platzi","ink",False),
    (34,60,"Udacity","ink",False),
    (20,78,"Crehana","ink",False),
    (15,90,"Coursera","ink",False),
    (62,66,"KonstruEdu","ink",False),
    (80,62,"ARCUX","ink",False),
    (70,82,"TEDI","ink",False),
    (88,82,"+academias","ink",False),
  ], ("Contenido genérico","AEC (Arq · Ing · Cons)"), ("e-Learning + IA","Cursos e-Learning"))}
""",
"Las plataformas horizontales venden contenido genérico. AECODE compite desde la profundidad vertical en construcción, sumando IA. En el cuadrante superior derecho —AEC más e-Learning con IA— estamos solos, creciendo a tres veces por año. Tenemos comunidad AEC, expertos, rutas por rol, IA sectorial y un modelo que conecta aprendizaje con productividad.")

# 16 ROADMAP
S("light","Roadmap","timeline",f"""
  {title('De operación validada a <span class="grad">plataforma regional</span>')}
  <div class="tl reveal">
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2024</div><div class="tl-what"><b>Live</b> + comunidad.</div></div>
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2025</div><div class="tl-what">Primer <b>B2B</b> + ×4 crecimiento.</div></div>
    <div class="tl-item"><div class="tl-dot"></div><div class="tl-when">2026</div><div class="tl-what"><b>Microlearning + IA</b>.</div></div>
    <div class="tl-item win"><div class="tl-dot"></div><div class="tl-when">2027</div><div class="tl-what"><b>LATAM</b> + AI Talent.</div></div>
  </div>
""",
"En 2024 validamos comunidad y programas en vivo. En 2025 hicimos nuestro primer piloto B2B y crecimos cuatro veces. En 2026 lanzamos microlearning e IA aplicada, empezando con programas como IA para ingeniería civil. En 2027 buscamos expansión regional, apoyados en eventos, alianzas y programas como AI Talent.")

# 17 ESCALABILIDAD
S("light","Escalabilidad","chart",f"""
  {title('Mismo conocimiento. Más usuarios. <span class="grad">Menor costo marginal.</span>')}
  {stackbar([("2024",[30,0,0],"100% Live"),("2026E",[132,55,33],"40% escalable"),("2027 Target",[160,140,120],"62% escalable")],
            [("B2C Live","#4465EE"),("B2B","#17B14E"),("On-demand AI","#6D70F9")], 420)}
""",
"La clave es cambiar el mix. Hoy Live valida y genera caja. Pero cada programa validado se convierte en cápsulas, rutas, prácticas y activos digitales reutilizables. Así crece el margen, la recurrencia y la capacidad de escalar sin depender solo de horas humanas.")

# 18 EQUIPO
S("dark","Equipo","team",f"""
  {title('Equipo técnico con <span class="grad">ejecución validada</span> y visión sectorial')}
  <div class="team reveal">
    {member("Yudely Palpan","CTO & Founder","violet")}
    {member("Alejandro Palpan","CEO & Estrategia","blue")}
    {member("Julie Palero","Finanzas & Mercados Int.","green")}
    {member("Daniella Galvez","Head of Academic & Skills","violet")}
    {member("Anggie Palpan","Marketing & Growth","blue")}
    {member("Erika Delgado","Community & BizDev","green")}
    {member("Fabrizio Inga","Head of Data & AI","violet")}
    {member("Fernando Valdivia","Product Engineering","blue")}
    {member("Marlon Tafur","Automatización","green")}
    {member("Anderson","Full Stack","violet")}
    {member("Yary","UX / UI","blue")}
  </div>
""",
"Tenemos un equipo multidisciplinario de más de doce personas con ejecución validada y visión sectorial. Yudely Palpan, CTO y founder; Alejandro Palpan, CEO y estrategia; Julie Palero en finanzas y mercados internacionales; Daniella Galvez en arquitectura académica y de skills; Anggie Palpan en marketing y growth; Erika Delgado en comunidad y desarrollo de negocio; Fabrizio Inga como head of data e IA; más Fernando, Marlon, Anderson y Yary en producto, automatización, full stack y diseño. No es un equipo que recién va a validar: es el que ya construyó comunidad, vendió y creció.")

# 19 ASK
S("dark","Ask","ask",f"""
  {title('US$125K para <span class="grad">escalar lo validado</span>')}
  <div class="ask-grid reveal">
    <div class="ask-left">{donut([("IA + plataforma",60,"#6D70F9"),("Growth B2C2B / LATAM",30,"#17B14E"),("Microlearning",10,"#4465EE")])}</div>
    <div class="ask-right">
      {bullets(["<b>60%</b> — IA + plataforma","<b>30%</b> — growth B2C2B / LATAM","<b>10%</b> — microlearning"])}
      <div class="ask-note reveal">El capital no financia una idea: financia convertir una operación validada en una <b>plataforma escalable</b>.</div>
    </div>
  </div>
""",
"Buscamos 125 mil dólares. El 60% irá a IA y plataforma. El 30% a growth B2C2B y expansión LATAM. El 10% a producción de microlearning. El capital no financia una idea. Financia la conversión de una operación validada en una plataforma escalable.")

# 20 CIERRE
S("dark","Cierre","close",f"""
  {LOGO}
  <div class="close-cta reveal">Aprende · Aplica · <span class="grad">Construye mejor</span></div>
  <div class="close-mail reveal">apalpan@genplusdesign.com · AECODE</div>
""",
"La construcción no se transforma solo con más herramientas ni más cursos. Se transforma cuando su gente aprende a aplicar tecnología en el trabajo real. AECODE existe para acelerar esa adopción tecnológica en construcción. Aprende, aplica, construye mejor.")

# ---------- render ----------
def render_slide(i,s):
    return (f'<section class="slide" data-base="{s["theme"]}" data-ch="{esc(s["chapter"])}" data-notes="{_a(s["notes"])}" data-idx="{i}">'
            f'<div class="slide-inner layout-{s["layout"]}">{s["content"]}</div>'
            f'<img class="slide-mark" src="brand/assets/logos/aecode_isotipo_principal.png" alt="">'
            f'<div class="slide-foot"><span class="foot-n">{i+1:02d}<i>/</i>{len(SLIDES):02d}</span></div></section>')
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
  --line:#C7C2EC; --card:#FFFFFF; --card-line:#E6E3F4; --danger:#E5484D;
  --accent:#4A3AC1; --accent2:#4465EE; --accent3:#17B14E; --ink-soft:#4A3AC1;
  --grad:linear-gradient(100deg,#4465EE,#6D12E3);
  --grad3:linear-gradient(100deg,#17B14E,#4A3AC1);
  --mesh-a:rgba(74,58,193,.08); --mesh-b:rgba(23,177,78,.08); --chip-bg:#EDEBF9;
}
.is-dark{
  --bg:#0E1121; --bg2:#1B1E3C; --surface:#13172F; --fg:#EEF3F8; --muted:#A2B4CB;
  --line:rgba(124,126,223,.20); --card:rgba(27,30,60,.55); --card-line:rgba(124,126,223,.26); --danger:#FF6B6B;
  --accent:#A6A7FF; --accent2:#7E97FF; --accent3:#2FD06E; --ink-soft:#C9D0F5;
  --grad:linear-gradient(100deg,#7E97FF,#9A5CFF);
  --grad3:linear-gradient(100deg,#2FD06E,#8C97DC);
  --mesh-a:rgba(74,58,193,.40); --mesh-b:rgba(23,177,78,.16); --chip-bg:rgba(124,126,223,.14);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:#05060f;color:#fff;overflow:hidden;font-family:Manrope,"Plus Jakarta Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.deck{position:fixed;inset:0;display:grid;place-items:center}
.stage{width:1280px;height:720px;position:relative;transform-origin:center}
.slide{position:absolute;inset:0;display:grid;place-items:center;background:var(--bg);color:var(--fg);
  opacity:0;visibility:hidden;pointer-events:none;transition:opacity .5s var(--ease),transform .55s var(--ease-out);overflow:hidden}
.slide::before{content:"";position:absolute;inset:-12%;z-index:0;
  background:radial-gradient(40% 52% at 12% 10%,var(--mesh-a),transparent 72%),radial-gradient(46% 54% at 90% 92%,var(--mesh-b),transparent 74%)}
.slide.active{opacity:1;visibility:visible;pointer-events:auto}
.slide-inner{position:relative;z-index:2;width:100%;height:100%;padding:62px 84px 72px;display:flex;flex-direction:column;justify-content:center;gap:24px}
.slide-foot{position:absolute;z-index:3;right:84px;bottom:30px;font-size:12px;letter-spacing:.18em;color:var(--muted);opacity:.65}
.foot-n{font-variant-numeric:tabular-nums;font-weight:700} .foot-n i{opacity:.4;font-style:normal;margin:0 4px}
.reveal{opacity:0;transform:translateY(16px);transition:opacity .6s var(--ease-out),transform .6s var(--ease-out)}
.slide.active .reveal{opacity:1;transform:none}
.s-title{font-weight:800;font-size:clamp(33px,4.8vw,60px);line-height:1.0;letter-spacing:-.03em;text-wrap:balance;max-width:19ch}
.lead{font-size:clamp(16px,1.5vw,21px);line-height:1.5;color:var(--muted);max-width:62ch}
.lead b{color:var(--fg);font-weight:700} .lead i{font-style:italic;color:var(--accent)}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
.red{color:var(--danger)}
.chip{display:inline-flex;align-items:center;gap:9px;align-self:flex-start;font-size:14px;font-weight:700;padding:9px 17px;border-radius:100px;border:1px solid var(--card-line);background:var(--chip-bg);color:var(--fg)}
.chip::before{content:"◆";color:var(--accent3);font-size:10px}
.chiprow{display:flex;gap:11px;flex-wrap:wrap}
.chip2{font-weight:700;font-size:15px;padding:11px 18px;border-radius:100px;background:var(--chip-bg);border:1px solid var(--card-line);color:var(--fg);transition:transform .18s var(--ease),border-color .2s}
.slide.active .chip2:hover{transform:translateY(-2px);border-color:var(--accent)}
/* cover/close/brand */
.layout-cover,.layout-close,.layout-brand{align-items:flex-start;justify-content:center;gap:24px}
.cover-logo img{height:56px;width:auto;display:block} .cover-logo.big img{height:74px}
.logo-light{display:none}.slide.is-light .logo-light{display:block} .slide.is-light .logo-dark{display:none}
.slide-mark{position:absolute;top:34px;right:38px;height:28px;width:auto;z-index:3;opacity:.85;pointer-events:none}
.layout-close .slide-mark,.layout-brand .slide-mark{display:none}
.close-cta{font-weight:800;font-size:clamp(24px,3vw,38px);color:var(--fg);letter-spacing:-.01em}
.close-cta::before{content:"";display:inline-block;width:34px;height:3px;background:var(--grad);border-radius:3px;vertical-align:middle;margin-right:16px}
.close-mail{font-weight:700;font-size:15px;color:var(--muted);margin-top:6px}
/* statement */
.layout-statement,.layout-brand{gap:30px}
.bigquote{font-weight:800;line-height:1.08;letter-spacing:-.03em;font-size:clamp(33px,5vw,60px);text-wrap:balance;max-width:22ch;border-left:3px solid var(--accent3);padding-left:30px}
/* eqs */
.eqs{display:flex;flex-direction:column;gap:15px}
.eq{display:flex;align-items:center;gap:18px;font-weight:800;font-size:clamp(21px,2.8vw,34px)}
.eq span{color:var(--fg)} .eq i{font-style:normal;font-weight:800;font-size:1.05em}
.eq-neq i{color:var(--muted)} .eq-eq i{color:var(--accent3)} .eq-eq span:last-child{color:var(--accent3)}
/* split */
.split{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center}
.split-l,.split-r{display:flex;flex-direction:column;gap:14px}
/* stat */
.statrow{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.statrow-2{grid-template-columns:1fr 1fr} .statrow-3{grid-template-columns:repeat(3,1fr)}
.stat{display:flex;flex-direction:column;gap:4px;padding:18px 20px;border-radius:16px;background:var(--card);border:1px solid var(--card-line);transition:transform .2s var(--ease),box-shadow .25s,border-color .25s}
.slide.active .stat:hover{transform:translateY(-4px);border-color:var(--accent);box-shadow:0 16px 34px rgba(8,10,30,.2)}
.statrow.bare .stat{background:none;border:none;padding:4px 0}
.statrow.bare .stat:hover{transform:none;box-shadow:none}
.stat-num{font-weight:800;line-height:1;font-size:clamp(38px,5vw,64px);letter-spacing:-.03em;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:1px;color:var(--accent)}
.statrow.bare .stat-num{font-size:clamp(50px,7vw,90px)}
.statrow.st-mini .stat-num{font-size:clamp(34px,4.4vw,52px)}
.stat-green .stat-num{color:var(--accent3)} .stat-blue .stat-num{color:var(--accent2)} .stat-danger .stat-num{color:var(--danger)}
.stat-pre,.stat-suf{font-size:.48em;font-weight:700}
.stat-label{font-size:15px;font-weight:700;color:var(--fg);line-height:1.25}
.statrow.bare .stat-label{color:var(--muted);font-weight:600;font-size:14.5px}
.stat-sub{font-size:13px;color:var(--muted);line-height:1.3}
.stat-danger .stat-sub{color:var(--danger);opacity:.85;font-weight:600}
/* cards */
.grid{display:grid;gap:16px}.grid-2{grid-template-columns:repeat(2,1fr)}.grid-3{grid-template-columns:repeat(3,1fr)}
.card{position:relative;padding:24px 22px;border-radius:18px;background:var(--card);border:1px solid var(--card-line);display:flex;flex-direction:column;gap:9px;overflow:hidden;transition:transform .2s var(--ease),box-shadow .25s,border-color .25s}
.slide.active .card:hover{transform:translateY(-5px);border-color:var(--accent);box-shadow:0 18px 38px rgba(8,10,30,.22)}
.card::before{content:"";position:absolute;left:0;top:0;width:100%;height:3px;background:var(--accent)}
.card-green::before{background:var(--accent3)} .card-blue::before{background:var(--accent2)} .card-danger::before{background:var(--danger)}
.card-num{font-weight:800;font-size:26px;color:var(--accent)}
.card-green .card-num{color:var(--accent3)} .card-blue .card-num{color:var(--accent2)} .card-danger .card-num{color:var(--danger)}
.card-head{font-weight:800;font-size:20px;line-height:1.18;color:var(--fg)}
.card-body{font-size:15.5px;line-height:1.45;color:var(--muted)} .card-body b{color:var(--fg)} .card-body i{color:var(--accent);font-style:italic}
/* bullets */
.bullets{list-style:none;display:flex;flex-direction:column;gap:11px}
.bullets li{position:relative;padding-left:24px;font-size:16px;line-height:1.4;color:var(--muted)}
.bullets li b{color:var(--fg);font-weight:700}
.bullets li::before{content:"";position:absolute;left:2px;top:8px;width:8px;height:8px;border-radius:2px;background:var(--accent3);transform:rotate(45deg)}
/* flow */
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.flow-step{font-weight:700;font-size:16.5px;padding:13px 19px;border-radius:13px;background:var(--card);border:1px solid var(--card-line);color:var(--fg);transition:transform .18s var(--ease),border-color .2s}
.slide.active .flow-step:hover{transform:translateY(-3px);border-color:var(--accent2)}
.flow-step.hot{border-color:var(--accent2);color:var(--accent2);box-shadow:0 0 24px rgba(68,101,238,.16)}
.flow-step.win{background:var(--grad3);color:#fff;border:none}
.flow-arr{color:var(--accent);font-weight:800;font-size:18px;font-style:normal}
/* latam */
.layout-split-latam .slide-inner{padding-right:64px}
.split-latam{display:grid;grid-template-columns:1fr 1.05fr;gap:40px;align-items:center;width:100%}
.sl-left{display:flex;flex-direction:column;gap:18px}
.latam{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;padding:10px}
.lt-grid-bg{position:absolute;inset:-10px;z-index:0;border-radius:20px;
  background:linear-gradient(rgba(124,126,223,.12) 1px,transparent 1px) 0 0/100% 28px,
  linear-gradient(90deg,rgba(124,126,223,.12) 1px,transparent 1px) 0 0/28px 100%;
  -webkit-mask:radial-gradient(60% 60% at 50% 50%,#000,transparent);mask:radial-gradient(60% 60% at 50% 50%,#000,transparent)}
.lt-pin{position:relative;z-index:1;display:flex;gap:10px;align-items:flex-start;padding:9px 12px;border-radius:12px;
  background:var(--card);border:1px solid var(--card-line);transition:transform .18s var(--ease),border-color .2s;cursor:default}
.slide.active .lt-pin:hover{transform:translateY(-3px);border-color:var(--accent)}
.lt-dot{width:11px;height:11px;border-radius:50%;background:var(--accent3);margin-top:4px;flex:none;position:relative}
.lt-dot::after{content:"";position:absolute;inset:-5px;border-radius:50%;border:2px solid var(--accent3);opacity:0;animation:ping 2.4s var(--ease) infinite}
@keyframes ping{0%{transform:scale(.6);opacity:.7}70%,100%{transform:scale(1.5);opacity:0}}
.lt-txt b{display:block;font-size:15px;font-weight:800;color:var(--fg)} .lt-txt small{font-size:12px;color:var(--accent-ink,var(--muted));color:var(--muted)}
/* product / demo */
.prod{display:grid;grid-template-columns:1fr 1.05fr;gap:40px;align-items:center;width:100%}
.prod-l{display:flex;flex-direction:column;gap:24px}
.prod-steps{display:flex;flex-direction:column;gap:14px}
.ps{display:flex;align-items:center;gap:14px;font-weight:800;font-size:22px;color:var(--fg)}
.ps span{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-size:15px;color:#fff;background:var(--grad);flex:none}
.demo-frame{border-radius:18px;overflow:hidden;border:1px solid var(--card-line);background:var(--bg2);box-shadow:0 28px 64px rgba(0,0,0,.34)}
.demo-bar{display:flex;align-items:center;gap:7px;padding:12px 17px;background:var(--card);border-bottom:1px solid var(--card-line)}
.demo-bar>span{width:11px;height:11px;border-radius:50%;background:var(--line)}
.demo-url{margin-left:14px;font-size:13px;color:var(--muted);background:var(--bg);padding:5px 14px;border-radius:6px;flex:1;max-width:280px}
.demo-body{padding:0}
.mock{position:relative;padding:46px 28px 40px;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;
  background:radial-gradient(60% 60% at 50% 35%,rgba(124,126,223,.22),transparent 70%)}
.mock-orb{width:96px;height:96px;border-radius:50%;background:conic-gradient(from 0deg,#6D70F9,#4465EE,#17B14E,#6D70F9);filter:blur(2px);opacity:.9;
  box-shadow:0 0 60px rgba(109,112,249,.6);animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.mock-play{position:absolute;top:64px;font-size:30px;color:#fff;opacity:.95}
.mock-h{font-weight:800;font-size:22px;color:var(--fg);margin-top:14px}
.mock-s{font-size:14px;color:var(--muted)} .mock-meta{font-size:12.5px;color:var(--accent);font-weight:700;margin-top:4px}
/* engine */
.layout-engine{gap:14px}
.engine{display:grid;grid-template-columns:1fr auto 1fr;gap:26px;align-items:center;margin-top:2px}
.eng-col{display:flex;flex-direction:column;gap:11px}
.eng-out{align-items:flex-end;text-align:right}
.eng-h{font-weight:800;font-size:12px;letter-spacing:.2em;color:var(--accent2)}
.eng-item{font-size:15px;font-weight:600;color:var(--fg);padding:8px 13px;border-radius:10px;background:var(--card);border:1px solid var(--card-line)}
.eng-out .eng-item{color:var(--accent3)}
.eng-core{display:flex;flex-direction:column;align-items:center;gap:10px}
.eng-ring{width:184px;height:184px;border-radius:50%;display:grid;place-items:center;text-align:center;position:relative;
  background:radial-gradient(circle,rgba(124,126,223,.12),transparent 68%)}
.eng-ring::before{content:"";position:absolute;inset:0;border-radius:50%;border:3px solid transparent;
  background:conic-gradient(from 0deg,#6D70F9,#4465EE,#17B14E,#6D70F9) border-box;-webkit-mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:spin 9s linear infinite}
.eng-formula{font-size:14px;font-weight:700;line-height:1.5;color:var(--fg);font-style:italic;z-index:1}
.eng-cap{font-size:12.5px;font-weight:700;color:var(--accent3);text-align:center}
.eng-methods{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:6px}
.em{font-size:14px;color:var(--muted);padding:11px 15px;border-radius:12px;background:var(--card);border:1px solid var(--card-line);transition:border-color .2s,transform .18s var(--ease);cursor:default}
.slide.active .em:hover{border-color:var(--accent2);transform:translateY(-2px)} .em b{color:var(--accent2)}
/* barchart */
.barchart{display:flex;flex-direction:column;gap:15px;width:100%}
.bar{cursor:default} .bar-top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;font-size:15px}
.bar-top span{color:var(--fg);font-weight:600} .bar-top b{color:var(--accent);font-weight:800;font-variant-numeric:tabular-nums}
.bar-track{height:13px;border-radius:100px;background:var(--bg2);overflow:hidden;border:1px solid var(--card-line)}
.bar-track i{display:block;height:100%;width:var(--w);border-radius:100px;background:var(--grad);transform:scaleX(0);transform-origin:left;transition:transform .9s var(--ease-out),filter .2s}
.slide.active .bar-track i{transform:scaleX(1)} .slide.active .bar:hover .bar-track i{filter:brightness(1.14)}
.bar-green .bar-top b{color:var(--accent3)} .bar-green .bar-track i{background:linear-gradient(100deg,var(--green),#43d98f)}
.bar-blue .bar-top b{color:var(--accent2)} .bar-blue .bar-track i{background:linear-gradient(100deg,var(--blue),#6f8cff)}
.bar-ink .bar-top b{color:var(--muted)} .bar-ink .bar-track i{background:var(--muted);opacity:.7}
/* traccion combo */
.trac{display:grid;grid-template-columns:1.15fr 1fr;gap:40px;align-items:center}
.st-mini{grid-template-columns:1fr 1fr;gap:16px 24px}
/* stackbar */
.stackbar{display:flex;flex-direction:column;gap:18px;width:100%}
.sb-cols{display:flex;align-items:flex-end;justify-content:space-around;gap:30px;height:248px;padding:0 6px;border-bottom:2px solid var(--card-line)}
.sb-col{flex:1;max-width:132px;display:flex;flex-direction:column;align-items:center;gap:8px;height:100%;justify-content:flex-end}
.sb-bar{width:70px;border-radius:9px 9px 0 0;overflow:hidden;display:flex;flex-direction:column-reverse;transform:scaleY(0);transform-origin:bottom;transition:transform .85s var(--ease-out)}
.slide.active .sb-bar{transform:scaleY(1)}
.sb-seg{width:100%;display:block;cursor:pointer;transition:filter .2s}
.slide.active .sb-bar:hover .sb-seg{filter:brightness(.55)} .slide.active .sb-seg:hover{filter:brightness(1.2)}
.sb-tot{font-weight:800;font-size:16px;color:var(--fg)} .sb-lab{font-size:13px;font-weight:700;color:var(--muted)}
.sb-legend{display:flex;gap:22px;justify-content:center;flex-wrap:wrap}
.sb-leg{display:flex;align-items:center;gap:7px;font-size:14px;color:var(--muted);font-weight:600} .sb-leg i{width:13px;height:13px;border-radius:4px}
/* tss */
.tss{display:flex;gap:30px;align-items:center}
.tss-rings{position:relative;width:236px;height:236px;flex:none}
.ring{position:absolute;border-radius:50%;display:grid;place-items:start center;padding-top:11px;font-weight:800;font-size:13px;left:50%;top:50%;transform:translate(-50%,-50%);cursor:pointer;transition:filter .2s}
.ring span{color:#fff;letter-spacing:.1em} .slide.active .ring:hover{filter:brightness(1.18) saturate(1.2)}
.ring.r0{width:236px;height:236px;background:rgba(74,58,193,.20);border:1px solid var(--violet)}
.ring.r1{width:162px;height:162px;background:rgba(68,101,238,.30);border:1px solid var(--blue)}
.ring.r2{width:90px;height:90px;background:var(--green);border:1px solid var(--green);place-items:center;padding:0}
.is-light .ring.r0 span,.is-light .ring.r1 span{color:#2a2470}
.tss-legend{display:flex;flex-direction:column;gap:13px}
.tss-leg{display:flex;gap:11px;align-items:flex-start;font-size:14.5px;cursor:default;transition:transform .18s var(--ease)}
.slide.active .tss-leg:hover{transform:translateX(4px)}
.tss-leg .dot{width:14px;height:14px;border-radius:4px;margin-top:3px;flex:none}
.tss-leg .d0{background:var(--violet)} .tss-leg .d1{background:var(--blue)} .tss-leg .d2{background:var(--green)}
.tss-leg b{color:var(--fg);font-weight:800} .tss-leg small{display:block;color:var(--muted);font-size:12.5px}
/* donut */
.donut-wrap{display:flex;align-items:center;gap:28px}
.donut-svg{position:relative;width:196px;height:196px;flex:none}
.donut-svg svg{width:100%;height:100%;overflow:visible}
.dn-arc{transition:stroke-width .22s var(--ease),opacity .22s;cursor:pointer}
.slide.active .donut-svg:hover .dn-arc{opacity:.4} .slide.active .donut-svg .dn-arc:hover{opacity:1;stroke-width:21}
.dn-center{position:absolute;inset:0;display:grid;place-items:center;text-align:center;pointer-events:none;gap:2px}
.dn-c-pct{font-weight:800;font-size:34px;color:var(--fg);font-variant-numeric:tabular-nums;line-height:1}
.dn-c-lab{font-size:12.5px;color:var(--muted);max-width:96px;line-height:1.2;font-weight:600}
.donut-legend{display:flex;flex-direction:column;gap:13px}
.dn-leg{display:flex;align-items:center;gap:10px;font-size:15px;color:var(--muted);cursor:default;transition:transform .18s var(--ease)}
.slide.active .dn-leg:hover{transform:translateX(4px)} .dn-leg span{width:14px;height:14px;border-radius:4px;flex:none} .dn-leg b{color:var(--fg);font-weight:800}
/* pricing blocks */
.layout-blocks{gap:18px}
.pblocks{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:4px}
.pblock{padding:24px 22px;border-radius:20px;background:var(--card);border:1px solid var(--card-line);display:flex;flex-direction:column;gap:14px;transition:transform .2s var(--ease),box-shadow .25s,border-color .25s;position:relative;overflow:hidden}
.pblock::before{content:"";position:absolute;left:0;top:0;width:100%;height:4px;background:var(--accent)}
.pblock-green::before{background:var(--accent3)} .pblock-blue::before{background:var(--accent2)}
.slide.active .pblock:hover{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 22px 46px rgba(8,10,30,.26)}
.pb-head{display:flex;flex-direction:column;gap:4px}
.pb-tag{font-weight:800;font-size:13px;letter-spacing:.06em;color:var(--accent);text-transform:uppercase}
.pblock-green .pb-tag{color:var(--accent3)} .pblock-blue .pb-tag{color:var(--accent2)}
.pb-role{font-weight:700;font-size:17px;color:var(--fg)}
.pb-icon{font-size:34px;line-height:1}
.pb-price b{display:block;font-weight:800;font-size:30px;color:var(--fg);letter-spacing:-.02em} .pb-price b.pb-2{margin-top:10px}
.pb-price small{display:block;font-size:13px;color:var(--muted);font-weight:600}
/* map2x2 */
.map2x2{display:grid;grid-template-columns:20px 1fr;grid-template-rows:1fr 20px;gap:6px;width:100%;height:404px}
.mp-axis-y{grid-column:1;grid-row:1;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.mp-axis-y::before,.mp-axis-x::before{content:"";flex:1}
.mp-axis-x{grid-column:2;grid-row:2;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.mp-plane{grid-column:2;grid-row:1;position:relative;border-left:2px solid var(--card-line);border-bottom:2px solid var(--card-line);
  background:linear-gradient(var(--card-line) 1px,transparent 1px) 0 50%/100% 50%,linear-gradient(90deg,var(--card-line) 1px,transparent 1px) 50% 0/50% 100%;background-color:rgba(124,126,223,.05)}
.mp-dot{position:absolute;transform:translate(-50%,-50%);font-size:13px;font-weight:700;color:var(--fg);white-space:nowrap;padding:6px 11px;border-radius:9px;background:var(--card);border:1px solid var(--card-line);cursor:default;transition:transform .18s var(--ease),border-color .2s}
.slide.active .mp-dot:hover{transform:translate(-50%,-50%) scale(1.08);border-color:var(--accent)}
.mp-big{color:#fff;background:var(--grad3);border:none;font-weight:800;font-size:14.5px;box-shadow:0 0 26px rgba(38,185,111,.4)}
/* team */
.layout-team{gap:22px}
.team{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.mem{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;padding:16px 10px;border-radius:16px;background:var(--card);border:1px solid var(--card-line);transition:transform .2s var(--ease),border-color .2s}
.slide.active .mem:hover{transform:translateY(-5px);border-color:var(--accent)}
.mem-av{width:54px;height:54px;border-radius:50%;display:grid;place-items:center;font-weight:800;font-size:19px;color:#fff;background:var(--grad)}
.mem-green .mem-av{background:linear-gradient(135deg,#17B14E,#1fa9a0)} .mem-blue .mem-av{background:linear-gradient(135deg,#4465EE,#6f8cff)}
.mem-n{font-weight:800;font-size:14px;color:var(--fg);line-height:1.15} .mem-r{font-size:11.5px;color:var(--muted);line-height:1.25}
/* timeline */
.tl{display:grid;grid-template-columns:repeat(4,1fr);position:relative;margin:16px 0}
.tl::before{content:"";position:absolute;left:6%;right:6%;top:9px;height:2px;background:var(--line)}
.tl-item{position:relative;padding:0 14px;display:flex;flex-direction:column;gap:9px}
.tl-dot{width:18px;height:18px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 5px var(--bg),0 0 18px rgba(74,58,193,.4);z-index:2;transition:transform .2s var(--ease)}
.slide.active .tl-item:hover .tl-dot{transform:scale(1.25)}
.tl-item.win .tl-dot{background:var(--accent3);box-shadow:0 0 0 5px var(--bg),0 0 18px rgba(38,185,111,.45)}
.tl-when{font-weight:800;font-size:19px;color:var(--accent)} .tl-item.win .tl-when{color:var(--accent3)}
.tl-what{font-size:15px;line-height:1.4;color:var(--muted)} .tl-what b{color:var(--fg)}
/* ask */
.layout-ask{gap:18px}
.ask-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:40px;align-items:center;margin-top:6px}
.ask-left{display:flex;justify-content:center}.ask-right{display:flex;flex-direction:column;gap:16px}
.ask-note{font-size:15px;line-height:1.5;color:var(--muted);padding:14px 18px;border-radius:14px;background:var(--card);border:1px solid var(--card-line)} .ask-note b{color:var(--fg)}
/* tooltip */
.tip{position:fixed;z-index:75;pointer-events:none;transform:translate(-50%,-100%);background:rgba(14,17,33,.97);color:#eef1ff;border:1px solid rgba(124,126,223,.55);padding:8px 13px;border-radius:10px;font-size:13.5px;font-weight:700;white-space:nowrap;opacity:0;transition:opacity .16s;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.tip.show{opacity:1}
/* chrome */
.chrome{position:fixed;inset:0;z-index:50;pointer-events:none}
.ctrl{position:absolute;bottom:22px;right:26px;display:flex;gap:8px;pointer-events:auto}
.ctrl button{width:39px;height:39px;border-radius:11px;border:1px solid rgba(255,255,255,.16);background:rgba(20,26,61,.6);color:#fff;backdrop-filter:blur(10px);cursor:pointer;font-size:15px;display:grid;place-items:center;transition:transform .15s,background .2s}
.ctrl button:hover{background:rgba(74,58,193,.7)} .ctrl button:active{transform:scale(.92)}
.ctrl button:focus-visible{outline:2px solid var(--green);outline-offset:2px}
.arrow-zone{position:fixed;top:0;bottom:0;width:13%;z-index:40;cursor:pointer}.arrow-zone.left{left:0}.arrow-zone.right{right:0}
.notes{position:fixed;left:0;right:0;bottom:0;z-index:55;background:rgba(10,12,30,.97);backdrop-filter:blur(14px);border-top:2px solid rgba(124,126,223,.45);padding:18px 30px 24px;transform:translateY(101%);transition:transform .35s var(--ease);pointer-events:auto;max-height:44vh;overflow:auto}
.notes.open{transform:none}
.notes-h{font-weight:800;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#A6A7FF;margin-bottom:9px;display:flex;justify-content:space-between;align-items:center}
.notes-h span{color:#8C97DC}
.notes p{font-size:clamp(15px,1.5vw,18px);line-height:1.6;color:#e7eaff;max-width:96ch}
.toc{position:fixed;inset:0;z-index:60;background:rgba(8,10,28,.96);backdrop-filter:blur(14px);padding:54px 64px;overflow:auto;display:none}
.toc.open{display:block}
.toc h3{font-weight:800;font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:#8b7df0;margin-bottom:22px}
.toc-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:9px}
.toc-item{display:flex;flex-direction:column;gap:4px;padding:12px 14px;border-radius:11px;background:rgba(30,37,78,.7);border:1px solid rgba(255,255,255,.08);color:#fff;cursor:pointer;text-align:left;transition:transform .15s,border-color .2s}
.toc-item:hover{transform:translateY(-3px);border-color:#43d98f}
.toc-n{font-weight:800;font-size:16px;color:#43d98f} .toc-t{font-size:12px;color:#a9b2da;line-height:1.25}
.toc-close{position:absolute;top:26px;right:36px;font-size:22px;background:none;border:none;color:#fff;cursor:pointer}
.segbar{position:absolute;top:0;left:0;right:0;height:5px;display:flex;gap:2px;pointer-events:auto}
.seg{flex:var(--c) 1 0;height:4px;align-self:flex-start;background:rgba(140,151,220,.22);position:relative;cursor:pointer;transition:height .2s,background .25s}
.seg:hover,.seg.cur{height:7px;background:rgba(140,151,220,.38)}
.seg i{position:absolute;left:0;top:0;height:100%;width:var(--f,0%);background:linear-gradient(90deg,#4465EE,#17B14E);transition:width .45s var(--ease)}
.seg .lab{position:absolute;top:12px;left:0;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#e7eaff;background:rgba(14,17,33,.94);border:1px solid rgba(124,126,223,.4);padding:4px 9px;border-radius:7px;white-space:nowrap;opacity:0;transform:translateY(-4px);transition:opacity .2s,transform .2s;pointer-events:none;z-index:6}
.seg:hover .lab{opacity:1;transform:none}
#btn-play.playing,#btn-notes.on{background:rgba(74,58,193,.85);color:#fff;box-shadow:0 0 18px rgba(124,126,223,.6)}
/* responsive móvil */
body.mobile .deck{place-items:stretch}
body.mobile .stage{width:100vw;height:100dvh;transform:none!important}
body.mobile .slide{display:block;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch}
body.mobile .slide-inner{position:static;height:auto;min-height:100%;justify-content:flex-start;padding:54px clamp(18px,5.5vw,30px) 82px;gap:clamp(16px,4vw,24px)}
body.mobile .slide-foot{right:clamp(18px,5.5vw,30px);bottom:18px} body.mobile .slide-mark{top:18px;right:18px;height:24px}
body.mobile .split,body.mobile .split-latam,body.mobile .prod,body.mobile .trac,body.mobile .ask-grid,body.mobile .grid-2,body.mobile .grid-3,body.mobile .tss,body.mobile .donut-wrap,body.mobile .engine,body.mobile .pblocks,body.mobile .eng-methods{display:flex;flex-direction:column;gap:16px}
body.mobile .statrow,body.mobile .statrow-2,body.mobile .statrow-3,body.mobile .st-mini,body.mobile .latam{display:grid;grid-template-columns:1fr 1fr;gap:14px}
body.mobile .team{grid-template-columns:repeat(3,1fr);gap:10px}
body.mobile .eng-out{align-items:flex-start;text-align:left}
body.mobile .s-title{font-size:clamp(26px,7.4vw,38px);max-width:none}
body.mobile .bigquote{font-size:clamp(27px,7.6vw,42px);max-width:none}
body.mobile .lead{font-size:clamp(15px,4vw,18px);max-width:none}
body.mobile .eq{font-size:clamp(19px,5.2vw,28px)}
body.mobile .statrow.bare .stat-num{font-size:clamp(42px,12vw,64px)}
body.mobile .tss-rings,body.mobile .eng-ring{margin:0 auto}
body.mobile .donut-svg{width:160px;height:160px}
body.mobile .map2x2{height:340px}
body.mobile .stackbar{overflow-x:auto} body.mobile .sb-cols{gap:16px;height:210px} body.mobile .sb-bar{width:50px}
body.mobile .ctrl{bottom:14px;right:11px;gap:7px} body.mobile .ctrl button{width:42px;height:42px}
body.mobile .arrow-zone{display:none}
body.mobile .toc{padding:48px 22px} body.mobile .toc-grid{grid-template-columns:repeat(2,1fr)} body.mobile .notes{max-height:55vh}
@media (prefers-reduced-motion:reduce){
  .reveal{transition:none!important;opacity:1!important;transform:none!important}
  .slide{transition:opacity .2s!important}
  .bar-track i,.sb-bar,.seg i,.eng-ring::before,.mock-orb,.lt-dot::after{transition:none!important;animation:none!important}
  .slide.active .bar-track i{transform:scaleX(1)} .slide.active .sb-bar{transform:scaleY(1)}
}
"""

JS = r"""
const slides=[...document.querySelectorAll('.slide')];const total=slides.length;let cur=0;
const stage=document.querySelector('.stage'),segbar=document.querySelector('#segbar'),tip=document.querySelector('#tip');
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
  if(isNaN(t))return;const dec=(el.dataset.count.split('.')[1]||'').length,d=900,t0=performance.now();
  (function st(n){const p=Math.min((n-t0)/d,1),e=1-Math.pow(1-p,3);el.textContent=(t*e).toFixed(dec);
  p<1?requestAnimationFrame(st):el.textContent=t.toFixed(dec);})(t0);});}
function updateNotes(){notesBody.textContent=slides[cur].dataset.notes||'';notesN.textContent=(cur+1)+' / '+total;}
function go(n){n=Math.max(0,Math.min(total-1,n));if(n===cur&&slides[cur].classList.contains('active')){countUp(slides[cur]);return}
  const dir=n>cur?1:-1,mob=document.body.classList.contains('mobile');
  const out=slides[cur];out.classList.remove('active');
  if(!reduced&&!mob)out.style.transform='translateX('+(-dir*36)+'px)';
  cur=n;const s=slides[cur];
  if(!reduced&&!mob){s.style.transition='none';s.style.transform='translateX('+(dir*36)+'px)';void s.offsetWidth;s.style.transition='';}
  s.classList.add('active');s.style.transform='';if(mob)s.scrollTop=0;
  [...s.querySelectorAll('.reveal')].forEach((el,i)=>el.style.transitionDelay=(reduced?0:Math.min(i*52,620))+'ms');
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
addEventListener('mouseover',e=>{const t=e.target.closest('[data-tip]');if(t){tip.textContent=t.dataset.tip;tip.classList.add('show');}
  const a=e.target.closest('.dn-arc');if(a){const w=a.closest('.donut-wrap');w.querySelector('.dn-c-pct').textContent=a.dataset.pct+'%';w.querySelector('.dn-c-lab').textContent=a.dataset.lab;}});
addEventListener('mousemove',e=>{if(tip.classList.contains('show')){tip.style.left=e.clientX+'px';tip.style.top=(e.clientY-16)+'px';}});
addEventListener('mouseout',e=>{if(e.target.closest('[data-tip]'))tip.classList.remove('show');});
function cycleMode(){mode=mode==='mix'?'dark':mode==='dark'?'light':'mix';localStorage.setItem('aecode-pitch-mode',mode);
  applyTheme();document.querySelector('#mode-ico').textContent=mode==='mix'?'◐':mode==='dark'?'●':'○';}
function toggleFs(){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}
function toggleToc(){document.querySelector('.toc').classList.toggle('open')}
function toggleNotes(){const o=notes.classList.toggle('open');document.querySelector('#btn-notes').classList.toggle('on',o);}
let timer=null;
function setPlay(p){const b=document.querySelector('#btn-play');b.classList.toggle('playing',p);b.querySelector('#play-ico').textContent=p?'❚❚':'▶';}
function togglePlay(){timer?stopPlay():(timer=setInterval(()=>{cur>=total-1?stopPlay():next()},14000),setPlay(true));}
function stopPlay(){if(timer){clearInterval(timer);timer=null;setPlay(false);}}
document.querySelector('.left').onclick=()=>{stopPlay();prev()};document.querySelector('.right').onclick=()=>{stopPlay();next()};
document.querySelector('#btn-prev').onclick=()=>{stopPlay();prev()};document.querySelector('#btn-next').onclick=()=>{stopPlay();next()};
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
<div class="chrome"><div class="segbar" id="segbar"></div>
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
<div class="tip" id="tip"></div>
<div class="notes" id="notes"><div class="notes-h">Guion del orador <span id="notes-n"></span></div><p id="notes-body"></p></div>
<div class="toc"><button class="toc-close" aria-label="Cerrar">✕</button>
<h3>Índice · {total} slides</h3><div class="toc-grid">{toc_items}</div></div>
<script>{JS}</script></body></html>"""

out=pathlib.Path(__file__).parent/"index.html"
out.write_text(HTML,encoding="utf-8")
print(f"OK -> {out} ({total} slides, {len(HTML):,} bytes)")

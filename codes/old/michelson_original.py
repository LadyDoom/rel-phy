Web VPython 3.2

# === Paramètres globaux ===

scene.width = 600
scene.height = 600
scene.align = 'left'

refEther = False
modifEther = 6

orientation = 0
lamb = 20e-6
c = 1
longV = 20
longH = 20
deltaL = 0

vEther = 0.0
particules = []

posSource = vector(-10, 0, 0)
posDetec = vector(0, -10, 0)

frequence = 0.25
longOnde = 1 / frequence
amplitude = 1

dt = 0.01
dx = 0.05

couleurs_fig = [color.black, color.gray(0.5), color.orange, color.green, color.magenta, color.cyan, color.red]
compteur_fig = 0

suiveurs = []
ondes = []

# === Fonctions ===

class onde:
    def __init__(self, debut, direction, couleur, amplitude, frequence=5, dephasage=0):
        self.amplitude = amplitude
        self.frequence = frequence
        self.dephasage = dephasage
        self.omega = 2 * pi * frequence
        self.dir = direction
        self.vertical = False
        self.pos = vector(debut)
        self.avance = 1
        self.sphere = sphere(pos=debut, radius=0.1, color=couleur, make_trail=True, trail_type="curve", interval=1, retain=1000)
        self.k = 2 * pi * frequence / c

    def updatekomega(self):
        frequence_app = self.frequence / (1 - vEther * cos(orientation * pi))
        self.omega = 2 * pi * frequence_app
        self.k = 2 * pi * frequence_app

    def get_amplitude(self, t):
        self.updatekomega()
        axis = vector(1, 0, 0) if not self.vertical else vector(0, 1, 0)
        coord = dot(self.pos, axis)
        return self.amplitude * sin(self.k * coord - self.avance * self.omega * t + self.dephasage)

    def update(self, t):
        amp = self.get_amplitude(t)
        crete = vector(0, amp, 0) if not self.vertical else vector(amp, 0, 0)
        self.sphere.pos = self.pos + crete
        self.pos += self.dir

def majVitesse(ev):
    global vEther
    try:
        vEther = float(eInput.text)
        if vEther < 0: vEther = 0
        if vEther > 1: vEther = 1
    except:
        vEther = 0
    eTexteSlider.text = f" {vEther:.1f} c"
    ventEther.axis = modifEther * vEther * vector(cos(orientation * pi), sin(orientation * pi), 0)
    majInterference()
    lancer_animation_onde()

def majOrientation(ev):
    global orientation
    try:
        orientation = float(oeInput.text)
        if orientation < 0: orientation = 0
        if orientation > 2: orientation = 2
    except:
        orientation = 0
    oeTexteSlider.text = f" {orientation:.2f} Pi"
    direction = vector(cos(orientation * pi), sin(orientation * pi), 0)
    ventEther.axis = modifEther * vEther * direction
    majInterference()
    lancer_animation_onde()

def majDeltaL(ev):
    global deltaL, longH
    try:
        deltaL = int(bhInput.text)
        if deltaL < -5: deltaL = -5
        if deltaL > 5: deltaL = 5
    except:
        deltaL = 0
    longH = longV + deltaL * (longOnde / 2)
    bhTexteSlider.text = f" {deltaL} λ/4 "
    miroirH.pos = vector(longH / 2, 0, 0)
    majInterference()
    lancer_animation_onde()

def ajoutParticules(nombre, taille):
    global particules
    particules.clear()
    for _ in range(nombre):
        pos = vector(random() * 30 - 15, random() * 30 - 15, random() * 2 - 1)
        p = sphere(pos=pos, radius=taille, color=color.white, opacity=0.3)
        particules.append(p)

def majParticules():
    vitesse = 2 * ventEther.axis
    for p in particules:
        p.pos += vitesse * dt
        if p.pos.x > 15: p.pos.x = -15
        if p.pos.x < -15: p.pos.x = 15
        if p.pos.y > 15: p.pos.y = -15
        if p.pos.y < -15: p.pos.y = 15

def temps(L, orientation):
    terme1 = 2 * L / c
    terme2 = sqrt(1 - vEther ** 2 * sin(orientation * pi) ** 2)
    terme3 = 1 - vEther ** 2
    return terme1 * (terme2 / terme3)

def majInterference():
    global courbe
    courbe.delete()
    d0 = abs(longH - longV)
    alpha = 0.1
    t1 = temps(longV, orientation + 1 / 2)
    t2 = temps(longH, orientation)
    delta_phi = (2 * pi * (t1 - t2) * c) / lamb
    for i in range(0, 100):
        courbe.plot(i, cos((2 * pi / 5) * (i * alpha + d0) + delta_phi) ** 2)


def dupliquerCourbe():
    global compteur_fig
    couleur = couleurs_fig[compteur_fig % len(couleurs_fig)]
    compteur_fig += 1
    courbe_snapshot = gcurve(color=couleur)
    d0 = abs(longH - longV)
    alpha = 0.1
    t1 = temps(longV, orientation + 1 / 2)
    t2 = temps(longH, orientation)
    delta_phi = (2 * pi * (t1 - t2) * c) / lamb
    for i in range(0, 100):
        y = cos((2 * pi / 5) * (i * alpha + d0) + delta_phi) ** 2
        courbe_snapshot.plot(i, y)

def animer_onde(onde1, onde2):
    t = 0
    while not ((onde1.pos - posDetec).mag < 1 and (onde2.pos - posDetec).mag < 1):
        if abs(dot(onde1.pos, vector(1, 0, 0)) - longH / 2) <= dx:
            onde1.dir = -onde1.dir
            onde1.avance = -onde1.avance
        if abs(dot(onde1.pos, vector(1, 0, 0))) <= dx and onde1.avance == -1:
            onde1.vertical = True
            onde1.dir = vector(0, -dx, 0)
        if abs(dot(onde2.pos, vector(1, 0, 0))) <= dx and not onde2.vertical:
            onde2.vertical = True
            onde2.dir = vector(0, dx, 0)
        if abs(dot(onde2.pos, vector(0, 1, 0)) - longV / 2) <= dx:
            onde2.dir = vector(0, -dx, 0)
            onde2.avance = -onde2.avance
        t += dt
        if (onde1.pos - posDetec).mag > 1:
            onde1.update(t)
        if (onde2.pos - posDetec).mag > 1:
            onde2.update(t)

def lancer_animation_onde():
    for o in ondes:
        o.sphere.clear_trail()
        o.sphere.visible = False
    ondes.clear()
    onde1 = onde(posSource, vector(dx, 0, 0), color.blue, amplitude, frequence)
    onde2 = onde(posSource, vector(dx, 0, 0), color.red, amplitude, frequence)
    ondes.append(onde1)
    ondes.append(onde2)
    animer_onde(onde1, onde2)

def boucle_particules():
    while True:
        rate(100)
        majParticules()

# === Interface ===

# === Interface (Sliders au-dessus de la scène) ===

wtext(text="<b>Vitesse par rapport à l'ether (entre 0 et 1)</b><br>", pos=scene.caption_anchor )
eInput = winput(bind=majVitesse, text="0.0", type="numeric", pos=scene.caption_anchor )
eTexteSlider = wtext(text=" c", pos=scene.caption_anchor )
wtext(text="<br><br>", pos=scene.pos=scene.caption_anchor )

wtext(text="<b>Orientation de l'ether (entre 0 et 2)</b><br>", pos=scene.caption_anchor )
oeInput = winput(bind=majOrientation, text="0.0", type="numeric", pos=scene.caption_anchor )
oeTexteSlider = wtext(text=" Pi", pos=scene.caption_anchor )
wtext(text="<br><br>", pos=scene.caption_anchor )

wtext(text="<b>Différence de longueur (entre -5 et 5)</b><br>", pos=scene.caption_anchor )
bhInput = winput(bind=majDeltaL, text="0", type="numeric", pos=scene.caption_anchor )
bhTexteSlider = wtext(text=" λ/4 ", pos=scene.caption_anchor )
wtext(text="<br><br>", pos=scene.caption_anchor )


# === Objets de la scène ===

ventEther = arrow(pos=vector(-longH / 2, longV / 2, 0),
                  axis=vector(1, 0, 0),
                  color=color.cyan,
                  shaftwidth=0.3)
source = sphere(pos=posSource, color=color.red)
miroirH = box(pos=vector(longH / 2, 0, 0), size=vector(0.1, 4, 4), axis=vector(1, 0, 0), opacity=0.8)
miroirV = box(pos=vector(0, longV / 2, 0), size=vector(0.1, 4, 4), axis=vector(0, 1, 0), opacity=0.8)
splitteur = box(size=vector(0.1, 4, 4), axis=vector(1, -1, 0), opacity=0.8)
detecteur = box(pos=posDetec, size=vector(3, 2, 2), axis=vector(0, 1, 0), color=color.white)

# === Franges d'interférence ===

graph1 = graph(title="Intensité normalisée selon la distance sur le détecteur",
               xtitle="Position sur l'écran (m)", ytitle="I/I_max",
               width=600, height=400)

graph1.align='right'

courbe = gcurve(color=color.blue)
button(bind=dupliquerCourbe, text="Garder en mémoire",pos=scene.caption_anchor)

# === Lancement initial ===

ajoutParticules(20, 0.5)
majInterference()
lancer_animation_onde()
boucle_particules()


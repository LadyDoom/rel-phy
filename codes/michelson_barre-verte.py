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

vEther = 0.0001
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
marqueur_pic = None
derniere_position_pic = None
position_pic_reference = None
position_pic_reference_visible = None
marqueurs_pics_stockes = []
ordre_pic_suivi = None

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
        return self.amplitude*exp(-2) * sin(self.k * coord - self.avance * self.omega * t + self.dephasage)

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
    longH = longV + deltaL * (longOnde / 4)
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

def find_principal_peak():
    """Track one fringe continuously: initialize on the peak nearest plot center, then keep same fringe order."""
    global ordre_pic_suivi
    d0 = abs(longH - longV)
    alpha = 0.1
    t1 = temps(longV, orientation + 1 / 2)
    t2 = temps(longH, orientation)
    delta_phi = (2 * pi * (t1 - t2) * c) / lamb
    
    # Phase model: arg(i) = (2*pi/5) * (alpha*i + d0) + delta_phi
    # Peaks of cos^2 happen when arg(i) = n*pi.
    phase0 = (2 * pi / 5) * d0 + delta_phi
    slope = (2 * pi / 5) * alpha

    # Initialize tracked order to the peak nearest the center of the plot (i ~= 50)
    if ordre_pic_suivi is None:
        i_centre = 50
        phase_centre = phase0 + slope * i_centre
        ordre_pic_suivi = int(round(phase_centre / pi))

    # Keep this same fringe order continuously (can move outside [0, 99])
    peak_position = (ordre_pic_suivi * pi - phase0) / slope
    
    return peak_position, delta_phi

def majInterference():
    global courbe, marqueur_pic, derniere_position_pic, position_pic_reference, position_pic_reference_visible
    courbe.delete()
    if marqueur_pic is not None:
        marqueur_pic.delete()
    
    d0 = abs(longH - longV)
    alpha = 0.1
    t1 = temps(longV, orientation + 1 / 2)
    t2 = temps(longH, orientation)
    delta_phi = (2 * pi * (t1 - t2) * c) / lamb
    
    for i in range(0, 100):
        courbe.plot(i, cos((2 * pi / 5) * (i * alpha + d0) + delta_phi) ** 2)
    
    # Ajouter un marqueur pour le pic principal
    peak_pos, _ = find_principal_peak()
    periode_frange_m = 5 / (2 * alpha)
    
    # Initialiser la référence au premier appel (position continue, pas visible)
    if position_pic_reference is None:
        position_pic_reference = peak_pos
    
    # Calculer le déplacement dans l'espace continu
    deplacement_continu = peak_pos - position_pic_reference
    
    # Ramener le déplacement dans [-periode/2, periode/2) pour l'affichage
    deplacement_m = ((deplacement_continu + periode_frange_m / 2) % periode_frange_m) - periode_frange_m / 2
    
    # Position visible du pic: référence + déplacement (modulo pour rester dans [0, 99])
    if position_pic_reference_visible is None:
        # Au premier appel, placer la référence visible au milieu
        peak_pos_visible = peak_pos
        while peak_pos_visible < 0:
            peak_pos_visible += periode_frange_m
        while peak_pos_visible > 99:
            peak_pos_visible -= periode_frange_m
        position_pic_reference_visible = peak_pos_visible
    
    # Calculer la position visible à partir de la référence visible + déplacement
    peak_pos_visible = position_pic_reference_visible + deplacement_m
    
    # Ramener dans [0, 99] si nécessaire
    while peak_pos_visible < 0:
        peak_pos_visible += periode_frange_m
    while peak_pos_visible > 99:
        peak_pos_visible -= periode_frange_m

    marqueur_pic = gvbars(delta=0.5, color=color.green)
    if 0 <= peak_pos_visible <= 99:
        marqueur_pic.plot(peak_pos_visible, 1.05)
    
    # Mettre à jour le texte de déplacement du pic
    texte_deplacement_pic.text = f"Déplacement du pic: {deplacement_m:.2f} m"
    
    derniere_position_pic = peak_pos


def dupliquerCourbe():
    global compteur_fig, position_pic_reference, position_pic_reference_visible, ordre_pic_suivi
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
    
    # Recenter tracked fringe to middle-peak for current pattern before saving
    ordre_pic_suivi = None

    # Also save the peak marker with the same color
    peak_pos, _ = find_principal_peak()
    periode_frange_m = 5 / (2 * alpha)
    # Le pic doit être proche du centre après recentrage
    peak_pos_visible = peak_pos
    while peak_pos_visible < 0:
        peak_pos_visible += periode_frange_m
    while peak_pos_visible > 99:
        peak_pos_visible -= periode_frange_m

    marqueur_snapshot = gvbars(delta=0.5, color=couleur)
    if 0 <= peak_pos_visible <= 99:
        marqueur_snapshot.plot(peak_pos_visible, 1.05)
    marqueurs_pics_stockes.append(marqueur_snapshot)
    
    # Reset reference to current peak position for next measurements
    position_pic_reference = peak_pos
    position_pic_reference_visible = peak_pos_visible

    # Refresh live marker/text immediately with the newly-centered tracked peak
    majInterference()

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
texte_deplacement_pic = wtext(text="Déplacement du pic: 0.00 m", pos=scene.caption_anchor)
wtext(text="<br>", pos=scene.caption_anchor)
button(bind=dupliquerCourbe, text="Garder en mémoire",pos=scene.caption_anchor)

# === Lancement initial ===

ajoutParticules(20, 0.5)
majInterference()
lancer_animation_onde()
boucle_particules()


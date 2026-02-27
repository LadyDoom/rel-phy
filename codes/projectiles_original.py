Web VPython 3.2
# Constantes
grille_dessinee = False
#scene.lights = []
#scene.ambient = color.gray(0.6) 
scalaireFleche = 50
dt          = 0.01
tailleSol   = 1000
trajFin     = False
pas=100
G = 6.67430e-11
r_planete = vec(0,0,0)

boules_ind = []


scene.width  = 600
scene.height = 600
scene.align  = 'left'

# Objets créés/masqués à chaque lancement ; initialisés à None
balle = forceAzimutale = forceCoriolis = forceCentrifuge = plancher = cible = cibleRouge = None


#dictionnaire pour changer les couleurs
couleurs_force = {'coriolis':   color.green,'azimutal':   color.orange,'centrifuge': color.red}

scene.up       = vector(0, 0, 1)
scene.forward  = vector(0, -1, -0.3)


tempAzimutal = 0
tempCoriolis = 0
tempCentrifuge = 0

tabCoriolis = None
courbeCoriolis = None
courbeAzimutal = None
courbeCentrifuge = None

vectAzimutal   = vec(0,0,0)
vectCoriolis   = vec(0,0,0)
vectCentrifuge = vec(0,0,0)
cibleRougePos = 0

t=0
m = 1
R = 2
w = vec(0.0, 0.00, 0.005)       
w_avant = w
r = vec(1, 0, 0)*R
r_avant = r
g = vec(0, 0, -10)





# Interface utilisateur
scene.caption = ""

RInput   = winput(bind=test, prompt=" Rayon planète R (m) : ",   text="6.371e6"); scene.append_to_caption("\n")
MInput   = winput(bind=test, prompt=" Masse planète M (kg) : ",  text="5.972e24"); scene.append_to_caption("\n")
omegaInput   = winput(bind=test, prompt=" Vitesse ang. Ω (rad/s) : ", text="7.292e-5"); scene.append_to_caption("\n")

scene.append_to_caption("\n")

latInput = winput(bind=test, prompt=" Colatitude labo φ (deg) : ", text="45");      scene.append_to_caption("\n")

posInput = winput(bind=test, prompt=" Position init. (x,y,z) : ", text="10,10,0"); scene.append_to_caption("\n")
impInput = winput(bind=test, prompt=" Vitesse init. (u,ϕ,θ) : ",  text="52, 0, 45"); scene.append_to_caption("\n")

scene.append_to_caption("\n")

cibleInput = winput(bind=test, prompt=" Position cible (x,y,z) : ",text="20,20,0"); scene.append_to_caption("\n")

startButton = button(text="Commencer", bind=start)

# Forces sup
scene.append_to_caption("\n\n<b>Forces à inclure :</b>\n")
cbCentrifuge  = checkbox(bind=test,text="Centrifuge",  checked=True);  scene.append_to_caption("  ")
cbCoriolis    = checkbox(bind=test,text="Coriolis",    checked=True);  scene.append_to_caption("   ")
cbAzimutal    = checkbox(bind=test,text="Azimutale",   checked=True);  scene.append_to_caption("   ")


for objet in (RInput, MInput, latInput, omegaInput,posInput, impInput,cibleInput, startButton):
    objet.display=scene

# Fonctions utilitaires
for obj in scene.objects:
    if hasattr(obj, "shininess"):
        obj.shininess = 0

def effacer():
    global boules_ind, balle, forceAzimutale, forceCoriolis, forceCentrifuge, plancher, cible, cibleRouge
    global tabCoriolis, courbeCoriolis, courbeAzimutal, courbeCentrifuge

    # Balle principale
    if balle is not None:
        balle.clear_trail()
        balle.visible = False

    # Boules individuelles
    for b, _ in boules_ind:
        b.clear_trail()
        b.visible = False
    boules_ind.clear()        # vide la liste, inplace

    for c in (courbeCoriolis, courbeAzimutal, courbeCentrifuge):
        if c is not None:
            c.delete()
    courbeCoriolis = courbeAzimutal = courbeCentrifuge = None

    # Flèches, sol, cibles
    for obj in (forceAzimutale, forceCoriolis, forceCentrifuge, plancher, cible, cibleRouge):
        if obj is not None:
            obj.visible = False

    if tabCoriolis is not None:
        tabCoriolis.delete()
        tabCoriolis = None
        
        
def spheACartOld(spherique):
    
    r = spherique.z
    phi = spherique.y
    theta = spherique.x
    
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return vec(x, y, z)
    
def spheACart(spherique):
    # spherique = vec(u, phi, theta)
    u     = spherique.x
    phi   = spherique.y
    theta = spherique.z
    x = u * sin(theta) * cos(phi)
    y = u * sin(theta) * sin(phi)
    z = u * cos(theta)
    return vec(x, y, z)


def dessinerGrille(pas):
    demi  = tailleSol / 2
    zlvl  = 0.51                  # légerement au-dessus du plancher
    Laxe  = demi                  # longueur visible des axes
    epais = 0.2                   # épaisseur des flèches

    # ───── flèches cardinales ─────
    # Est (+x) / Ouest (-x)
    arrow(pos=vec(0,0,zlvl), axis=vec( Laxe, 0, 0), shaftwidth=epais, color=color.red)
    arrow(pos=vec(0,0,zlvl), axis=vec(-Laxe, 0, 0), shaftwidth=epais, color=color.red)
    label(pos=vec( Laxe+1, 0, zlvl), text='E',  box=False, height=12, color=color.red)
    label(pos=vec(-Laxe-2,0, zlvl), text='O',  box=False, height=12, color=color.red)

    # Nord (+y) / Sud (-y)
    arrow(pos=vec(0,0,zlvl), axis=vec(0, Laxe, 0), shaftwidth=epais, color=color.green)
    arrow(pos=vec(0,0,zlvl), axis=vec(0,-Laxe, 0), shaftwidth=epais, color=color.green)
    label(pos=vec(0, Laxe+1, zlvl), text='N',  box=False, height=12, color=color.green)
    label(pos=vec(0,-Laxe-2, zlvl), text='S',  box=False, height=12, color=color.green)

    # Haut (+z)
    arrow(pos=vec(0,0,0),    axis=vec(0,0,Laxe), shaftwidth=epais*10, color=color.blue)
    label(pos=vec(0,0,Laxe+1), text='Haut', box=False, height=12, color=color.blue)

    # ───── grille (lignes grises) ─────
    k = 0.0
    while k <= demi + 1e-6:
        # lignes verticales x = ±k
        curve(pos=[vec( k, -demi, zlvl), vec( k,  demi, zlvl)], color=color.gray(0.7))
        if k > 1e-6:   # évite doublon, car k=0 déjà tracé
            curve(pos=[vec(-k,-demi, zlvl), vec(-k, demi, zlvl)], color=color.gray(0.7))

        # lignes horizontales y = ±k
        curve(pos=[vec(-demi,  k, zlvl), vec( demi,  k, zlvl)], color=color.gray(0.7))
        if k > 1e-6:
            curve(pos=[vec(-demi,-k, zlvl), vec( demi,-k, zlvl)], color=color.gray(0.7))

        k += pas



def test():
    pass

def parseVec(s):
    return vec(*[float(x.strip()) for x in s.split(",")])

def afficherFleche(F):
    if mag(F) < 1e-9:
        return vec(0,0,0)
    return norm(F)*scalaireFleche

def ajouter_boule_force(force):
    b = sphere(pos=positionInitiale,radius=0.06,color=couleurs_force[force],make_trail=True,trail_color=couleurs_force[force])
    b.vitesse = impulsionInitiale
    boules_ind.append((b, {force}))

def start(b):
    global m, R, w, g, r_planete, cibleRougePos
    global balle, forceAzimutale, forceCoriolis, forceCentrifuge
    global positionInitiale, impulsionInitiale, plancher, trajFin
    global cible, cibleRouge
    global grille_dessinee
    global t
    global tabCoriolis, courbeCoriolis, courbeAzimutal, courbeCentrifuge


    effacer()
    t = 0.0
    
    
    
    # Tableaux des forces

    tabCoriolis = graph(title='Magnitude de la force coriolis', xtitle='t', ytitle='N',align='right')

    courbeCentrifuge = gcurve(graph=tabCoriolis, label='|F_centri|',color=couleurs_force['centrifuge'])

    courbeCoriolis = gcurve(graph=tabCoriolis, label='|F_cor|',color=couleurs_force['coriolis'])


    #tabAzimutal = graph(title='Magnitude de la force azimutal', xtitle='t', ytitle='N',align='right')

    courbeAzimutal = gcurve(graph=tabCoriolis, label='|F_azi|',color=couleurs_force['azimutal'])

    #tabCentrifuge = graph(title='Magnitude de la force centrifuge', xtitle='t', ytitle='N',align='right')

    
    # lecture des données
    R = float(RInput.text)                 # rayon planète
    M = float(MInput.text)                 # masse planète
    lat_deg = 90-float(latInput.text)         # latitude du labo
    omega   = float(omegaInput.text)           # vecteur de la rotation (rad/s)

    lat_rad = radians(lat_deg)

    # On construit w avec la latitude (longitude sera 0)
    w = vec(0, omega*cos(lat_rad), omega*sin(lat_rad))
    w_avant=w
    w=majW(w)
    # gravité de la planète
    g_mag = G * M / R**2
    g = vec(0, 0, -g_mag)

    # position du laboratoire sur la terre
    #r_planete = vec(R*cos(lat_rad), 0, R*sin(lat_rad))
    r_planete = vec(0, 0, R)
    




    positionInitiale  = parseVec(posInput.text)
    temp = parseVec(impInput.text)
    
    impulsionInitiale = spheACart(vec(temp.x,radians(temp.y),radians(temp.z)))


    # Sol 
    plancher = box(pos=vec(0,0,0), length=tailleSol, height=tailleSol, width=1, color=color.white,opacity=0.4)
    
    if not grille_dessinee:
        dessinerGrille(pas)
        grille_dessinee = True
    
    # Création du trajet total
    balle = sphere(pos=positionInitiale, radius=0.1, color=color.magenta, make_trail=True)
    
    
    # Création des autres trajets

    if cbCentrifuge.checked: 
        ajouter_boule_force('centrifuge')
    if cbCoriolis.checked:  
        ajouter_boule_force('coriolis')
    if cbAzimutal.checked:   
        ajouter_boule_force('azimutal')
    
    
    
    balle.vitesse = impulsionInitiale

    forceAzimutale  = arrow(shaftwidth=1, color=color.orange)
    forceCoriolis   = arrow(shaftwidth=1, color=color.green)
    forceCentrifuge = arrow(shaftwidth=1, color=color.red)
    


    # Cible naive
    x0, y0, z0      = balle.pos.x, balle.pos.y, balle.pos.z
    vx0, vy0, vz0   = balle.vitesse.x, balle.vitesse.y, balle.vitesse.z
    grav = abs(g.z)
    temps = (vz0 + sqrt(vz0**2 + 2*grav*z0)) / grav
    xf, yf = vx0*temps, vy0*temps
    cible = sphere(pos=vec(x0+xf, y0+yf, 0), radius=5, color=color.blue)
    
    # Cible arbitraire
    cibleRougePos = parseVec(cibleInput.text)
    cibleRouge = sphere(pos=cibleRougePos, radius=5, color=color.red)


    # On centre la caméra
    scene.center   = (balle.pos+cible.pos)/2
    scene.range = mag((balle.pos+cible.pos))

    
    trajFin = False
    while not trajFin:
        rate(150)
        majVariables()
        majVisuel()
        t += dt
    print(f"Le projectile a touché le sol au point {balle.pos}")
    print(f"La cible était au point {cibleRougePos}")
    distance = mag(balle.pos - cibleRougePos)
    print(f"Vous l'avez manqué de {distance:.2f} m")
    
def majW(w):
    
    return w

def majVariables():
    global balle, trajFin, vectAzimutal, vectCoriolis, vectCentrifuge
    global r, w, r_avant, w_avant, r_planete

    r = r_planete + balle.pos  # le r 
    v = balle.vitesse
    dw = (w - w_avant)/dt

    vectAzimutal   = 0*m*cross(r, dw)
    vectCoriolis   = 2*m*cross(v, w)
    vectCentrifuge = m*cross(cross(w, r), w)

    a = g + vectCoriolis + vectCentrifuge + vectAzimutal
    balle.vitesse += a*dt
    balle.pos     += balle.vitesse*dt
    
    
    # Maj des autres trajets
    for b, ens in boules_ind:
        r_i  = r_planete + b.pos
        v_i  = b.vitesse
        dw_i = (w - w_avant)/dt

        az_i  = 0*m*cross(r_i, dw_i)
        cor_i = 2*m*cross(v_i, w)
        cen_i = m*cross(cross(w, r_i), w)

        a_i = g
        if 'azimutal'   in ens:
            a_i += az_i
        if 'coriolis'   in ens: 
            a_i += cor_i
        if 'centrifuge' in ens: 
            a_i += cen_i

        b.vitesse += a_i*dt
        b.pos     += b.vitesse*dt
    
    if balle.pos.z <= 0:      # contact sol
        trajFin = True

    r_avant, w_avant = r, w

def majVisuel():
    global tabCoriolis
    tempAzimutal = mag(vectAzimutal)
    tempCoriolis = mag(vectCoriolis)
    tempCentrifuge = mag(vectCentrifuge)
    
    courbeCoriolis.plot(t, tempCoriolis)    
    courbeAzimutal.plot(t, tempAzimutal)    
    courbeCentrifuge.plot(t, tempCentrifuge)    
    
    scene.center   = (balle.pos+cible.pos)/2
    scene.range = mag((balle.pos+cible.pos))
    
    forceAzimutale.axis  = afficherFleche(vectAzimutal)
    forceCoriolis.axis   = afficherFleche(vectCoriolis)
    forceCentrifuge.axis = afficherFleche(vectCentrifuge)
    
    

    for fleche in (forceAzimutale, forceCoriolis, forceCentrifuge):
        fleche.pos = balle.pos

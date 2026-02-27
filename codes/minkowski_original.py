from vpython import *

# === Fonctions utilitaires ===
def test():
    pass

############### Variables globales
counter = 0
tempVitesse = 0.5
objVitesse = tempVitesse
min_x = 0
max_x = 0
hauteur = 0
profondeur =0
écart = 0
modeAjout=True
# Variables pour tracer une ligne entre clic et relâchement
debutLigne = None
clicEnCours = False
###############################################
scene.visible=False
#scene.background = vector(0.652, 0.791, 0.966)
scene.background = color.black
scene.align = 'left'
pointeurSouris = None

tempDel=[]
tempDelBase=[]
objetsMagenta = []

for obj in scene.objects:          # everything currently in the scene
    if hasattr(obj, "shininess"):  # spheres, boxes, arrows, curves…
        obj.shininess = 0

# === Entrée utilisateur (interface initiale) ===
scene.caption = ""


tempTitre = wtext(text="<b>Paramètres</b><br>", pos=scene.title_anchor)

#wtext(text="<br>", pos=scene.title_anchor)

min_label = wtext(text=" Min x: ", pos=scene.title_anchor)
minInput = winput(bind=test,text="0", type="numeric", pos=scene.title_anchor)
#wtext(text="<br>", pos=scene.title_anchor) 

max_label = wtext(text=" Max x: ", pos=scene.title_anchor)
maxInput = winput(bind=test,text="20", type="numeric", pos=scene.title_anchor)
#wtext(text="<br>", pos=scene.title_anchor)

h_label = wtext(text=" Max y: ", pos=scene.title_anchor)
hInput = winput(bind=test,text="20", type="numeric", pos=scene.title_anchor)
#wtext(text="<br>", pos=scene.title_anchor)

p_label = wtext(text=" Min y: ", pos=scene.title_anchor)
pInput = winput(bind=test,text="0", type="numeric", pos=scene.title_anchor)
#wtext(text="<br>", pos=scene.title_anchor)


e_label = wtext(text=" Écart: ", pos=scene.title_anchor)
eInput = winput(bind=test,text="2", type="numeric", pos=scene.title_anchor)

wtext(text="<br><br>", pos=scene.title_anchor)
####################################################


tempTag = wtext(text="<b></b><br>", pos=scene.title_anchor)

v_label = wtext(text="Vitesse de l'observateur : ", pos=scene.title_anchor)
sVitesse = slider(min=-0.99, max=0.99, value=0.5, step=0.01, length=200, bind=majVitesseSlider, pos=scene.title_anchor)
txtVitesse = wtext(text=" (v = 0.5 c)", pos=scene.title_anchor)

wtext(text="<br><br>", pos=scene.title_anchor)




start_button = button(bind=lancer_diagramme,text="Créer le diagramme", pos=scene.title_anchor)
wtext(text="<br><br>", pos=scene.title_anchor)


#####################################################################################################
def br():
    wtext(text="<br>", pos=scene.title_anchor)
def creer_ui_secondaire():
    global acheck, rcheck, bcheck, cMagenta
    global sObjet, txtVitesseObjet
    global x_label, xInput, ct_label, ctInput, x2_label, ct2_label, x2Input, ct2Input, tempTag
    global ajoutBouton, bouton_supprimer, modeEntree
    global boutonSegment


    tempTag.text="<b>Vitesse de l'observateur</b><br>"

    wtext(text="<b>Affichages</b>", pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)

    acheck = checkbox(bind=ajoutCheck, text="Ajouter des objets", checked=True, pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)

    rcheck = checkbox(bind=cacherRef, text="Afficher le référentiel en mouvement", checked=True, pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)

    bcheck = checkbox(bind=cacherRefBase, text="Afficher le référentiel stationnaire", checked=True, pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)

    cMagenta = checkbox(bind=retirerObjet, text="Afficher les objets", checked=True, pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.title_anchor)

    wtext(text="<b>Vitesse de l'objet</b>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    #wtext(text="Vitesse de l'objet à placer :", pos=scene.title_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    sObjet = slider(min=-1, max=1, value=0.5, length=200, bind=majObjVitesse, pos=scene.caption_anchor)
    txtVitesseObjet = wtext(text=" (v = 0.5 c)", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    wtext(text="<b> Ajouter un point par coordonnées</b>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    x_label = wtext(text=" x :    ", pos=scene.caption_anchor)
    xInput  = winput(bind=test, type="numeric", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    ct_label = wtext(text=" ct :   ", pos=scene.caption_anchor)
    ctInput  = winput(bind=test, type="numeric", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    x2_label = wtext(text=" x2 :  ", pos=scene.caption_anchor)
    x2Input  = winput(bind=test, type="numeric", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    ct2_label = wtext(text=" ct2 : ", pos=scene.caption_anchor)
    ct2Input  = winput(bind=test, type="numeric", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    ajoutBouton = button(text="Ajouter le point", bind=ajouter_point_manuellement, pos=scene.caption_anchor)

    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)
    
    boutonSegment = button(text="Tracer segment", bind=ajouter_segment_manuellement, pos=scene.caption_anchor)

    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    
    bouton_supprimer = button(text="Supprimer le dernier élément", bind=supprimer_dernier_objet, pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)

    modeEntree = checkbox(bind=changer_mode_entree,
                          text="Entrée dans le référentiel en mouvement (x', ct')",
                          checked=False,
                          pos=scene.caption_anchor)
    wtext(text="<br>", pos=scene.caption_anchor)


def supprimer_dernier_objet(b):
    if len(objetsMagenta) >= 2:
        objetsMagenta[-1].visible = False
        objetsMagenta[-2].visible = False
        objetsMagenta.pop()
        objetsMagenta.pop()

def changer_mode_entree(ev):
    global x_label,ct_label,x2_label,ct2_label
    if ev.checked:
        x_label.text = " x' :    "
        ct_label.text = " ct' :   "
        x2_label.text = " x2' :  "
        ct2_label.text = " ct2' : "
    else:
        x_label.text = " x :    "
        ct_label.text = " ct :   "
        x2_label.text = " x2 :  "
        ct2_label.text = " ct2 : "
# === Initialisation des flèches
def ajouter_segment_manuellementt(b):
    global x2_label, x2Input, ct2_label, ct2Input

    try:
        # Lecture des deux points
        x1  = float(xInput.text)
        ct1 = float(ctInput.text)
        x2  = float(x2Input.text)
        ct2 = float(ct2Input.text)
    except ValueError:
        print("Entrées invalides.")
        return

    p1 = coord_vers_vec(x1,  ct1)
    p2 = coord_vers_vec(x2,  ct2)

def ajouter_segment_manuellement(b):
    try:
        x1  = float(xInput.text)
        ct1 = float(ctInput.text)
        x2  = float(x2Input.text)
        ct2 = float(ct2Input.text)
    except:
        print("Entrées invalides.")
        return

    p1 = coord_vers_vec(x1, ct1)
    p2 = coord_vers_vec(x2, ct2)

    # tracer directement le segment (2 points suffisent)
    seg = curve(pos=[p1, p2], radius=0.06, color=color.magenta)
    objetsMagenta.append(seg)

    # petites lignes d’univers translucides au long du segment (optionnel)
    n = 5
    direction = norm(vec(objVitesse, 1, 0))
    for i in range(n + 1):
        t = i / n
        point = p1 * (1 - t) + p2 * t
        cyl = cylinder(pos=point, axis=direction * 20, radius=0.8, color=color.magenta, opacity=0.15)
        objetsMagenta.append(cyl)


    # revoir TODO
    ligne = curve(radius=0.05, color=color.magenta)
    objetsMagenta.append(ligne)

    n = 5
    for i in range(n + 1):
        t = i / n
        point = p1 * (1 - t) + p2 * t
        ligne.append(pos=point)

        direction = norm(vec(objVitesse, 1, 0))
        cyl = cylinder(pos=point, axis=direction * 20,
                       radius=1, color=color.magenta, opacity=0.1)
        objetsMagenta.append(cyl)

def coord_vers_vec(x, ct):
    """Retourne un vec(x,ct,0) ou la projection (x',ct') selon modeEntree."""
    if modeEntree.checked:
        u_xp  = norm(vec(1 / tempVitesse, 1, 0))
        u_ctp = norm(vec(    tempVitesse, 1, 0))
        return x * u_xp + ct * u_ctp
    else:
        return vec(x, ct, 0)


def ajouter_point_manuellement(b):
    try:
        x = float(xInput.text)
        ct = float(ctInput.text)

        if modeEntree.checked:
            # Mode (x', ct') — projection géométrique
            u_xp = norm(vec(1 / tempVitesse, 1, 0))
            u_ctp = norm(vec(tempVitesse, 1, 0))
            position = x * u_xp + ct * u_ctp
        else:
            position = vec(x, ct, 0)

        sph = sphere(pos=position, radius=0.3, color=color.magenta)
        objetsMagenta.append(sph)

        direction = norm(vec(objVitesse, 1, 0))
        cyl = cylinder(pos=position, axis=direction * 18, color=color.red, radius=0.07)
        objetsMagenta.append(cyl)
    except ValueError:
        print("Entrées invalides.")




def retirerObjet(ev):
    if ev.checked:
        for o in objetsMagenta:
            o.visible = True
    else:
        for o in objetsMagenta:
            o.visible = False
            
def cacherRef(ev):
    if ev.checked==False:
        for elem in tempDel:
            elem.visible=False
    else:
        dessiner_obv(min_x, max_x, hauteur, écart)

def cacherRefBase(ev):
    if ev.checked==False:
        for elem in tempDelBase:
            elem.visible=False
    else:
        dessiner_plan_cartesien(min_x, max_x, hauteur, écart)


def majObjVitesse():
    global objVitesse
    objVitesse=sObjet.value
    txtVitesseObjet.text = " (v = " + str(round(objVitesse, 2)) + " c)"

def majVitesseSlider():
    global tempVitesse
    tempVitesse = sVitesse.value
    txtVitesse.text = " (v = " + str(round(tempVitesse, 3)) + " c)"
    
    for elem in tempDel:
        elem.visible = False
    dessiner_obv(min_x, max_x, hauteur, écart)

def majVitesse(ev):
    global tempVitesse
    tempVitesse =float(vInput.text)
    for elem in tempDel:
        elem.visible=False
    #print(tempDel)
    dessiner_obv(min_x, max_x, hauteur, écart)

def decomposer_position(evt):
    global pointeurSouris
    # Projeter la position de la souris sur le plan XY
    position = scene.mouse.project(normal=vec(0, 0, 1), point=vec(0, 0, 0))
    if position is None:
        return

    position.z = 0.2
    pointeurSouris.pos = position
    pointeurSouris.visible = True

    # Mettre à jour la flèche x (de (0,0) à (x,0))
    fleche_x.pos = vec(0, 0, 0)
    fleche_x.axis = vec(position.x, 0, 0)

    # Mettre à jour la flèche y (de (0,0) à (0,y))
    fleche_y.pos = vec(0, 0, 0)
    fleche_y.axis = vec(0, position.y, 0)
    
    temp = (position.y-position.x*tempVitesse)/(1/tempVitesse-tempVitesse)
    fleche_yobv.pos = vec(0, 0, 0)
    fleche_yobv.axis = vec(temp,temp*1/tempVitesse , 0)

    

    temp = (position.y-position.x*1/tempVitesse)/(tempVitesse-1/tempVitesse)
    fleche_xobv.pos = vec(0, 0, 0)
    fleche_xobv.axis = vec(temp,temp*tempVitesse , 0)
    


# === Dessin du plan cartésien

def dessiner_plan_cartesien(min_x, max_x, hauteur, écart):
    scene.center = vec((min_x + max_x) / 2, (hauteur+profondeur) / 2, 0)
    
    #Axes
    arrow(pos=vec(0, 0, 0), axis=vec(min_x, 0, 0), shaftwidth=0.08, color=color.white)
    arrow(pos=vec(0, 0, 0), axis=vec(max_x, 0, 0), shaftwidth=0.08, color=color.white)
    arrow(pos=vec(0, 0, 0), axis=vec(0, hauteur, 0), shaftwidth=0.08, color=color.white)

    label(pos=vec(max_x, 0, 0), text="x", xoffset=10, height=12, box=False, color=color.red)
    label(pos=vec(0, hauteur, 0), text="ct", yoffset=10, height=12, box=False, color=color.green)
    
    
    #Lignes verticales
    x = 0
    while x < max_x:
        t=cylinder(pos=vec(x, 0, 0), axis=vec(0, hauteur, 0), radius=0.05, color=color.gray(0.8))
        tempDelBase.append(t)
        if profondeur <0:
            t=cylinder(pos=vec(x, 0, 0), axis=vec(0, -hauteur, 0), radius=0.05, color=color.gray(0.8))
            tempDelBase.append(t)

        
        x += écart
    x = -écart
    while x > min_x:
        t=cylinder(pos=vec(x, 0, 0), axis=vec(0, hauteur, 0), radius=0.05, color=color.gray(0.8))
        tempDelBase.append(t)
        if profondeur <0:
            t=cylinder(pos=vec(x, 0, 0), axis=vec(0, -hauteur, 0), radius=0.05, color=color.gray(0.8))
            tempDelBase.append(t)
            x -= écart
        
    y = 0

    while y <= hauteur:
        t=cylinder(pos=vec(0, y, 0), axis=vec(max_x - 2, 0, 0), radius=0.05, color=color.gray(0.8))
        tempDelBase.append(t)
        t=cylinder(pos=vec(0, y, 0), axis=vec(min_x + 2, 0, 0), radius=0.05, color=color.gray(0.8))
        tempDelBase.append(t)

        y += écart
    
    if profondeur <0:
        y = -écart
        while y >= profondeur - 1:
            t=cylinder(pos=vec(0, y, 0), axis=vec(max_x - 2, 0, 0), radius=0.05, color=color.gray(0.8))
            tempDelBase.append(t)
            t=cylinder(pos=vec(0, y, 0), axis=vec(min_x + 2, 0, 0), radius=0.05, color=color.gray(0.8))
            tempDelBase.append(t)
        
            y -= écart

def getAngle(vit):
    return pi/2-atan(vit)

def dessiner_obv(min_x, max_x, hauteur, écart):
    scene.center = vec((min_x + max_x) / 2, hauteur / 2, 2)
    

    
    t=arrow(pos=vec(0, 0, 0), axis=norm(vec((1/tempVitesse), 1, 0))*max_x/cos(pi/2-getAngle(tempVitesse)), shaftwidth=0.1, color=color.purple)
    tempDel.append(t)
    
    t=arrow(pos=vec(0, 0, 0), axis=norm(vec(tempVitesse, 1, 0))*hauteur/abs(cos(getAngle(1/tempVitesse))), shaftwidth=0.1, color=color.purple)
    tempDel.append(t)
    
    
    
    if profondeur <0:
        t=arrow(pos=vec(0, 0, 0), axis=norm(vec(-(1/tempVitesse), -1, 0))*max_x/cos(pi/2-getAngle(tempVitesse)), shaftwidth=0.1, color=color.purple)
        tempDel.append(t)
        t=arrow(pos=vec(0, 0, 0), axis=norm(vec(-tempVitesse, -1, 0))*hauteur/(cos(getAngle(1/tempVitesse))), shaftwidth=0.1, color=color.purple)
        tempDel.append(t)
    
    t=label(pos=norm(vec((1/tempVitesse), 1, 0))*max_x/cos(pi/2-getAngle(tempVitesse)), text="x'", xoffset=10, height=12, box=False, color=color.red)
    tempDel.append(t)
    
    
    if tempVitesse>0:
        t=label(pos=norm(vec(tempVitesse, 1, 0))*hauteur/cos(getAngle(1/tempVitesse)), text="ct'", yoffset=10, height=12, box=False, color=color.green)
        tempDel.append(t)
        
    else:
        t=label(pos=norm(vec(tempVitesse, 1, 0))*hauteur/abs(cos(getAngle(1/tempVitesse))), text="ct'", yoffset=10, height=12, box=False, color=color.green)
        tempDel.append(t)
        
    
    #Lignes verticales
    x = 0
    while x < max_x and (x*tempVitesse)<max_x/2:

        if tempVitesse <0:
            t=cylinder(pos=vec(-x, -x*(tempVitesse), 0), axis=norm(vec((tempVitesse), 1, 0))*hauteur, radius=0.05, color=color.orange)
        else:
            t=cylinder(pos=vec(x, x*(tempVitesse), 0), axis=norm(vec((tempVitesse), 1, 0))*hauteur, radius=0.05, color=color.orange)  
        tempDel.append(t)
        if profondeur <0:
            
            if tempVitesse <0:
                t=cylinder(pos=vec(-x, -x*(tempVitesse), 0), axis=norm(vec( (tempVitesse),1, 0))*-hauteur, radius=0.05, color=color.orange)
            else:
                t=cylinder(pos=vec(x, x*(tempVitesse), 0), axis=norm(vec((tempVitesse), 1, 0))*hauteur, radius=0.05, color=color.orange)    
            tempDel.append(t)
        x += écart
    x = -écart
    #while x > min_x:
     #   cylinder(pos=vec(x, 0, 0), axis=norm(vec(-tempVitesse, 1, 0))*18, radius=0.05, color=color.gray(0.8))
      #  x -= écart
        
    y = 0

    while y <= hauteur - 1 and (y*tempVitesse)<hauteur/2:
        t=cylinder(pos=vec(y*tempVitesse, y, 0), axis=norm(vec((1/tempVitesse), 1, 0))*max_x, radius=0.05, color=color.orange)
        tempDel.append(t)
        if profondeur <0:
            t=cylinder(pos=vec(-y*tempVitesse, -y, 0), axis=norm(vec( (1/tempVitesse),1, 0))*-max_x, radius=0.05, color=color.orange)
            tempDel.append(t)
        y += écart
        
    

# Bouton de démarrage
def lancer_diagramme(bouton):
    global vslider,min_x,max_x,hauteur,écart,profondeur
    min_x = int(minInput.text)
    max_x = int(maxInput.text)
    hauteur = int(hInput.text)
    profondeur = int(pInput.text)
    écart = float(eInput.text)

    dessiner_plan_cartesien(min_x, max_x, hauteur, écart)
    dessiner_obv(min_x, max_x, hauteur, écart)
        
    # Cacher les éléments de l'interface
    for w in (tempTitre, min_label, minInput, max_label, maxInput,h_label, hInput, p_label, pInput, e_label, eInput,v_label, start_button):
        w.delete()

    scene.visible = True
    scene.caption = "<b> Diagramme de Minkowski </b>"
    #afficher nouveaux boutons
    creer_ui_secondaire()




# Ajoute un objet dans le plan
def ajoutObjet(evt):
    global counter
    counter += 1
    posObjet = scene.mouse.project(normal=vec(0, 0, 1), point=vec(0, 0, 0))

    t =sphere(pos=posObjet, radius=0.3, color=color.magenta)
    objetsMagenta.append(t)
    t =cylinder(pos=posObjet, axis=norm(vec(objVitesse, 1, 0))*18, color=color.red,radius=0.07)
    objetsMagenta.append(t)

    
def ajoutCheck(ev):
    global modeAjout
    modeAjout = ev.checked
    
def redirection():
    if not modeAjout:

        decomposer_position()

def redirection2():
    global debutLigne, clicEnCours
    if modeAjout:
        debutLigne = scene.mouse.project(normal=vec(0, 0, 1), point=vec(0, 0, 0))
        clicEnCours = True
    else:
        decomposer_position()
        
    
    
def relacherSouris(evt):
    global debutLigne, clicEnCours
    if modeAjout and clicEnCours and debutLigne is not None:
        finLigne = scene.mouse.project(normal=vec(0, 0, 1), point=vec(0, 0, 0))
        if finLigne is not None:
            distance = mag(finLigne - debutLigne)
            if distance < 0.2:
                # Clic court → ajout d’un objet
                ajoutObjet(evt)
            else:
                # Clic-glisser → tracer une ligne avec lignes d’univers
                ligne = curve(radius=0.05, color=color.magenta)
                objetsMagenta.append(ligne)

                n = 5
                for i in range(n + 1):
                    t = i / n
                    point = debutLigne * (1 - t) + finLigne * t
                    ligne.append(pos=point)
                    direction = norm(vec(objVitesse, 1, 0))
                    cyl=cylinder(pos=point, axis=direction * 20, radius=1, color=color.magenta, opacity=0.1)
                    objetsMagenta.append(cyl)

    debutLigne = None
    clicEnCours = False


############### Programme

pointeurSouris = sphere(
    pos=vec(0, 0, 0),
    radius=0.25,           
    color=color.yellow,
    shininess=0,
    visible=False
)


scene.bind('mousemove', redirection)
scene.bind('mousedown', redirection2)
scene.bind("mouseup", relacherSouris)



fleche_x = arrow(color=color.red, shaftwidth=0.15)
fleche_y = arrow(color=color.green, shaftwidth=0.15)

fleche_xobv = arrow(color=color.red, shaftwidth=0.15)
fleche_yobv = arrow(color=color.green, shaftwidth=0.15)



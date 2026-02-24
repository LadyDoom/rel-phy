Ce repo est une REL (Ressource Éducative Libre) qui consiste en un petit site Web qui contient trois activités interactives de visualisation et d’exploration en physique.

# Comment le repo fonctionne

**Sur la branche `master`**, on a les fichiers source — les `.qmd`, `_quarto.yml`, `images/`, `styles.css`. C'est là qu’on travaille et qu’on écrit le contenu.

**Sur la branche `gh-pages`**, on a les fichiers que Quarto a généré à partir des fichiers `.qmd` avec la commande `quarto publish gh-pages`.

Cette organisation en deux branches permet de s'assurer que la branche master est "propre" (ne contient que le code source, sans les fichiers générés automatiquement).

# Quel est le flux de travail

```jsx
On édite les .qmd en local (c'est du markdown)
      ↓
git add + commit + push sur master  → sauvegarde le code source
      ↓
quarto publish gh-pages  → render + push vers gh-pages (HTML généré)
      ↓
GitHub Action "pages build and deployment" se déclenche
      ↓
Site publié en ligne
```

# Comment les pages fonctionnent

## **Le point de départ : le code VPython**

L’animation est en VPython (le bloc `{python, eval=FALSE}` en bas de la page). C'est le code "lisible" qui est derrière l’animation, mais Quarto ne l'exécute pas (`eval=FALSE`), il l'affiche juste comme référence.

## **Ce que fait GlowScript**

VPython a un outil qui s'appelle **GlowScript** qui traduit automatiquement du code Python en JavaScript. C'est ce qu’on voit dans les grands blocs `{=html}`  — c'est le code Python **déjà converti en JavaScript** par GlowScript. Ce JavaScript est ce qui fait vraiment tourner l'animation dans le navigateur. Il peut être exporté directement depuis la page du projet sur le site de GlowScript via l’option “*Share or export this program***”.**

## **Le rôle de Quarto**

Quarto prend tout ça et génère une page HTML. Il y a deux choses distinctes dans les fichiers`.qmd` :

- Le bloc `{=html}` → injecté **tel quel** dans la page HTML finale, c'est l'animation interactive
- Le bloc `{python, eval=FALSE}` → affiché comme **code coloré** (syntax highlighting) uniquement, pour que le lecteur comprenne la logique

**Le flux complet :**

```
Le code a été produit sur glowscript.org
        ↓
GlowScript l'a traduit en JavaScript
        ↓
Ce JS a été collé dans un bloc {=html} dans le fichier .qmd
        ↓
Quarto génère le HTML final
        ↓
Le navigateur exécute le JS → animation 3D interactive
```

**En résumé**, Python n'est jamais vraiment exécuté ici — c'est une simulation 100% JavaScript dans le navigateur. Python est à la fois le langage de travail (plus lisible) et la documentation du code pour les lecteurs.

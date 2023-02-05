# Simulation d'écoulement de fluide autour d'un cylindre: utilisation de la méthode de Lattice-Boltzmann

La méthode de Lattice-Boltzmann est une alternative aux discrète aux méthodes classiques de CFD, telles que la résolution de la l'équation de Navier-Stokes.
Il s'agit non pas d'évaluer les équations de l'écoulement du fluide à l'échelle macroscopique, mais de modéliser des particules de fluide à l'échelle microscopique et mésoscopique sur un réseau, et d'en étudier la diffusion et leurs collisions.
L'intérêt de cette méthode réside en la limitation des degrés de liberté de chaque particule sur le réseau, amenant à une résolution plus aisée du système.

## Introductions aux équations générales de la méthode de Lattice-Boltzmann 

La méthode Lattice-Boltzmann est une méthode récente permettant la reproduction numérique du comportement complexe d'un fluide newtonien ou non newtonien. 
Contrairement à la méthode traditionnelle consistant en la résolution des équations de Navier-Stokes, cette méthode L-B constitue une alternative en discrétisant l'équation de Boltzmann. Elle consiste en l'étude de la dynamique des particules de fluide de manière mésoscopique et discontinue en étudiant la collision et la diffusion des particules, alors que N-S évalue un fluide continu.

### Équations de Navier-Stokes

* Équation de continuité (bilan de masse):
	$$\frac{\partial \rho}{\partial t} + \overrightarrow{\nabla} \cdot \left( \rho \vec{v} \right) = 0$$
	
* Équation de bilan de la quantité de mouvement:
$$\frac{\partial \left( \rho \vec{v} \right)}{\partial t} +  \left( \vec{v} \cdot \overrightarrow{\nabla} \right) \rho \vec{v} = - \overrightarrow{\nabla} p + \overrightarrow{\nabla} \cdot \overrightarrow{\overrightarrow {\tau}} + \rho \vec{f}$$

* Équation de bilan de l'énergie:
	$$\frac{\partial \left( \rho e\right)}{\partial t} + \overrightarrow{\nabla} \cdot \left[ \; \left(\rho e + p\right) \vec{v} \; \right] = \overrightarrow{\nabla} \cdot \left( \overrightarrow{\overrightarrow {\tau}} \cdot \vec{v} \right) + \rho \vec{f} \cdot \vec{v} - \overrightarrow{\nabla} \cdot \vec{\dot{q}} + r$$
 
 Où dans ces équations:
- $t$ désigne le temps
- $\rho$ désigne la masse volumique du fluide
- $p$ désigne la pression
- $\vec{v}$ désigne la vitesse eulérienne d'une particule fluide
- $\overrightarrow{\overrightarrow {\tau}}$ désigne le tenseur des contraintes visqueuses
- $\vec{f}$ désigne la résultante des forces massiques s'exerçant dans le fluide
- $e$ est l'énergie totale par unité de masse
- $\vec{\dot{q}}$ est le flux de chaleur perdu par conduction thermique
- $r$ représente la perte de chaleur volumique due au rayonnement

### Équation de Boltzmann
Cette équation décrit le comportement statique d'un système thermodynamique hors d'état d'équilibre, effectuant un lien entre la physique microscopique et la physique macroscopique.
On étudie la distribution de la probabilité pour la position $r$ et l'impulsion $p$ d'une particule donnée au travers de la fonction de distribution au sein d'un volume $V$. $$f: (r,p) \mapsto f(r,p)$$ 
Cette fonction évolue au cours du temps suivant trois facteurs: les forces externes exercées sur les particules, la diffusion des particules liée à leur mouvement dans l'espace et les éventuelles collisions: $$\frac{df}{dt} = (\frac{\partial f}{\partial t}) _{force} + (\frac{\partial f}{\partial t})_{diff} + (\frac{\partial f}{\partial t})_{coll}$$

Afin d'expliciter cette équation, on estime en premier lieu que le nombre de particules n'évolue pas dans la région considérée. D'après le théorème de Liouville:

> Le volume d'une région de l'espace des phases reste constant lorsqu'on suit cette région dans le temps.

Puisque l'on conserve le nombre de particules dans une région considérée, on a alors du point de vue lagrangien $$\frac{Df}{Dt}=0$$
On note $\vec{v} = \frac{d\vec{r}}{dt}$ et $\vec{F} = \frac{d\vec{p}}{dt}$ où $\vec{F}$ est le champ de forces extérieures et $\vec{v}=\vec{p}/m$ avec $\vec{p}$ le vecteur quantité de mouvement de la particule et $m$ sa masse.
En explicitant la dérivée lagrangienne, on obtient l'équation de conservation $$ \frac{\partial f}{\partial t} +  \vec{v} \cdot \overrightarrow{\nabla_r} f + \vec{F} \cdot \overrightarrow{\nabla_p} f = 0$$
Toutefois, il est nécessaire de prendre en compte les effets des collisions des particules entre elles. Aussi, les collisions de particules entre elles modifient les trajectoires de celles-ci au sein du volume de la région et on n'a plus conservation. En ajoutant un terme au bilan, on obtient l'équation générale de Boltzmann:
$$ \frac{\partial f}{Dt} +  \vec{v} \cdot \overrightarrow{\nabla_r} f + \vec{F} \cdot \overrightarrow{\nabla_p} f = (\frac{\partial f}{\partial t})_{coll}$$

## Le réseau

Ce projet consiste en la réalisation d'une simulation numérique d'écoulement de fluide en deux dimensions. Pour cela on considère un réseau à deux dimensions centré sur la particule considérée, entouré de huit noeuds. Il y a  quatre connexions nord, sud, est, ouest et quatre connexions diagonales, ainsi qu'une connexion sur le noeud considéré.
Caque particule peut se déplacer vers un noeud avec un pondération $w_i$ et une vitesse $v_i$ par pas de temps. Ce modèle est appelé D2Q9.
![D2Q9](C:\Users\guill\iCloudDrive\AM\7GIM\PJT\Mécaflu\D2Q9.png)
A chaque itération, la particule se déplace sur un point $p_i$ parmi ceux-ci: (0,0), (0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1).

## La fonction de distribution

A partir d'un tel modèle, on peut décrire un fluide comme une fonction de distribution $(x,v) \mapsto f(x,v)$, décrivant la densité de fluide dans la phase considérée au point $x$ affecté d'une vitesse $v$, comme explicité dans le modèle de Boltzmann ci-dessus.
Expérimentalement, un système hors état d'équilibre $f$ revient à un état d'équilibre $f_{eq}$ par des processus de relaxation qui dissipent l'énergie du système excité suivant une loi exponentielle de constante de temps $\tau$, nommée temps de relaxation. 

### Temps de relaxation

Ce temps de relaxation décrit la durée nécessaire au système pour revenir à son état d'équilibre, ie à la fonction de distribution pour revenir à son état d'équilibre.
On estime que le temps de relaxation est défini par: $$\tau = \frac{\nu_p}{c_s^2} \frac{\Delta t}{\Delta x^2} + \frac{1}{2}$$
Avec:
- $\nu_p$ la viscosité physique du fluide
- $c_s^2$ la vitesse du son en unité de Lattice-Boltzmann
- $\Delta t$ le pas de temps
- $\Delta x^2$ le pas d'espace
Ces derniers sont liés par la relation de conversion de la vitesse du son en unité physique en unité Lattice-Boltzmann: $$c_{s,p} = c_s \frac{\Delta x}{\Delta t}$$

### La loi de collision

Alors dans l'approximation BGK, on a la relation $$\frac{Df}{Dt} = -\frac{f-f_{eq}}{\tau}$$ (on décrit ici le terme de collision...) qui définit la probabilité qu'une particule soit localisée en un point $x$ à une vitesse $v$ à un instant donné.
Cette équation peut être discrétisée sur le réseau pour un temps caractéristique de simulation $\Delta t$ et pour tout $i \in \left[ \!\!\left[ 1;9 \right]\!\!\right]$:
$$F_i(x_i + v_i dt, t + dt) - F_i(x_i,t) = - \frac{F_i(x_i,t) - F_i^{eq}(x_i,t)}{\tau}$$ 

### La fonction de distribution à l'équilibre

Il est alors nécessaire de détailler la fonction de distribution à l'équilibre. On considère ici un fluide isotherme ayant une célérité du son constante. On trouve dans la littérature l'expression suivante:
$$F_i^{eq} = w_i \rho \left(1+3(v_i \cdot u) + \frac{9}{2} (v_i \cdot u)^2 + \frac{3}{2} (u \cdot u)^2 \right)$$
Où les $w_i$ sont les poids correspondants au modèle D2Q9, soit $$w_i= \begin{cases} \frac{4}{9} \textrm{ si } i=0\\ \frac{1}{9} \textrm{ si } i \in \left[ 1, 2, 3, 4 \right]\\ \frac{1}{36} \textrm{ si } i \in \left[ 5, 6, 7, 8 \right]\end{cases}$$ et $u$ la vitesse du fluide.

## L'algorithme

On détaille dans cette partie le fonctionnement de l'algorithme qui permet la simulation d'écoulement du fluide

### Collision et écoulement

On cherche à obtenir dans toute la région la densité macroscopique $\rho$ et le moment équivalent que subit chaque particule de fluide $\rho u$, que l'on peut définir ainsi en sommant dans toutes les directions du réseau:

$$\rho = \sum f_i$$
$$\rho u = \sum f_i v_i$$

### Conditions aux limites

Les conditions aux limites sont évaluées à l'échelle microscopique. Les lois de la réflexion s'appliquent lorsqu'une particule de fluide entre en contact avec un solide. Les collisions fluide-solide ne sont pas de la même nature que les collisions fluide-fluide, qui elle mènent à un état d'équilibre, conséquence de l'écoulement. Ainsi, les particules rebondissent simplement sans glisser contre les parois du solide. Cela se traduit par la loi: $$f_i(x,t+\Delta t)=f_{-i}(x,t)$$
Où l'indice $-i$ définit $v_{-i}=-v_i$.

### La simulation

Implémentée en Python, elle contient une grille (matrice) qui sert à recueillir en chacun de ses éléments les valeurs de la fonction de distribution $f$. Une troisième dimension permet de stocker la vitesse de chacune des particules relativement aux noeuds adjacents dans le réseau la  (neuf éléments).
Le réglage du temps de relaxation, équivalent dans les équations de Navier-Stokes à la viscosité dynamique, permet d'obtenir un écoulement turbulant à même de générer des tourbillons de Von Karman

## Sources
https://physique-univ.fr/onewebmedia/Phystat-c5-site.pdf
https://www.researchgate.net/figure/The-D2Q9-model-for-LBM-simulation_fig4_282092725
https://fr.wikipedia.org/wiki/M%C3%A9thode_de_Boltzmann_sur_r%C3%A9seau
https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_de_Liouville_(hamiltonien)
https://hmf.enseeiht.fr/travaux/beiepe/book/export/html/91
https://medium.com/swlh/create-your-own-lattice-boltzmann-simulation-with-python-8759e8b53b1c
https://hmf.enseeiht.fr/travaux/projnum/book/export/html/3507
https://fr.wikipedia.org/wiki/%C3%89quations_de_Navier-Stokes
https://www.ndsu.edu/fileadmin/physics.ndsu.edu/Wagner/LBbook.pdf
https://iopscience.iop.org/article/10.1209/0295-5075/17/6/001/pdf
https://hal.archives-ouvertes.fr/hal-03232070/file/anefficientlattice.pdf

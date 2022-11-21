from csv import unix_dialect
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from tqdm import tqdm

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y1-y2)**2)

def main():
    ### Paramètres d'affichage

    x=400
    y=100
    nbre_iterations=4000
    fig = plt.figure()
    frames=[]
    affichage_n=50  # Affichage tous les n itérations
    affichage_tps_reel=False # Affichage en temps réel
    enregistrer=True    # Enregistrer en la vidéo de la simulation
    affichage_vitesse=False
    
    ### Paramètres du fluides 

    """rho_0=100 # masse volumique du fluide initiale"""
    tau=0.57 # temps de relaxation qui équivaut à la viscosité dynamique

    ### Lattice / réseau

    taille=9
    """index=np.arange(taille)"""

    ### Positions dans le réseau et poids
    px=np.array([0, 0, 1, 1, 1, 0,-1,-1,-1])
    py=np.array([0, 1, 1, 0,-1,-1,-1, 0, 1])
    w=np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36])

    ### Conditions initiales

    f=np.ones((y,x,taille)) # Création de la fonction de distribution
    f+=0.01*np.random.randn(y,x,taille) # Inhomogénéité aléatoire du fluide

    """X,Y=np.meshgrid(range(x),range(y))  # Création de l'affichage"""

    f[:,:,3]+=2   ### Assignation d'une vitesse vers la droite (3ème noeud)

    """rho=np.sum(f,2) # Somme par ligne (stacking)
    for i in index:
            f[:,:,i] *= rho_0/rho   # Application de la densité de particule de référence du fluide"""

    ### Cylindre

    """X,Y=np.meshgrid(range(x),range(y))
    cyl=(X-x/4)**2+(Y-y/2)**2 < (y/4)**2    # Equation de cercle plein (True si matière, False sinon)"""

    cyl=np.full((y,x),False)
    for b in range(y):
        for a in range(x):
            if distance(x//4,y//2,a,b)<13:
                cyl[b][a]=True
    
    ### Simulation

    for iteration in tqdm(range(nbre_iterations)):
        
        ### Suppression de la reflectivité des bords

        f[:,-1,[6,7,8]]=f[:,-2,[6,7,8]]
        f[:, 0,[2,3,4]]=f[:, 1,[2,3,4]]
        
        ### Avancement de la simulation
        for i,p_x,p_y in zip(range(taille),px,py):
            f[:,:,i]=np.roll(f[:,:,i],p_x,axis=1)   ### On déplace les caractéristiques de chaque noeud vers celui qui correspond à la vitesse qu'il possède
            f[:,:,i]=np.roll(f[:,:,i],p_y,axis=0)

        ### Conditions aux limites et rebond

        boundary=f[cyl,:]   # Application des conditions aux limites
        boundary=boundary[:,[0,5,6,7,8,1,2,3,4]]    # Application des conditions de rebond

        ### Calcul des paramètres du fluide

        rho=np.sum(f,2)
        vx=np.sum(f*px,2)/rho
        vy=np.sum(f*py,2)/rho

        ### Matérialisation du cylindre

        f[cyl,:]=boundary
        vx[cyl]=0
        vy[cyl]=0
        
        ### Collisions

        f_eq=np.zeros(f.shape)
        for i,p_x,p_y,w_i in zip(range(taille),px,py,w):
            f_eq[:,:,i]=rho*w_i*(1+3*(p_x*vx+p_y*vy) + 9*(p_x*vx+p_y*vy)**2/2 - 3*(vx**2+vy**2)/2)

        f-=(1/tau)*(f-f_eq)
        
        

        """    ### Affichage en temps réel
        if (iteration%affichage_n)==0: ### on affiche une image sur 10 pour alléger le travail machine
            plt.cla() # Clear the current axes
            vx[cyl]=0   # pas dans le vitesse de fluide dans le cylindre car il y a de la matière solide
            vy[cyl]=0

            vorticite=(np.roll(vx, -1,axis=0)-np.roll(vx,1,axis=0))-(np.roll(vy,-1,axis=1)-np.roll(vy,1,axis=1))    # Calcul de la vorticité
            vorticite[cyl]=np.nan   # Not a Number pour éviter les erreurs dues à la manipulation de flottants
            vorticite=np.ma.array(vorticite,mask=cyl)   # Idem
            plt.imshow(vorticite,cmap='bwr')    # Affiche la vorticité
            plt.imshow(~cyl,cmap='gray',alpha=0.3)  # Affiche ce qui ne correspond pas au cylindre
            plt.clim(-.1,.1)    # Non saturation des couleurs
            ax=plt.gca()    # Get current axes
            ax.invert_yaxis()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)	
            ax.set_aspect('equal')	
            plt.savefig("img_"+str(iteration//10)+".png")

    ### Animation
    img=[]  # Importation des images
    frames=[]   # Stockage les images pour en faire une vidéo

    for i in tqdm(range(iteration)):
        img.append(plt.imread("img_"+str(iteration//10)+".png"))

    fig=plt.figure()
    for i in tqdm(range(len(img))):
        frames.append([plt.imshow(img[i],animated=True)])

    animate=animation.ArtistAnimation(fig,tqdm(frames),interval=100,blit=True)
    animate.save("Lattice-Boltzmann.mp4")"""

        if iteration%affichage_n==0:

            if affichage_vitesse==True:
                vitesse=np.sqrt(vx**2+vy**2)
                frames.append([plt.imshow(vitesse,animated=True)])
                if affichage_tps_reel==True:
                    plt.imshow(vitesse)
                    plt.pause(.01)
                plt.cla
            
            else:
                rotationnel=(vx[2:, 1:-1]-vx[0:-2, 1:-1])-(vy[1:-1, 2:]-vy[1:-1, 0:-2])
                frames.append([plt.imshow(rotationnel, cmap="bwr",animated=True)])
                if affichage_tps_reel==True:
                    plt.imshow(rotationnel, cmap="bwr")
                    plt.pause(.01)
                plt.cla

    ani = animation.ArtistAnimation(fig, frames, interval=100, blit=True)           
    ani.save("Lattice-Boltzmann.mp4")
if __name__=="__main__":
    main()
import matplotlib
matplotlib.use('Agg') #C'est le backend qu'on va utiliser pour afficher les images dans le navigateur web. Il est necessaire de l'utiliser pour que le code fonctionne sur le serveur web
import matplotlib.pyplot as plt
from linkedlists import Node
from linkedlists import Linkedlist
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLEU_DATA = '#1f77b4' # Couleur pour les données bleues
GRIS_PTR = '#7f7f7f' # Couleur pour les pointeurs gris
ORANGE = '#ff7f0e' # Couleur pour les noeuds visites
ROUGE = '#d62728' # Couleur pour les noeuds courants ou supprimés
VERT = '#2ca02c' # Couleur pour les noeuds non inseres ou non visites
BORDER_COLOR = '#000000' # Couleur pour les bordures des noeuds

def _draw_node(ax, x, y, data, next_existe, face = BLEU_DATA, dashed= False, adresse = None):
    """Dessine un noeud dont le coin inférieur gauche est en (x, y) avec la valeur data et un pointeur vers le noeud suivant si next_existe est True.
    Paramètres:
    x,y : coordonnées du coin inférieur gauche du noeud
    data : valeur du noeud
    next_existe : True si le noeud a un pointeur vers le noeud suivant(on dessine "o" s'il existe), False sinon et on dessine "x" pour indiquer qu'il n'y a pas de pointeur vers le noeud suivant
    face : couleur de remplissage du noeud
    dashed: bordure en pointilles (noeud flottant) ou pas (noeud fixe)
    adresse : adresse memoire du noeud a afficher sous le noeud 
    """
    style = "round, pad= 0.03, rounding_size=0.05"
    ls = "--" if dashed else "-" #Trait en pointillés si le noeud est flottant, sinon trait plein
    #Pour ce qui est des données du noeud, on dessine un rectangle avec la valeur du noeud et l'adresse memoire du noeud si elle est fournie
    ax.add_patch(FancyBboxPatch((x, y), 0.9, 1.0, boxstyle=style, edgecolor=BORDER_COLOR, facecolor=face, linewidth=1.6, linestyle=ls))
    """On dessine le texte de la valeur du noeud au centre du rectangle
    ax.text(x + 0.45, y + 0.5, str(data), ha='center', va='center', fontsize=12, color='white')
    if adresse is not None:
        ax.text(x + 0.45, y - 0.2, str(adresse), ha='center', va='center', fontsize=8, color='black') """
    #Pour ce qui est du pointeur vers le noeud suivant, on dessine un cercle avec "o" si le pointeur existe, sinon on dessine un cercle avec "x"
    ax.add_patch(FancyBboxPatch((x + 0.9, y ), 0.7, 1.0, boxstyle=style, edgecolor=BORDER_COLOR, facecolor=GRIS_PTR, linewidth=1.6, linestyle=ls))
    
    #On dessine le texte du pointeur vers le noeud suivant au centre du cercle
    if next_existe:
        ax.text(x + 1.25, y + 0.5, "o", ha='center', va='center', fontsize=12, color='white')
    else:
        ax.text(x + 1.25, y + 0.5, "x", ha='center', va='center', fontsize=12, color='white')
    ax.text(x + 0.45, y + 0.5, str(data), ha="center", va="center",
            fontsize=13, fontweight="bold", color="#0f172a")
    ax.text(x + 1.25, y + 0.5, "o" if next_existe else "None",
            ha="center", va="center", fontsize=11,
            color=BORDER_COLOR if next_existe else "#b91c1c",
            fontweight="bold")
    if adresse:   # l'adresse mémoire réelle, sous le nœud
        ax.text(x + 0.8, y - 0.35, adresse, ha="center", va="center",
                fontsize=7.5, color="#64748b", family="monospace")
def fleche(ax, x1, y1, x2, y2, dashed=False, rad=-0.2, couleur="#0f172a"):
    """Dessine une flèche courbe d'un compartiment pointeur vers le nœud suivant."""
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle="-|>", mutation_scale=22, lw=1.8,
                                 color=couleur, linestyle="--" if dashed else "-",
                                 connectionstyle=f"arc3,rad={rad}"))


def positions(n):
    """Renvoie la liste des abscisses des n nœuds, espacés régulièrement."""
    return [i * 2.6 for i in range(n)]


def dessiner_liste(liste_chainee, titre="", surligne=None, courant=None,
                   supprime=None, noeud_flottant=None, annotation=None,
                   fichier=None, ignorer_arete=None):
    """Dessine l'état d'une LinkedList avec en-tête/queue et pointeurs.

    Paramètres pédagogiques
    -----------------------
    surligne       : set d'indices déjà visités (orange)
    courant        : indice du nœud "courant" pendant un parcours (rouge)
    supprime       : indice d'un nœud qui va être sauté (rouge, flèches fantôme)
    ignorer_arete  : indice i -> ne PAS dessiner la flèche i -> i+1
                     (utilisé pour montrer la "recousure" avant suppression)
    noeud_flottant : tuple (data, adresse) dessiné en vert en pointillés,
                     avec une flèche pointillée vers la tête (insertion au début)
    annotation     : texte libre affiché sous le schéma
    fichier        : si fourni, sauvegarde en PNG au lieu d'afficher
    """
    surligne = surligne or set()
    valeurs = liste_chainee.to_list()          # [10, 20, 30]
    n = len(valeurs)
    xs = positions(n)

    fig, ax = plt.subplots(figsize=(max(3.5, n * 2.6 + 2.5), 3.2), dpi=130)

    # ---------- CAS PARTICULIER : liste vide ----------
    if n == 0:
        ax.text(0.4, 0.5, "head", fontsize=12, fontweight="bold", color="#7c3aed")
        fleche(ax, 0.95, 0.5, 1.85, 0.5, rad=0)
        ax.text(2.1, 0.5, "None", fontsize=13, fontweight="bold", color="#b91c1c")
        ax.text(0.4, -0.25, "tail", fontsize=12, fontweight="bold", color="#059669")
        fleche(ax, 0.9, -0.2, 1.85, 0.25, rad=-0.3)
        ax.set_xlim(-0.5, 4); ax.set_ylim(-1, 1.6)
    else:
        # ---------- 1) NŒUDS ----------
        for i, val in enumerate(valeurs):
            noeud_reel = _noeud_a_indice(liste_chainee, i)
            couleur = BLEU_DATA
            if i in surligne:                       couleur = ORANGE
            if courant == i:                        couleur = ROUGE
            if supprime == i:                       couleur = ROUGE
            _draw_node(ax, xs[i], 0, val,
                            next_existe=(i < n - 1),
                            face=couleur,
                            dashed=(supprime == i and ignorer_arete is not None),
                            adresse=f"0x{id(noeud_reel):012x}")

        # ---------- 2) FLÈCHES pointeur -> pointeur ----------
        for i in range(n - 1):
            if ignorer_arete == i:
                continue   # on masque la vieille flèche (suppression en cours)
            x1, x2 = xs[i], xs[i + 1]
            fleche(ax, x1 + 1.25, 0.5, x2 + 0.05, 0.5)
        # dernière flèche : de la queue vers "None"
        if supprime is None:
            fleche(ax, xs[-1] + 1.25, 0.5, xs[-1] + 2.3, 0.05, rad=-0.25,
                    couleur="#b91c1c")
            ax.text(xs[-1] + 2.35, 0.0, "None", fontsize=12, fontweight="bold",
                    color="#b91c1c", va="center")

        # ---------- 3) ÉTIQUETTES head / tail ----------
        ax.annotate("head", xy=(xs[0] + 0.45, 1.0), xytext=(xs[0] + 0.45, 1.75),
                    fontsize=12, fontweight="bold", color="#7c3aed", ha="center",
                    arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=1.8))
        ax.annotate("tail", xy=(xs[-1] + 0.45, 1.0), xytext=(xs[-1] + 0.45, 1.75),
                    fontsize=12, fontweight="bold", color="#059669", ha="center",
                    arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.8))

        # ---------- 4) NŒUD FLOTTANT (nouveau nœud, pas encore inséré) ----------
        if noeud_flottant is not None:
            data, adr = noeud_flottant
            fx = -2.6          # à gauche de tout, isolé
            _draw_node(ax, fx, 0, data, next_existe=True,
                            face=VERT, dashed=True, adresse=adr)
            ax.annotate("new_node", xy=(fx + 0.45, 1.0), xytext=(fx + 0.45, 1.75),
                        fontsize=11, fontweight="bold", color="#15803d",
                        ha="center",
                        arrowprops=dict(arrowstyle="-|>", color="#15803d",
                                        lw=1.6, linestyle="--"))
            # flèche pointillée : le nouveau nœud "regarde" l'ancienne tête
            fleche(ax, fx + 1.25, 0.5, xs[0] + 0.05, 0.5, dashed=True,
                    rad=-0.25, couleur="#15803d")
            ax.text((fx + xs[0]) / 2 + 0.6, 1.15,
                    "new_node.next = ancienne_tête", fontsize=9,
                    color="#15803d", ha="center", style="italic")
            ax.set_xlim(fx - 0.7, xs[-1] + 3.2)
        else:
            ax.set_xlim(-0.7, xs[-1] + 3.2)
        ax.set_ylim(-0.9, 2.3)

    # ---------- 5) TITRE ET ANNOTATION ----------
    if titre:
        ax.set_title(titre, fontsize=12, fontweight="bold", color="#0f172a",
                     pad=14)
    if annotation:
        ax.text(0.02, -0.72, annotation, transform=ax.transAxes, fontsize=10,
                color="#334155", style="italic",
                bbox=dict(boxstyle="round,pad=0.4", fc="#f8fafc",
                          ec="#cbd5e1", lw=1))

    ax.axis("off")
    fig.tight_layout()
    if fichier:
        fig.savefig(fichier, bbox_inches="tight", facecolor="white")
        plt.close(fig)
    else:
        plt.show()



def _noeud_a_indice(liste_chainee, i):
    """Renvoie l'OBJET Node réel à l'indice i (pour afficher sa vraie adresse)."""
    courant = liste_chainee.head
    for _ in range(i):
        courant = courant.next
    return courant
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedlists import Node, Linkedlist
from draw import dessiner_liste

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rendus")
os.makedirs(DOSSIER, exist_ok=True)


def sauve(nom, liste, **kwargs):
    """Raccourci : dessine la LISTE + sauvegarde dans ./rendus/nom.png"""
    chemin = os.path.join(DOSSIER, nom)
    dessiner_liste(liste, fichier=chemin, **kwargs)
    print(f"  -> rendus/{nom}")



# PARTIE 1 — INSERTION AU DÉBUT, image par image

print("PARTIE 1 : insertion au début (insert_at_beginning)")
ll = Linkedlist()
ll.insert_at_end(20)     # on prépare une liste [20, 30]
ll.insert_at_end(30)     # (on utilisera la méthode "fin" plus bas, au calme)
sauve("01_debut_initial.png", ll,
      titre="Étape 0 : liste de départ = [20, 30]",
      annotation="On veut insérer 10 AU DÉBUT.")

# Étape A : on crée le nœud 10... il est SEUL, déconnecté de la liste
new_node = Node(10)
sauve("02_new_node_isole.png", ll,
      titre="Étape 1 : new_node = Node(10)  <- encore isolé !",
      noeud_flottant=(10, f"0x{id(new_node):012x}"),
      annotation="new_node existe en mémoire, mais personne ne pointe vers lui.")

# Étape B : on branche new_node.next vers l'ancienne tête
new_node.next = ll.head
sauve("03_new_node_pointe_tete.png", ll,
      titre="Étape 2 : new_node.next = self.head",
      noeud_flottant=(10, f"0x{id(new_node):012x}"),
      annotation="Le nouveau nœud 'regarde' l'ancienne tête (20). "
                 "Rien n'est encore cassé : la liste est toujours valide.")

# Étape C : on déplace head (c'est exactement le code de la méthode)
ll.head = new_node
sauve("04_head_deplace.png", ll, titre="Étape 3 : self.head = new_node", annotation="MAGIQUE : déplacer UN SEUL pointeur (head) suffit ! ""La liste est maintenant [10, 20, 30].")



# PARTIE 2 — INSERTION À LA FIN

print("PARTIE 2 : insertion à la fin (insert_at_end)")
ll2 = Linkedlist()
ll2.insert_at_end(10)
ll2.insert_at_end(20)
sauve("05_fin_avant.png", ll2,
      titre="Avant : liste = [10, 20], tail pointe vers 20",
      annotation="On veut ajouter 30 à la fin.")
ll2.insert_at_end(30)
sauve("06_fin_apres.png", ll2,
      titre="Après : tail.next = new_node PUIS tail = new_node",
      annotation="Deux affectations seulement -> O(1). "
                 "Sans le pointeur tail, il aurait fallu PARCOURIR toute la liste !")



# PARTIE 3 — RECHERCHE : le parcours nœud par nœud

print("PARTIE 3 : recherche de 30 (search)")
ll3 = Linkedlist()
for v in [10, 20, 30, 40]:
    ll3.insert_at_end(v)
valeur_cherchee = 30
sauve("07_recherche_depart.png", ll3,
      titre=f"Recherche de {valeur_cherchee} : courant = head",
      courant=0,
      annotation="On compare 10 avec 30 : différent -> on suit le pointeur.")

sauve("08_recherche_pas1.png", ll3,
      titre=f"courant = courant.next -> nœud 20",
      surligne={0}, courant=1,
      annotation="10 est visité (orange). On compare 20 avec 30 : différent.")

sauve("09_recherche_trouve.png", ll3,
      titre=f"courant = courant.next -> nœud 30 : TROUVÉ !",
      surligne={0, 1}, courant=2,
      annotation="On renvoie True et on s'arrête immédiatement.")



# PARTIE 4 — SUPPRESSION : la "recousure"

print("PARTIE 4 : suppression de 30 (delete)")
ll4 = Linkedlist()
for v in [10, 20, 30, 40]:
    ll4.insert_at_end(v)
sauve("10_suppression_localise.png", ll4,
      titre="Étape 1 : on a localisé 30 grâce à 'precedent' (20)",
      surligne={0}, supprime=2,
      annotation="secret : precedent garde UNE LONGUEUR D'AVANCE sur courant.")

sauve("11_suppression_recousure.png", ll4,
      titre="Étape 2 : precedent.next = courant.next  (RECOSURE !)",
      surligne={0}, supprime=2, ignorer_arete=1,
      annotation="La flèche 20 -> 30 est remplacée par 20 -> 40. "
                 "Le nœud 30 devient orphelin : Python le détruit tout seul.")

ll4.delete(30)
sauve("12_suppression_apres.png", ll4,
      titre="Étape 3 : liste finale = [10, 20, 40]",
      annotation="La queue n'a pas bougé (on n'a pas supprimé le dernier).")



# PARTIE 5 — LISTE VIDE

print("PARTIE 5 : liste vide")
ll5 = Linkedlist()
sauve("13_liste_vide.png", ll5,
      titre="LinkedList() : head et tail pointent vers None",
      annotation="None = 'je ne pointe vers rien'. Toute méthode commence par "
                 "vérifier ce cas (d'où les if self.head).")

print(f"\nTerminé ! Ouvrez les images dans l'ordre : {DOSSIER}")
class Node:
    def __init__(self,data):
        self.data=data
        self.next=None

class Linkedlist:
    def __init__(self):
        self.head=None
        self.tail = None

    def insert_at_beginning(self,data):
        new_node=Node(data)

        if self.head is None: #si il n'y a rien a la tete de la liste,
            self.head=new_node  #on cree une tete
            self.tail=new_node  #et puisqu'il n'y avait rien a la tete ce la signifie que la liste etait vide donc la tete est aussi la queue de la liste

        else: #si par contre il y avait deja une tete
            new_node.next=self.head  #on pose l'ancienne tete de la liste comme le suivant du nouveau noeud
            self.head=new_node #Et on pose le nouveau noeud comme la tete de la liste
    
    def insert_at_end(self,data):
        """Comment insérer un élément à la fin d'une liste chaînée"""
        new_node = Node(data)
        if self.tail is None: #si il n'y a rien a la queue de la liste, il n'y a rien a la tete de la liste non plus donc on cree une tete et une queue
            self.head=new_node #donc on cree une tete qui est le nouveau noeud et aussi la queue de la liste
            self.tail=new_node
        else: #si par contre il y avait deja une queue
            self.tail.next=new_node #on pose le nouveau noeud comme le suivant de l'ancienne queue
            self.tail=new_node

    def insert_at_position(self, data, position):
        """Comment insérer un élément à une position donnée dans une liste chaînée"""
        if position == 0 or self.head is None:
            self.insert_at_beginning(data)
            return

        current_node = self.head
        for i in range(position - 1):
            if current_node is None:
                break
            current_node = current_node.next

        if current_node is None:
            print("La position donnée est supérieure à la taille de la liste")
            return

        new_node = Node(data)
        new_node.next = current_node.next
        current_node.next = new_node

        # Si l'élément est inséré tout à la fin, on met à jour la queue (tail)
        if new_node.next is None:
            self.tail = new_node

    def search(self, data):
        """Comment rechercher un élément dans une liste chaînée"""
        current_node = self.head
        while current_node is not None:
            if current_node.data == data:
                return True
            current_node = current_node.next
        return False

    def delete(self, data):
        """Supprimer la première occurrence d'une valeur dans la liste chaînée"""
        if self.head is None:
            return False

        # Cas 1 : La tête contient la valeur à supprimer
        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return True

        # Cas 2 : La valeur est dans la suite de la liste
        current_node = self.head
        while current_node.next is not None:
            if current_node.next.data == data:
                if current_node.next == self.tail:
                    self.tail = current_node
                current_node.next = current_node.next.next
                return True
            current_node = current_node.next

        return False

    def to_list(self):
        """Comment transformer une liste chaînée en liste Python de valeurs"""
        liste = []
        current_node = self.head
        while current_node is not None:
            liste.append(current_node.data)
            current_node = current_node.next
        return liste


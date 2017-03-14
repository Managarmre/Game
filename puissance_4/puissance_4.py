"""
	Puissance 4
	@author Pauline Houlgatte
	@version 1.0
"""

from tkinter import *
import random
from tkinter.messagebox import showerror,showinfo

global joueur_actuel

def creation_fenetre():
	print("Création de la fenêtre...")
	fenetre = Tk()
	print("Fenêtre créée.")
	return fenetre

def dessiner_grille(fenetre):
	print("Création de la grille...")
	grille = [['None' for i in range(7)] for i in range(6)]
	print("Grille créée : ",len(grille)," colonnes et ", 
		len(grille[0])," lignes.")
	print("Ajout de la grille dans la fenêtre...")
	canvas = Canvas(fenetre, width=280, height=240, background='white')
	for i in range(len(grille[0])):
		colonne = canvas.create_line(40*i,0,40*i,240)
	for i in range(len(grille)):
		ligne = canvas.create_line(0,40*i,280,40*i)
	canvas.pack()
	print("Ajout terminé.")
	return grille,canvas

def verification_placement(grille,colonne,ligne=-1):
	print("Vérification du placement du pion...")
	c = [grille[i][colonne] for i in range(len(grille))]
	for i in range(len(c)):
		if (c[i] == 'None'):
			ligne = i
		else:
			break;
	if (ligne == -1):
		print("Colonne complète...")
		showerror("Placement interdit",
			"Colonne complète, placez votre pion à une autre position !")
		return -1
	print("Le placement a été validé.")
	return ligne

def ajout_pion_grille(grille,canvas,colonne,ligne,color):
	print("Ajout d'un pion sur la grille...")
	grille[ligne][colonne] = color
	pion = canvas.create_oval(colonne*40,ligne*40,
		colonne*40+40,ligne*40+40,fill=color)
	print("Un pion a été ajouté.")

def mise_a_jour_joueur():
	while True:
		yield "yellow"
		yield "red"

def recuperation_clic(event):
	clic_colonne = event.x
	clic_colonne = int(clic_colonne/40)
	ligne = verification_placement(grille,clic_colonne)
	if (ligne != -1):
		color = next(joueur_actuel)
		ajout_pion_grille(grille,canvas,clic_colonne,ligne,color)
		end_of_game(clic_colonne,ligne,grille,color)

def end_of_game(colonne,ligne,grille,color):
	compteur = 0
	ligne_verif = grille[ligne]
	nombre_ligne = ligne_verif.count(color)
	if (nombre_ligne >= 4):
		for i in range (len(ligne_verif)):
			if (compteur == 4):
				break;
			elif (ligne_verif[i] == color):
				compteur = compteur + 1
			else:
				compteur = 0
	verif_end_of_game(compteur,color)

	compteur = 0
	colonne_verif = [grille[i][colonne] for i in range(len(grille))]
	nombre_colonne = colonne_verif.count(color)
	if (nombre_colonne >= 4):
		for i in range (len(colonne_verif)):
			if (compteur == 4):
				break;
			elif (colonne_verif[i] == color):
				compteur = compteur + 1
			else:
				compteur = 0
	verif_end_of_game(compteur,color)

	diag1_verif = [grille[ligne][colonne]]
	diag2_verif = [grille[ligne][colonne]]

	tmp1 = [(ligne,colonne)]
	tmp2 = [(ligne,colonne)]

	for i in range(1,6):
		if (ligne - i >= 0 and colonne - i >= 0):
			diag2_verif.insert(0,grille[ligne-i][colonne-i])
			tmp2.insert(0,(ligne-i,colonne-i))
		if (ligne + i < len(grille) and colonne + i < len(grille[0])):
			diag2_verif.append(grille[ligne+i][colonne+i])
			tmp2.append((ligne-i,colonne-i))
		if (ligne - i >= 0 and colonne + i < len(grille[0])):
			diag1_verif.append(grille[ligne-i][colonne+i])
			tmp1.insert(0,(ligne-i,colonne-i))
		if (ligne + i < len(grille) and colonne - i >= 0):			
			diag1_verif.insert(0,grille[ligne+i][colonne-i])
			tmp1.append((ligne-i,colonne-i))

	nombre_diag1 = diag1_verif.count(color)
	nombre_diag2 = diag2_verif.count(color)

	compteur = 0
	if (nombre_diag1 >= 4):
		for i in range (len(diag1_verif)):
			if (compteur == 4):
				break;
			elif (diag1_verif[i] == color):
				compteur = compteur + 1
			else:
				compteur = 0
	verif_end_of_game(compteur,color)

	compteur = 0
	if (nombre_diag2 >= 4):
		for i in range (len(diag2_verif)):
			if (compteur == 4):
				break;
			elif (diag2_verif[i] == color):
				compteur = compteur + 1
			else:
				compteur = 0
	verif_end_of_game(compteur,color)

def verif_end_of_game(compteur,color):
	if (compteur == 4):
		print("C'est gagné !")
		message = "Félicitation "+color+" remporte la partie"
		showinfo("Victoire !", message)
		print("Fin de la partie")
		exit()

"""
	main function
"""
if __name__ == '__main__':
	joueur_actuel = mise_a_jour_joueur()

	fenetre = creation_fenetre()
	grille,canvas = dessiner_grille(fenetre)

	canvas.bind("<Button-1>", recuperation_clic)
	canvas.pack()

	fenetre.mainloop()
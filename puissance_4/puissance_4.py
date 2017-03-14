"""
	Puissance 4
	@author Pauline Houlgatte
	@version 2.0
"""

"""
	liste des tâches
		réaliser différents niveaux d'IA
"""

from tkinter import *
import random
from tkinter.messagebox import showerror,showinfo
import argparse

global joueur_actuel

def arg_parser():
    parser = argparse.ArgumentParser(description=
    	'Par défaut JvJ')
    parser.add_argument('-ia', help=
    	'JvsIA - Niveau ia, 1 = random, 5 = expert',
    	choices=[1,2,3,4,5],type=int)
    args = parser.parse_args()
    return args

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
		# tour IA
		if (niveau_ia) :
			c_ia, l_ia = ia(grille,niveau_ia,color)
			color = next(joueur_actuel)
			ajout_pion_grille(grille,canvas,c_ia,l_ia,color)
			end_of_game(c_ia,l_ia,grille,color)

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

def ia(grille,niveau,couleur_adverse):
	print("L'IA prépare son coup...")
	if (niveau == 1):
		ligne,colonne = ia_random(grille)
	elif (niveau == 2): 
		ligne,colonne = ia_expert(grille,couleur_adverse)
	print("L'IA a terminé son tour.")
	return colonne,ligne

def ia_random(grille):
	colonne = random.randrange(0,len(grille),1)
	ligne = verification_placement(grille,colonne)
	while (ligne == -1):
		colonne = random.randrange(0,len(grille),1)
		ligne = verification_placement(grille,colonne)
	return ligne,colonne

def ia_expert(grille,couleur_adverse):
	# regarder le plus loin possible, 
	# bloquer tout alignement de trois pions gagnants
	# min max / alpha bêta
	ligne = 0
	colonne = 0
	return ligne,colonne

"""
	main function
"""
if __name__ == '__main__':
	arg = arg_parser()
	niveau_ia = arg.ia

	joueur_actuel = mise_a_jour_joueur()

	fenetre = creation_fenetre()
	grille,canvas = dessiner_grille(fenetre)

	canvas.bind("<Button-1>", recuperation_clic)
	canvas.pack()

	fenetre.mainloop()


"""
/*
       fonction minmax avec �lagage alpha/beta
       @param n : profondeur atteinte dans l'arbre du jeu
       @param grille : configuration atteinte
       @param alpha : param�tre pour l'�lagages, valeur maximale actuellement atteinte
       par le programme 
       @param beta : param�tre pour l'�lagages, valeur minimale actuellement atteinte
       par l'adversaire du programme
    */
  private Resultat minimaxAlphaBeta(int n, Puissance4 grille, double alpha, double beta) {
	int[] coups ;
	Resultat succ = new Resultat (0.0,-1) ;
	Resultat res = new Resultat(0.0,-1) ;
	Puissance4 grille2 ;
 
	if (n == _profondeur) {
	    return new Resultat(grille.evaluation(), coupAleatoire(grille)) ;	    
	}
	else {
	    if ((n % 2) == 0) {
		/* c'est � l'ordi de jouer */
		coups = grille.generateurDeCoups() ;
		if (coups.length == 0) return new Resultat(0.0,-1) ;
		int pos=0;
		for (int i = 0 ; i < coups.length ; i++) {
		  if (grille.programmeAGagne(coups[i])) return new Resultat(MAX,coups[i]) ;
		}
		res.valeur(alpha) ;
		res.colonne(coups[0]) ;
		
		/* ajout */	
		Resultat[] tabMemo=new Resultat[_matrice[0].length];
		tabMemo[pos]=new Resultat(alpha, coups[0]);
		/* fin ajout */
		
		for (int i = 0 ; i < coups.length && (alpha < beta) ; i++) {	     		
		    grille2 = grille.copie() ;
		    grille2.programmeJoueEn(coups[i]) ;
		    succ = minimaxAlphaBeta(n+1, grille2, alpha, beta) ;		    
		if(n==0)System.out.println("colonne "+coups[i]+" : "+succ.valeur());
		    /* ajout personnel */
		    if (succ.valeur() == alpha) { //aleatoire
			tabMemo[pos]=new Resultat(succ.valeur(), coups[i]);
			pos++;
		    }
		   /* fin ajout */
		    
		    if (succ.valeur() > alpha) {	           
			alpha = succ.valeur() ;
			res.valeur(alpha) ;
			res.colonne(coups[i]);
			/* ajout personnel */
			tabMemo[0]=new Resultat(succ.valeur(), coups[i]);
			pos=1;
			/* fin ajout */
			
		    }
		   
		}
		 if(pos>1){/* plusieurs �galit�s */
		 	int ran =RANDOM.nextInt(pos);
		    	   res=tabMemo[ran];
		    	   if(n==0)System.out.println("coup al�atoire :  
		nb choix("+pos+") pos("+ran+") colonne("+res.colonne()+")");
		    	   if(n==0)afficheR(tabMemo,pos);
		    	   }
		return res ;
	    }
	    else {/* on simule l'adversaire */
		coups = grille.generateurDeCoups() ;
		if (coups.length == 0) return new Resultat(0.0,-1) ;
		
		for (int i = 0 ; i < coups.length ; i++) {
		    if (grille.adversaireAGagne(coups[i])) return new Resultat(MIN,coups[i]) ;
		}
		res.valeur(beta) ;
		res.colonne(coups[0]) ;
		/* teste tous les cas possibles */
		for (int i = 0 ; i < coups.length && (alpha < beta) ; i++) {	     
		    grille2 = grille.copie() ;
		    grille2.adversaireJoueEn(coups[i]) ;
		  
		    succ = minimaxAlphaBeta(n+1, grille2, alpha, beta) ;
		 
		    if (succ.valeur() < beta) {
			beta = succ.valeur() ;
			res.valeur(beta) ;
			res.colonne(coups[i]) ;
		    }
		}		
		return res ;
	    }
	}
    }
"""

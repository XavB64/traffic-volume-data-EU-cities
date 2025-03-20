Les donn�es de la d�tection de Verhers Berlin sont fournies tous les mois sous forme de valeurs horaires des d�tecteurs de trafic pr�cis et agr�g�es via les sections de direction des routes. 

Chaque archive csv contient les champs de donn�es suivants:

D�tecteurs:

detid-15 - ID du d�tecteur (ventin � 15 chiffres).
tag - date
heure-heure de la journ�e pour laquelle les valeurs mesur�es ont �t� d�termin�es (8 08:00 - 08:59).
qualitaet - refl�te la proportion des intervalles de mesure parfaits disponibles pour l'heure: 1,0 - 100%. Les valeurs horaires inf�rieures � 75 % ne sont pas incluses.
q'3kfz'3det'3h - nombre de tous les v�hicules � moteur par heure.
V-3 kfz-3det-3h - vitesse moyenne [km/h/km/h/km/h/k/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/j/
q-3pkw-3det-3h - nombre de toutes les voitures par heure.
V-3pkw-3det-3h - vitesse moyenne [km/h) sur toutes les voitures par heure.
q-3lkw-3det-3h - nombre de tous les camions par heure.
V-3lkw-3det-3h - vitesse moyenne [km/h) sur tous les camions par heure.


Sections transversales de mesure:

mq-name - ID de la section transversale de mesure.
tag - date
heure-heure de la journ�e pour laquelle les valeurs mesur�es ont �t� d�termin�es (8 08:00 - 08:59).		
qualitaet - En raison du processus, cette valeur est toujours de 1,0, c'est-�-dire qu'il y avait une valeur horaire valable pour tous les d�tecteurs appartenant � cette section transversale. 
			Aucune valeur n'est form�e pour la section de mesure manquante dans des d�tecteurs individuels.
q'3kfz'3mq'3h - nombre de tous les v�hicules � moteur en heure.
v-3kfz-3mq-3h - Moyenne vitesse [km/h/min/h/k/h//////////////////////////////////////////////////////////////////////////////
q'3pkw'3mq'3h - nombre de toutes les voitures par heure.
V-3pkw-3mq-3h - vitesse moyenne (km/h) sur toutes les voitures par heure.
q 3lkw-3mq-3h - nombre de tous les camions par heure.
v-3lkw-3mq-3h - vitesse moyenne [km/h) sur tous les camions par heure.



Notes : 
Il peut y avoir de petites diff�rences entre le nombre de v�hicules � moteur (q-kfz-det-hr) et la somme pour les voitures (q-pkw-det-hr) et les camions (q-lkw-3det-3h). Ceci r�sulte d'erreurs d'arrondi dues � la m�thode s�lectionn�e.
Seules des valeurs horaires pour les d�tecteurs sont form�es s'il existe des donn�es valables pour au moins 75 % des intervalles de mesure d'une heure. Si ce n'est pas le cas, la valeur horaire correspondante est manquante dans l'archive csv.
S'il n'y a pas de valeur horaire valable pour les d�tecteurs de TOUT de section transversale de mesure pour les d�tecteurs de LAL, aucune valeur horaire n'est form�e pour la section transversale de mesure.



L'emplacement des d�tecteurs et l'affectation des d�tecteurs individuels � une coupe de mesure li�e � la direction se trouvent dans le fichier ma�tre de d�tection de trafic de donn�es-Berlin.xlsx.

Il contient les fiches de donn�es suivantes:
1) DET
Affectation du d�tecteur ID (DET-ID15) � l'ID de la section de mesure (MQ-ID15). 
La colonne LANE contient des informations sur l'emplacement de la voie (HF-R - 1. Trail de droite sur la route principale, HR-2vr - 2. Sujet de droite sur la route principale, ...).

2) QM 
Donn�es de la section transversale de mesure avec les colonnes suivantes:

MQ-ID15 - ID de la section transversale de mesure.
MQ-SHORT-NAME - Nom abr�g� de la section transversale de mesure.
POSITION - Nom de la rue.
POSITION-DETAIL - Description du tron�on routier.
DIRECTION - Objectif
ORIENTATION - Direction du voyage
X-GK4 - Coordonn�e en X (Gauss-Kr-ger-4)
Y-GK4 - coordonn�e Y (ciel gaussien)
AN-AHL-DET - Nombre de d�tecteurs appartenant � la section transversale de mesure.
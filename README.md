liens vedios: https://drive.google.com/drive/folders/1Zd9fIM0qbjTM7ebx1mn8ZMEeGf9FMxlv

# ProjetP1_Tri_Robot

## Description
Ce projet vise à développer un système robotisé automatisé en utilisant un bras robotique Kuka iiwa et une caméra Realsense pour la détection, le tri et la manipulation d'objets. Le système combine du code Python et Java pour effectuer la détection d'objets, la communication entre les logiciels, et le contrôle du robot. 

Le flux de travail principal inclut l'identification d'objets, l'estimation de leur pose et l'envoi des données pertinentes au robot via un protocole de communication TCP. Une fois les objets triés et manipulés, le robot envoie une commande de fin de tâche pour relancer un nouveau cycle de détection, permettant ainsi un fonctionnement automatisé.

## Matériels
- **Robotique** :
  - Kuka iiwa
  - Caméra Realsense
- **Programmation et logiciels** :
  - Java / Sunrise (pour le contrôle du robot)
  - Python 3 avec OpenCV et pyrealsense2 (pour le traitement d'image)
  - Visiocode (outil pour la gestion de la communication et des programmes)

## Fonctionnalités principales
1. **Détection des objets** : Le programme Python utilise la caméra Realsense pour identifier les formes (cubes, cylindres, etc.) et les couleurs spécifiques des objets.
2. **Estimation de la pose** : Les coordonnées XYZ, la couleur, la forme et l'angle de rotation des objets sont calculés.
3. **Transmission des données via TCP** : Les données sont envoyées au robot Kuka via Java/Sunrise, incluant les informations sur les objets (position, forme, couleur, angle).
4. **Réception des commandes du robot** : Un script Python est automatiquement lancé pour recevoir les instructions de fin de programme envoyées par le robot Kuka. Une fois la tâche terminée, il redémarre le processus de détection, permettant l'automatisation du tri des objets.
5. **Calibration des coordonnées** : Les coordonnées des objets par rapport à la caméra sont transformées en coordonnées relatives au bras robotique via un code de calibration.
6. **Interface utilisateur** : Une interface permet aux utilisateurs humains de sélectionner manuellement la priorité de traitement des objets selon leur couleur ou type, avant que le programme ne réalise les tâches de tri en conséquence.
7. **Automatisation** : Sauf l'interface utilisateur. Tout le processus est automatisé, avec des cycles continus de détection et manipulation d'objets, déclenchés par des messages TCP entre le robot et le programme Python.

## Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton_nom_utilisateur/ProjetP1_Tri_Robot.git

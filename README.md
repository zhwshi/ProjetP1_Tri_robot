liens vedios: https://drive.google.com/drive/folders/1Zd9fIM0qbjTM7ebx1mn8ZMEeGf9FMxlv

# ProjetP1_Tri_Robot

## Description
Ce projet consiste à développer un système robotisé utilisant un bras robotique Kuka iiwa et une caméra Realsense pour détecter et manipuler des objets. Le traitement d'image et la détection des objets sont réalisés avec Python 3 et OpenCV, tandis que la communication avec le robot se fait via le logiciel de programmation Sunrise et le langage Java.

## Matériels
- **Robotique** :
  - Kuka iiwa
  - Caméra Realsense
- **Programmation et logiciels** :
  - Java / Sunrise (pour le contrôle du robot)
  - Python 3 avec OpenCV et pyrealsense2 (pour le traitement d'image)
  - Visiocode (outil pour la gestion de la communication et des programmes)

## Fonctionnalités principales
1. **Détection des objets** : Identification de formes (cubes, cylindres, etc.) et couleurs spécifiques à l'aide de la caméra Realsense.
2. **Estimation de la pose** : Calcul des coordonnées (XYZ) des objets détectés.
3. **Envoi des données via TCP** : Transfert des informations sur les objets détectés au robot pour exécution des actions.
4. **Calcul et affichage de l'angle de rotation** : Pour les objets de forme carrée, le système calcule l'angle de rotation.

## Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton_nom_utilisateur/ProjetP1_Tri_Robot.git

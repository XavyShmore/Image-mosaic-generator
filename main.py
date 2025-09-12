import os
import random
from PIL import Image

def creer_mosaique_aleatoire(dossier_images, n, taille_image=(200, 200)):
    """
    Génère une mosaïque d'images de n x n à partir d'un dossier.

    Args:
        dossier_images (str): Le chemin vers le dossier contenant les images.
        n (int): La dimension de la grille (n x n).
        taille_image (tuple): La taille (largeur, hauteur) de chaque image dans la mosaïque.
    """

    # --- 1. Récupérer les chemins des images ---
    try:
        fichiers_images = [f for f in os.listdir(dossier_images) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]
        if not fichiers_images:
            print(f"❌ Aucun fichier image trouvé dans le dossier '{dossier_images}'.")
            return
            
        chemins_images = [os.path.join(dossier_images, f) for f in fichiers_images]
        
    except FileNotFoundError:
        print(f"❌ Le dossier '{dossier_images}' n'a pas été trouvé.")
        return

    # --- 2. Mélanger les images de manière aléatoire ---
    random.shuffle(chemins_images)
    
    # S'assurer qu'on a assez d'images pour remplir la grille
    nombre_images_necessaires = n * n
    if len(chemins_images) < nombre_images_necessaires:
        print(f"⚠️ Attention : Pas assez d'images ({len(chemins_images)}) pour remplir une grille de {n}x{n}.")
        # On complète la liste en réutilisant les images disponibles
        chemins_images = (chemins_images * (nombre_images_necessaires // len(chemins_images) + 1))
    
    # Sélectionner le bon nombre d'images
    images_selectionnees = chemins_images[:nombre_images_necessaires]

    # --- 3. Créer la toile pour la mosaïque ---
    largeur_mosaique = n * taille_image[0]
    hauteur_mosaique = n * taille_image[1]
    mosaique = Image.new('RGB', (largeur_mosaique, hauteur_mosaique))
    
    print(f"Création d'une mosaïque de {n}x{n}...")

    # --- 4. Parcourir et coller chaque image ---
    index_image = 0
    for i in range(n):  # Lignes
        for j in range(n):  # Colonnes
            try:
                # Ouvrir l'image
                img = Image.open(images_selectionnees[index_image])
                
                # Redimensionner l'image pour qu'elle s'adapte à la case
                img = img.resize(taille_image, Image.Resampling.LANCZOS)
                
                # Calculer la position où coller l'image
                position_x = j * taille_image[0]
                position_y = i * taille_image[1]
                
                # Coller l'image sur la toile
                mosaique.paste(img, (position_x, position_y))
                
                index_image += 1
            except Exception as e:
                print(f"Erreur lors du traitement de l'image {images_selectionnees[index_image]}: {e}")
                index_image += 1
                continue

    # --- 5. Sauvegarder l'image finale ---
    nom_fichier_sortie = 'mosaique.png'
    mosaique.save(nom_fichier_sortie)
    print(f"✅ Mosaïque sauvegardée avec succès sous le nom '{nom_fichier_sortie}' !")
    # Optionnel: afficher l'image
    # mosaique.show()


# --- Configuration ---
if __name__ == "__main__":
    # Nom du dossier où se trouvent vos images
    # Assurez-vous que ce dossier existe et se trouve au même endroit que le script,
    # ou fournissez un chemin complet (ex: "C:/Users/VotreNom/Images")
    dossier_source = "images" 
    
    while True:
        try:
            # Demander à l'utilisateur la taille de la grille
            dimension_n = int(input("Entrez la dimension de la mosaïque (ex: 3 pour une grille 3x3) : "))
            if dimension_n > 0:
                break
            else:
                print("Veuillez entrer un nombre entier positif.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")

    # Lancer la fonction de création
    creer_mosaique_aleatoire(dossier_source, dimension_n)
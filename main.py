import os
import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def creer_mosaique_aleatoire(dossier_images, n, taille_image=(200, 200)):
    """
    Génère une mosaïque d'images de n x n à partir d'un dossier.
    Retourne un objet PIL Image ou None si une erreur survient.
    """
    try:
        fichiers_images = [f for f in os.listdir(dossier_images) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))]
        if not fichiers_images:
            messagebox.showerror("Erreur", f"Aucun fichier image trouvé dans le dossier '{dossier_images}'.")
            return None
            
        chemins_images = [os.path.join(dossier_images, f) for f in fichiers_images]
        
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le dossier '{dossier_images}' n'a pas été trouvé.")
        return None

    random.shuffle(chemins_images)
    
    nombre_images_necessaires = n * n
    if len(chemins_images) < nombre_images_necessaires:
        chemins_images = (chemins_images * (nombre_images_necessaires // len(chemins_images) + 1))
    
    images_selectionnees = chemins_images[:nombre_images_necessaires]

    largeur_mosaique = n * taille_image[0]
    hauteur_mosaique = n * taille_image[1]
    mosaique = Image.new('RGB', (largeur_mosaique, hauteur_mosaique))
    
    index_image = 0
    for i in range(n):
        for j in range(n):
            try:
                img = Image.open(images_selectionnees[index_image])
                img = img.resize(taille_image, Image.Resampling.LANCZOS)
                position_x = j * taille_image[0]
                position_y = i * taille_image[1]
                mosaique.paste(img, (position_x, position_y))
                index_image += 1
            except Exception as e:
                print(f"Erreur lors du traitement de l'image {images_selectionnees[index_image]}: {e}")
                index_image += 1
                continue
    return mosaique

class MosaicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Mosaïque")
        self.root.geometry("800x600")

        self.dossier_source = ""
        self.image_mosaique = None
        self.image_preview = None

        # --- Frame pour les contrôles ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Sélection du dossier
        ttk.Button(control_frame, text="Sélectionner un dossier d'images", command=self.selectionner_dossier).pack(side=tk.LEFT, padx=5)
        self.label_dossier = ttk.Label(control_frame, text="Aucun dossier sélectionné")
        self.label_dossier.pack(side=tk.LEFT, padx=5)

        # Taille de la mosaïque
        ttk.Label(control_frame, text="Taille de la mosaique (NxN):").pack(side=tk.LEFT, padx=(20, 5))
        self.spinbox_n = ttk.Spinbox(control_frame, from_=1, to=20, width=5)
        self.spinbox_n.set(3)
        self.spinbox_n.pack(side=tk.LEFT, padx=5)

        # Taille des images
        ttk.Label(control_frame, text="Taille image (px):").pack(side=tk.LEFT, padx=(20, 5))
        self.spinbox_img_w = ttk.Spinbox(control_frame, from_=50, to=500, width=5, increment=10)
        self.spinbox_img_w.set(200)
        self.spinbox_img_w.pack(side=tk.LEFT, padx=2)
        ttk.Label(control_frame, text="x").pack(side=tk.LEFT, padx=2)
        self.spinbox_img_h = ttk.Spinbox(control_frame, from_=50, to=500, width=5, increment=10)
        self.spinbox_img_h.set(200)
        self.spinbox_img_h.pack(side=tk.LEFT, padx=5)

        # Boutons d'action
        ttk.Button(control_frame, text="Générer", command=self.previsualiser).pack(side=tk.LEFT, padx=5)
        self.bouton_sauvegarder = ttk.Button(control_frame, text="Sauvegarder", command=self.sauvegarder, state=tk.DISABLED)
        self.bouton_sauvegarder.pack(side=tk.LEFT, padx=5)

        # --- Frame pour la prévisualisation ---
        preview_frame = ttk.Frame(root, padding="10")
        preview_frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(preview_frame, bg="gray")
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def selectionner_dossier(self):
        self.dossier_source = filedialog.askdirectory(title="Sélectionnez le dossier contenant les images")
        if self.dossier_source:
            self.label_dossier.config(text=os.path.basename(self.dossier_source))
        else:
            self.label_dossier.config(text="Aucun dossier sélectionné")

    def previsualiser(self):
        if not self.dossier_source:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un dossier d'images.")
            return

        try:
            n = int(self.spinbox_n.get())
            img_w = int(self.spinbox_img_w.get())
            img_h = int(self.spinbox_img_h.get())
            if n <= 0 or img_w <= 0 or img_h <= 0:
                raise ValueError
            taille_image = (img_w, img_h)
        except ValueError:
            messagebox.showerror("Erreur", "Les tailles doivent être des nombres entiers positifs.")
            return

        self.image_mosaique = creer_mosaique_aleatoire(self.dossier_source, n, taille_image)

        if self.image_mosaique:
            # Redimensionner pour l'aperçu
            w, h = self.image_mosaique.size
            max_size = 500
            if w > h:
                new_w = max_size
                new_h = int(h * max_size / w)
            else:
                new_h = max_size
                new_w = int(w * max_size / h)
            
            img_resized = self.image_mosaique.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.image_preview = ImageTk.PhotoImage(img_resized)
            
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, anchor=tk.CENTER, image=self.image_preview)
            self.bouton_sauvegarder.config(state=tk.NORMAL)

    def sauvegarder(self):
        if not self.image_mosaique:
            messagebox.showerror("Erreur", "Aucune mosaïque à sauvegarder. Veuillez d'abord en générer une.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Sauvegarder la mosaïque"
        )
        if filepath:
            try:
                self.image_mosaique.save(filepath)
                messagebox.showinfo("Succès", f"Mosaïque sauvegardée avec succès sous:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erreur de sauvegarde", f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicApp(root)
    root.mainloop()
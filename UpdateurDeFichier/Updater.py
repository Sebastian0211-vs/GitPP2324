import subprocess

chemin_fichier = "test.py"
chemin_fichier_tmp = "tmp" + chemin_fichier
chemin_fichier_ajout = ""

subprocess.run(f"cp {chemin_fichier} {chemin_fichier_tmp}")

def writeFile(chemin_fichier, chemin_fichier_tmp, line_number):
    with open(chemin_fichier_tmp, "w") as fichier_tmp, open(chemin_fichier, "r") as fichier, open(chemin_fichier_ajout, "r") as fichier_ajout:
        for i, ligne in enumerate(fichier, start=1):
            fichier_tmp.write(ligne)
            if i == line_number:
                for ajout_ligne in fichier_ajout:
                    fichier_tmp.write(ajout_ligne)
        for ligne in fichier:
            fichier_tmp.write(ligne)
    subprocess.run(f"mv {chemin_fichier_tmp} {chemin_fichier}")


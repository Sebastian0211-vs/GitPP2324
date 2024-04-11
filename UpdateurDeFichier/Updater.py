import subprocess

chemin_fichier = "test.py"
chemin_fichier_tmp = "tmp" + chemin_fichier
chemin_fichier_ajout = ""

subprocess.run(f"cp {chemin_fichier} {chemin_fichier_tmp}")

def writeFile(chemin_fichier, chemin_fichier_tmp):
    with open(chemin_fichier_tmp, "w") as fichier_tmp, open(chemin_fichier, "r") as fichier, open(chemin_fichier_ajout, "r") as fichier_ajout:
        for ligne in fichier:
            fichier_tmp.write(ligne)
        for ligne in fichier_ajout:
            fichier_tmp.write(ligne)

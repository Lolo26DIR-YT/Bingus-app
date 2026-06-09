# 🛠️ Guide de Développement & Compilation (Bingus App)

Ce guide rassemble toutes les commandes utiles pour compiler rapidement l'application en fichier exécutable `.exe` sans avoir à retaper toutes les options de PyInstaller.

---

## 🚀 1. Recompiler l'application en `.exe`

Comme le fichier `bingus_hack_panel.spec` est déjà généré à la racine, tu as juste à exécuter cette commande unique dans ton terminal (VS Code ou PowerShell) :

```powershell
python -m PyInstaller bingus_hack_panel.spec ; Move-Item -Path .\dist\bingus_hack_panel.exe -Destination .\ -Force
```
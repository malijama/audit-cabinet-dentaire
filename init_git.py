#!/usr/bin/env python3
import subprocess
import os

def init_git_repository():
    print("🔧 Initialisation du repository Git")
    print("=" * 50)
    
    try:
        # Initialiser Git
        subprocess.run(['git', 'init'], check=True)
        print("✅ Repository Git initialisé")
        
        # Ajouter tous les fichiers
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Fichiers ajoutés au staging")
        
        # Premier commit
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Audit analytique cabinet dentaire'], check=True)
        print("✅ Premier commit effectué")
        
        print("\n🎉 Repository Git configuré avec succès !")
        print("\n📋 Prochaines étapes :")
        print("1. Créer un nouveau repository sur GitHub")
        print("2. Copier l'URL du repository")
        print("3. Exécuter : git remote add origin <votre-repo-url>")
        print("4. Exécuter : git push -u origin main")
        print("\n💡 Pour tester l'application :")
        print("   streamlit run streamlit_app.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation Git : {e}")
    except FileNotFoundError:
        print("❌ Git n'est pas installé sur votre système")
        print("💡 Installez Git depuis : https://git-scm.com/")

def show_project_structure():
    print("\n📁 Structure du projet :")
    print("=" * 30)
    
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if not file.startswith('.'):
                print(f"{subindent}{file}")

if __name__ == "__main__":
    init_git_repository()
    show_project_structure() 
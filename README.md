# python-projet-template

## 1. my_project
Description

## 2. Créer un environnement virtuel
```
python -m venv .venv # ou avec uv : uv venv
source .venv/bin/activate  # sous Windows : .venv\Scripts\activate
```

## 3. Installer les dépendances
```
pip install -e .
```

**TODO**
Refactoring
---

Nouvelle structure à mettre en place :
```markdown
src/
   db/
      base.py ✅         # Interface abstraite
      models.py ✅ [En cours] : modification du modele de routine
      adapters/
         postgres.py ✅
         sqlite.py
      repositories/
         user_repository.py ✅
         routine_repository.py ✅
         ...
   domain/
      models/          # Entités métier
         user.py ✅
         routine.py [En cours]
      services/        # ← Logique métier
         user_service.py
         routine_service.py [En cours]
         ...
      exceptions.py    # Exceptions personnalisées
   presentation/
      callbacks/
      pages/
      components/      # ← Composants UI réutilisables
      app.py
   config/
      settings.py ✅      # Centralise env.py et autres configs
      logger.py ✅
   tests/              # ← Ne pas oublier !
      unit/
      integration/
```

[En cours]
- Routine
   - Possibilité de modifier une routine. Si changement de type, alors message warning perte d'historique des données (à préciser)
   - Ajouter des explications sur la création des routines

[A faire]
- Ajouter une liste de tags à sélectionner sur les dialogs stat
- Ajouter la sélection d'icon sur dialogs stat
- dashboard
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
- Ajouter des classes dans domain/. L'idée est de structurer au maximum le code.
    - User(id, fisrtname, lastname, email, password, creation_date)
    - UserInfos(id, user_id, tags:list)
    - Stat(id, user_id, type[bool, int, float, str, list], tags, description, creation_date)
    - StatValue(id, stat_id, data:jsonb, update_date)

Nouvelle structure à mettre en place :
```markdown
src/
   db/
      base.py ✅         # Interface abstraite
      models.py
      adapters/
         postgres.py ✅
         sqlite.py     # Pour les tests
      repositories/    # ← IMPORTANT : couche métier/données
         user_repository.py ✅
         ...
   domain/
      models/          # Entités métier
         user.py ✅
         stat.py
      services/        # ← Logique métier
         user_service.py
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





- Créer une page de connexion utilisateur, avec la création d'un utilisateur

- Option de modification d'une stat
    - si changement de type, alors message warning perte d'historique des données (à préciser)

- Ajouter une liste de tags à sélectionner sur les dialogs stat
- Ajouter la sélection d'icon sur dialogs stat
- dashboard
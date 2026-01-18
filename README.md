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
- Créer une page de connexion utilisateur, avec la création d'un utilisateur
- Créer 3 tables 
    - User(user_id, name, tags, ?)
    - Stat_ref(ref_id, user_id, stat_id, type, ?)
    - Stats(stat_id, date, text, checkbox, feedback, multiselect, number_input, time_input)

- Option de modification d'une stat
    - si changement de type, alors message warning perte d'historique des données (à préciser)

- Ajouter une liste de tags à sélectionner sur les dialogs stat
- Ajouter la sélection d'icon sur dialogs stat
- dashboard
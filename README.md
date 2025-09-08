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

```
columns = st.columns(10)

icons = ["🍎", "🍌", "🍇", "🍓", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝"]

selected_icons = []

for index, column in enumerate(columns):
    with column:
        if button(icons[index], key=f"button_{index}"):
            selected_icons.append(icons[index])
```
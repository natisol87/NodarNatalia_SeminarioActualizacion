# Clase 3 · Problemas frecuentes con Git y GitHub

Actividad de la Clase 3: contar cómo se resolvió cada situación de la clase. No hay código para correr: esta carpeta explica tres problemas que aparecen al subir un proyecto a GitHub, qué los causa y cómo se resuelven.

---

## 1. README duplicado

**Qué pasa:** el repositorio se creó en GitHub con la opción de agregar un README, y en la compu también había un `README.md`. Eso deja dos historias distintas del mismo proyecto: una en GitHub y otra local. Al hacer `git push`, GitHub lo rechaza (`rejected ... fetch first`), porque tiene un commit que la compu no tiene.

**Cómo se resuelve:** primero se trae lo que está en GitHub y se une con lo local, y después se sube.

```bash
git pull origin main --allow-unrelated-histories
# si los dos README chocan, Git marca el conflicto: se edita el archivo,
# se deja una sola versión y se guarda
git add README.md
git commit -m "Une el README de GitHub con el local"
git push origin main
```

**Para que no pase:** crear el repositorio en GitHub **vacío** (sin README, sin `.gitignore` y sin licencia) cuando el proyecto ya existe en la compu.

---

## 2. Carpeta sin ignorar

**Qué pasa:** se subió a GitHub una carpeta que no tenía que subirse, por ejemplo el entorno virtual `.venv/` o `__pycache__/`. Pasa cuando se hace `git add .` antes de tener el `.gitignore`, o cuando la carpeta no estaba escrita en él. Agregarla al `.gitignore` después **no alcanza**: Git ya la está siguiendo.

**Cómo se resuelve:** se agrega la carpeta al `.gitignore` y se le dice a Git que la deje de seguir, sin borrarla de la compu.

```bash
# 1. Agregar la carpeta al .gitignore, por ejemplo la línea: .venv/
# 2. Sacarla del repositorio (queda en la compu)
git rm -r --cached .venv
git commit -m "Deja de versionar el entorno virtual"
git push
```

**Para que no pase:** crear el `.gitignore` antes del primer `git add`, y revisar `git status` antes de cada commit.

---

## 3. Ramas `master` y `main`

**Qué pasa:** según la versión y la configuración, `git init` crea la rama principal con el nombre `master`, mientras que GitHub usa `main`. Al subir, queda una rama de cada nombre, o el push falla con `src refspec main does not match any` porque en la compu no existe ninguna rama llamada `main`.

**Cómo se resuelve:** se renombra la rama local a `main` y se sube esa.

```bash
git branch -M main
git push -u origin main
```

Si en GitHub quedó una rama `master` que sobra, se puede borrar con `git push origin --delete master`, una vez que todo está en `main`.

**Para que no pase:** configurar Git una vez para que siempre use `main`:

```bash
git config --global init.defaultBranch main
```

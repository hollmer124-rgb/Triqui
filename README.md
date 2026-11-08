# Triqui Neon Edition

El proyecto ofrece dos versiones del juego:

- `triqui.py`: versión de escritorio original con Tkinter y Pygame.
- `app.py`: versión web para dos jugadores, compatible con el runtime Python de Vercel.

## Probar localmente

Se requiere Python 3.12 o posterior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app app run --debug
```

Abre la dirección local que muestra Flask. La versión web se juega con dos personas en el mismo navegador; los nombres y el marcador se mantienen en el navegador durante la sesión.

## Desplegar en Vercel

1. Sube estos archivos a la raíz del repositorio y conéctalo con Vercel, o importa el repositorio desde el panel de Vercel.
2. Deja **Root Directory** en la raíz del proyecto. No se necesita un comando de build ni variables de entorno.
3. Vercel detectará Flask desde `requirements.txt` y cargará `app:app`, declarado en `pyproject.toml`.
4. Pulsa **Deploy**. Cada solicitud sirve la interfaz web desde `templates/index.html`.

La versión de escritorio necesita ventanas gráficas y no se ejecuta en Vercel; para el despliegue se usa la versión web incluida.

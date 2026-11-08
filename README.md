# Triqui Neon Edition

El proyecto ofrece dos versiones del juego:

- `triqui.py`: versión de escritorio original con Tkinter y Pygame.
- `index.html`: versión web para dos jugadores, servida como sitio estático.

## Probar localmente

Puedes abrir `index.html` directamente en el navegador o servirlo localmente:

```powershell
python -m http.server 8000
```

Luego abre `http://localhost:8000`. La versión web se juega con dos personas en el mismo navegador; los nombres y el marcador se mantienen en el navegador durante la sesión.

## Desplegar en Vercel

1. Sube los cambios al repositorio conectado a Vercel.
2. En **Settings → Build and Deployment**, deja **Framework Preset** en **Other**, **Root Directory** en la raíz del proyecto y los comandos de build vacíos.
3. Pulsa **Redeploy** en el último deployment para publicar estos cambios.

`vercel.json` desactiva la detección automática de frameworks. Vercel sirve `index.html` directamente, sin funciones Python, dependencias ni comando de build.

La versión de escritorio necesita ventanas gráficas y no se ejecuta en Vercel; para el despliegue se usa la versión web incluida.

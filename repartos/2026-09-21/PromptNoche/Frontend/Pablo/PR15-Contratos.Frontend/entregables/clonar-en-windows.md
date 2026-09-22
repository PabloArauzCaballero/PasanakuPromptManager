# Clonar el monorepo en Windows sin que falle por rutas largas — H2.S1.M7

```bash
git config core.longpaths true
git clone https://github.com/PabloArauzCaballero/PasanakuBackend.git
```

`docs/Modelos/**` tiene rutas que superan los 260 caracteres del límite clásico de Windows;
sin `core.longpaths true`, el checkout falla a mitad de camino con `Filename too long` en esas
rutas específicas, no en `apps/`/`packages/`/`clientes/` (que este carril sí necesita).

Confirmado ya en una sesión anterior de este mismo turno (memoria del proyecto
`pasanaku-backend-repo`): el clon durable en esta máquina
(`Entrypoint-GitHUb/Pasanaku/PasanakuBackend`) se hizo con esta configuración. No hace falta
`git config --global`: alcanza con setearlo antes del `clone`, o `--config core.longpaths=true`
en el propio comando si se prefiere no tocar la config global de la máquina.

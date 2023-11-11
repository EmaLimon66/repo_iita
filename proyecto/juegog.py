from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import uniform

app = Ursina()

# Suelo superior
suelo = Entity(model='plane',
               texture='grass',
               collider='mesh',
               scale=(50, 1, 50))
suelo.y = 1 

# Suelo inferior (debajo del suelo)
suelo_inferior = Entity(model='plane',
                        texture='grass',
                        collider='box',
                        scale=(75, 1, 75))
suelo_inferior.y = suelo.y - 10  
suelo_inferior.color = color.clear  

jugador = FirstPersonController(collider='box')
jugador.cursor.visible = False

cielo = Sky(texture='sky_sunset')
nivel = 1

posicion_inicial = jugador.position  # Guarda la posición inicial del jugador

bloques = []
direcciones = []
window.fullscreen = True
for i in range(10):
    r = uniform(-2, 2)
    bloque = Entity(
        position=(r, 1 + i, 3 + i * 5),
        model='cube',
        texture='white_cube',
        color=color.azure,
        scale=(3, 0.5, 3),
        collider='box',
    )
    bloques.append(bloque)
    if r < 0:
        direcciones.append(1)
    else:
        direcciones.append(-1)

objetivo = Entity(
    color=color.gold,
    model='cube',
    texture='white_cube',
    position=(0, 11, 55),
    scale=(10, 1, 10),
    collider='box'
)
columna = Entity(
    color=color.green,
    model='cube',
    position=(0, 36, 58),
    scale=(1, 50, 1)
)

salto = Audio(
    'assets/salto.mp3',
    loop=False,
    autoplay=False
)

caminar = Audio(
    'assets/camino.mp3',
    loop=False,
    autoplay=False
)

pausa = False

menu_continuar = Button(
    text='Continuar',
    scale=0.1,
    color=color.azure,
    highlight_color=color.lime,
    pressed_color=color.olive,
    x=0,
    y=0.1,
    enabled=False
)

menu_salir = Button(
    text='Salir',
    scale=0.1,
    color=color.azure,
    highlight_color=color.lime,
    pressed_color=color.olive,
    x=0,
    y=-0.1,
    enabled=False
)

def mostrar_menu():
    global pausa
    pausa = True
    menu_continuar.enabled = True
    menu_salir.enabled = True
    jugador.cursor.locked = False

def ocultar_menu():
    global pausa
    pausa = False
    menu_continuar.enabled = False
    menu_salir.enabled = False
    jugador.cursor.locked = True

def salir_del_juego():
    application.quit()

def update():
    global nivel, pausa
    if not pausa:
        i = 0
        for bloque in bloques:
            bloque.x -= direcciones[i] * time.dt
            if abs(bloque.x) > 5:
                direcciones[i] *= -1
            if bloque.intersects().hit:
                jugador.x -= direcciones[i] * time.dt
            i = i + 1
        if jugador.z > 56 and nivel == 1:
            nivel = 2
            cielo.texture = 'sky_sunset'
        caminando = held_keys['a'] or \
                    held_keys['d'] or \
                    held_keys['w'] or \
                    held_keys['s']
        if caminando and jugador.grounded:
            if not caminar.playing:
                caminar.play()
        else:
            if caminar.playing:
                caminar.stop()
        
        if jugador.y < suelo_inferior.y + 1:
            jugador.position = posicion_inicial  # Reposiciona al jugador en la posición inicial si cae por debajo del suelo inferior

def input(key):
    global pausa
    if key == 'escape':
        if not pausa:
            mostrar_menu()
        else:
            ocultar_menu()

app.run()

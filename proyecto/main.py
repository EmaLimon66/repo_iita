from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina(borderless=False)

Jugador = FirstPersonController()

vida = 50.0
vida_barra = Entity(parent=camera.ui, model='quad', scale_x=vida / 100, scale_y=0.025, color=color.blue, x=-0.50, y=-0.45)

Sky()

Tierra = Entity(model='plane', collider='box', texture='cesped.jpg', scale=200)
Tierra.position = Vec3(0, 0, 0)

# Guardar la posición inicial del jugador
posicion_inicial_jugador = Jugador.position

# Agregar árboles aleatorios encima del suelo
for i in range(100): 
    x = random.uniform(-100, 100)
    z = random.uniform(-100, 100)
    y = Tierra.position.y

    Arbol = Entity(
        model='Arbol1.obj',
        scale=1,
        position=(x, y, z),
        color=color.brown,
    )

# Colisionador debajo del plano
colisionador_abajo = Entity(model='quad', scale=(200, 1), position=(0, -10, 0), collider='box')

Enemigo = Entity(
    model='cube',
    texture='ojos_enojados.jpg',
    scale=2,
    position=(30, 1, 40),
    color=color.red,
    collider='box'
)

Enemigo2 = Entity(
    model='cube',
    texture='ojos_enojados.jpg',
    scale=2,
    position=(60, 1, 50),
    color=color.red,
    collider='box'
)

# Inicializa Arma en el suelo
Arma = Entity(
    model='cube',
    texture='cesped.jpg',
    scale=1,
    position=(random.uniform(-100, 100), Tierra.position.y + 0.5, random.uniform(-100, 100))
)

# Generar cubo de ganar alejado
cubo_ganar = Entity(
    model='cube',
    color=color.green,
    scale=2,
    position=(random.uniform(-100, 100), 1, random.uniform(-100, 100)),  # Posición aleatoria
    collider='box'
)

# Texto de ganaste
texto_ganaste = Text(
    text='¡Ganaste!',
    origin=(0, 0),  # Alineación del texto al centro
    scale=2,
    background=True,
    color=color.lime,
    enabled=False
)

# Botones para salir o volver a jugar
boton_salir = Button(
    text='Salir',
    scale=0.1,
    color=color.azure,
    highlight_color=color.lime,
    pressed_color=color.olive,
    x=0,
    y=0.1,
    enabled=False
)

boton_volver_a_jugar = Button(
    text='Volver a Jugar',
    scale=0.1,
    color=color.azure,
    highlight_color=color.lime,
    pressed_color=color.olive,
    x=0,
    y=-0.1,
    enabled=False
)

def Enemigo_Seguirme2():
    Direccion_Al_Jugador = Jugador.position - Enemigo2.position
    Direccion_Al_Jugador.y = 0
    Direccion_Al_Jugador.normalize()
    Velocidad_Enemigo = 4.5
    Enemigo2.position += Direccion_Al_Jugador * Velocidad_Enemigo * time.dt
    Enemigo2.position.y = 0

def Enemigo_Seguirme():
    Direccion_Al_Jugador = Jugador.position - Enemigo.position
    Direccion_Al_Jugador.y = 0
    Direccion_Al_Jugador.normalize()
    Velocidad_Enemigo = 4.5
    Enemigo.position += Direccion_Al_Jugador * Velocidad_Enemigo * time.dt
    Enemigo.position.y = 0

def Ataque_Enemigo():
    global vida
    distance = (Jugador.position - Enemigo.position).length()
    if distance < 1.0:
        if vida > 0:
            vida -= 0.4
            vida_barra.scale_x = vida / 100
            if vida <= 0:
                application.quit()

Jugador.cursor.visible = False

# Variable para controlar el estado de pausa
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
    Jugador.cursor.locked = False
    Jugador.enabled = False

def ocultar_menu():
    global pausa
    pausa = False
    menu_continuar.enabled = False
    menu_salir.enabled = False
    Jugador.cursor.locked = True
    Jugador.enabled = True

def salir_del_juego():
    application.quit()

def volver_a_jugar():
    global pausa, vida
    pausa = False
    vida = 50.0
    vida_barra.scale_x = vida / 100
    Jugador.position = posicion_inicial_jugador
    texto_ganaste.enabled = False
    boton_salir.enabled = False
    boton_volver_a_jugar.enabled = False
    Jugador.cursor.visible = False

def input(key):
    global pausa
    if key == 'escape':
        if not pausa:
            mostrar_menu()
        else:
            ocultar_menu()

def continuar():
    global pausa
    ocultar_menu()

menu_continuar.on_click = continuar
menu_salir.on_click = salir_del_juego
boton_volver_a_jugar.on_click = volver_a_jugar

def verificar_ganar():
    global pausa
    distance = (Jugador.position - cubo_ganar.position).length()
    if distance < 2.0:
        pausa = True
        texto_ganaste.enabled = True
        boton_salir.enabled = True
        boton_volver_a_jugar.enabled = True
        Jugador.cursor.locked = True

def update():
    global Arma

    if not pausa:
        Enemigo_Seguirme()
        Ataque_Enemigo()
        Enemigo_Seguirme2()
        verificar_ganar()

        # Verifica si el jugador ha caído debajo del plano
        if Jugador.y < -10:
            Jugador.position = posicion_inicial_jugador  # Reposiciona al jugador en la posición inicial

app.run()

import streamlit as st
#Lo que hacemos es importar y luego "as" abrevia como "st" en vez de poner streamlit
import requests

RIOT_API_KEY= st.secrets["RIOT_API_KEY"]

if "puuid" not in st.session_state:
    st.session_state["puuid"] = None

st.set_page_config(
    page_title="LoL Analyzer",
    page_icon="⚔️",
    layout="wide"
)
#Set_page_config es literalemente como el estandar para la pagina digamos, como el titulo que aperece
#el icono que sale en el navegador y el modo de vista Como "ultra Wide"
st.title("LoL Analyzer")

st.write("Analiza tus partidas de League Of Legends con datos oficiales de Riot Games")

#Agrega una barra lateral y le agrega el titulo que colocamos 
st.sidebar.title("LoL Analyzer")

seccion = st.sidebar.radio(
    "Navegación",
    ["Perfil",
     "Partidas",
     "Análisis",
     "Timeline"]
)

if seccion == "Perfil":
    st.header("Perfil del jugador")
    #Aquí estamos diciendo que de la barra lateral es igual a perfil, en la app se vera como titulo
    #Perfil de jugador y si seleccionamos otro no dira nada porque aun no lo definimos
    
    
# Crea los campos de texto y guarda lo que escriba el usuario
# en las variables game_name y tag_line
    game_name = st.text_input(
        "Riot ID",
        placeholder="Ejemplo: Arkan Dïsléxico"
    )
    tag_line = st.text_input(
        "Tag",
        placeholder="Ejemplo: LAN"
    )
 # Crea el botón "Buscar Jugador".
# buscar será True cuando el usuario presione el botón

    buscar = st.button(
        "Buscar Jugador",
        type="primary"
    )
    # Si se presiona el botón, comprueba que ambos campos tengan información

    if buscar:   
        
         # Si Riot ID O Tag están vacíos, muestra una advertencia
        if game_name == "" or tag_line == "":
                st.warning("Escribe tu Riot ID y tu Tag.")
                
         # Si ambos campos tienen información, continúa con la búsqueda
        else:
                st.write("Buscando jugador...")
                url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
                  #Aquí estamos utilizando un f-string es decir metemos una variable en este caso game_name y tag name
                  #para hacer un URL funcional 
                # "..."       string normal
                # f"...{x}..." string que puede insertar variables/expresiones
                
                respuesta = requests.get(
                    url,
                    headers={"X-Riot-Token": RIOT_API_KEY}
                )
                #get se utiliza para hacer una consulta o pedir información
                st.write(respuesta.status_code)
                # Muestra el código de estado HTTP de la respuesta.
                # 200 significa que la petición a Riot se realizó correctamente.
                datos = respuesta.json()
                # Convierte la respuesta JSON de Riot a datos que Python puede manejar.
                # En este caso, el resultado se guarda como un diccionario en la variable "datos".
                st. write(datos)
                # Muestra en pantalla todos los datos que Riot devolvió
                # después de convertir la respuesta JSON a un diccionario de Python.
                st.write(datos["gameName"])
                # Accede únicamente al valor de la clave "gameName"
                # del diccionario datos y muestra el nombre del jugador.
                st.session_state["puuid"]= datos["puuid"]
                # Obtiene el PUUID del diccionario recibido de Riot y lo guarda
                # en session_state para conservarlo al cambiar entre secciones de la app.

elif seccion == "Partidas":
    st.header("Historial de partidas")
    if st.session_state["puuid"] is None:
        st.warning("Primero Busca un jugador en la sección de Perfil")
    
    else:  
        st.write("Jugador cargado correctamente.")
        puuid = st.session_state["puuid"]
        url_partidas = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        
        respuesta_partidas = requests.get(
            url_partidas,
            headers={"X-Riot-Token": RIOT_API_KEY}
        )
        st.write(respuesta_partidas.status_code)
        #nos regresa el estatus en pantalla de el historial de partidas 
        datos_partida = respuesta_partidas.json()
        # Convierte la respuesta JSON a datos de Python
        # y guarda los IDs de las partidas en la variable "partidas"
        partidas = respuesta_partidas.json()
        #definimos la variable para hacerla mas entendible
        
        
        # Muestra en pantalla la lista completa de IDs de partidas
        # que Riot devolvió anteriormente.
        #st.write(partidas)
        # Recorre uno por uno todos los IDs que existen dentro de la lista "partidas".
        # En cada vuelta, el ID actual se guarda temporalmente en "partida_id".
        for partida_id in partidas:
            #st.write(partida_id)
             # Construye la URL para consultar los datos completos de la partida actual.
            # Al ser un f-string, {partida_id} cambia en cada vuelta del for.
            url_detalle = f"https://americas.api.riotgames.com/lol/match/v5/matches/{partida_id}"
            respuesta_detalle = requests.get(
                url_detalle,
                headers={"X-Riot-Token": RIOT_API_KEY}
            )
            #st.write(respuesta_detalle.status_code)
            #nos regresa el estatos de cada partida estamos combinando respuesta_detalle =request.get de arriba
            detalle_partida = respuesta_detalle.json()
            participantes = detalle_partida["info"]["participants"]
            #Aquí "Jugador" es nuestro diccinario dentro de el existen los datos de kda y nombre del champ
            for jugador in participantes:
                if jugador["puuid"] == puuid:
                    champion_name = jugador["championName"]
                    imagen_champion = f"https://ddragon.leagueoflegends.com/cdn/16.15.1/img/champion/{champion_name}.png"
                    
                    with st.container():
                        col1, col2, col3 = st.columns(3)
                        
                        col1.subheader(champion_name)
                        col1.image(imagen_champion, width=80)

                    #DATOS BÁSICOS DEL JUGADOR
                    kills = jugador["kills"]
                    deaths = jugador["deaths"]
                    assists = jugador["assists"]
                    victoria = jugador["win"]
                    team_id = jugador["teamId"]

                    #DURACIÓN DE LA PARTIDA
                    duracion = detalle_partida["info"]["gameDuration"]
                    duracion_minutos = round(duracion / 60, 2)

                    #FARMEO
                    minioms = jugador["totalMinionsKilled"]
                    monstruos = jugador["neutralMinionsKilled"]
                    cs = minioms + monstruos
                    cs_por_minuto = round(cs / duracion_minutos, 2)

                    #ORO
                    gold = jugador["goldEarned"]
                    gold_minuto = round(gold / duracion_minutos, 2)

                    #DAÑO A CAMPEONES
                    damage = jugador["totalDamageDealtToChampions"]
                    damage_minuto = round(damage / duracion_minutos, 2)

                    #DAÑO
                    damage_torres = jugador["damageDealtToTurrets"]

                    #VISIÓN
                    vision_score = jugador["visionScore"]
                    wards = jugador["wardsPlaced"]
                    wards_minuto = round(wards / duracion_minutos, 2)
                    vision_minuto = round(vision_score / duracion_minutos, 2)

                    #KILLS TOTALES DE NUESTRO EQUIPO
                    kills_equipo = 0
                    for companero in participantes:
                        if companero["teamId"] == team_id:
                            kills_equipo += companero["kills"]

                    #KILL PARTICIPATION
                    if kills_equipo > 0:
                        kp = round((kills + assists) / kills_equipo * 100, 2)
                    else:
                        kp = 0

                    #============================================================
                    # MOSTRAR DATOS EN PANTALLA 
                    #============================================================
                    with st.container():
                        col1, col2, col3 = st.columns(3)
                        # Aquí usamos f-strings para combinar las variables de arriba en KDA, ORO, DAÑO ETC...
                        col1.write(f"KDA: {kills} / {deaths} / {assists}")
                        col1.write(f"CS: {cs}")
                        col1.write(f"CS/min: {cs_por_minuto}")
                        col1.write(f"Oro: {gold}")
                        col1.write(f"Oro/min: {gold_minuto}")
                        col1.write(f"Daño a campeones: {damage}")
                        col2.write(f"Daño/min: {damage_minuto}")
                        col2.write(f"Daño a torres: {damage_torres}")
                        col2.write(f"Visión Score: {vision_score}")
                        col2.write(f"Wards/min: {wards_minuto}")
                        col2.write(f"Vision/min: {vision_minuto}")
                        col3.write(f"Wards colocados: {wards}")
                        col3.write(f"Kill Participation: {kp}%")

                        if victoria:
                            col3.success("resultado: Victoria")
                        else:
                            col3.error("resultado: Derrota")

                    st.divider()
                    
            
elif seccion == "Análisis":
    st.header("Análisis de rendimiento")
    
elif seccion == "Timeline":
    st.header("Timeline de partidas")

#elif nos sirve como condicional, si "if" no se cumple compruba la siguiente si hicieramos 4 ifs 
#comprobaria todos los resultados


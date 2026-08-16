import streamlit as st
#Lo que hacemos es importar y luego "as" abrevia como "st" en vez de poner streamlit
import requests
import base64

RIOT_API_KEY= st.secrets["RIOT_API_KEY"]

if "puuid" not in st.session_state:
    st.session_state["puuid"] = None

st.set_page_config(
    page_title="LoL Analyzer",
    page_icon="⚔️",
    layout="wide"
)

#Diccionario de hechizos de invocador

hechizos = {
    4: "Flash",
    14: "Ignite",
    12: "Teleport",
    7: "Heal",
    11: "Smite",
    3: "Exhaust",
    1: "Cleanse",
    6: "Ghost",
    21: "Barrier",
}
#Diccionario de Imangenes de hechizos de invocador

imagenes_hechizos = {
    4: "SummonerFlash",
    14: "SummonerDot",
    12: "SummonerTeleport",
    7: "SummonerHeal",
    6: "SummonerHaste",
    3: "SummonerExhaust",
    21: "SummonerBarrier",
    1: "SummonerBoost",
    11: "SummonerSmite"
}

import streamlit as st
import requests
import base64

# ... API KEY ...
def poner_fondo(imagen):
    with open(imagen, "rb") as archivo:
        imagen_base64 = base64.b64encode(archivo.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.45)),
                url("data:image/jpg;base64,{imagen_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp p,
        .stApp label,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4 {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] div {{
            color: #222222 !important;
        }}
        
        [class*="st-key-partida_"] {{
            background: rgba(10, 10, 15, 0.58);
            backdrop-filter: blur(7px);
            -webkit-backdrop-filter: blur(7px);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 14px;
        }}        
        </style>
        """,
        unsafe_allow_html=True
    )

poner_fondo("Fondo.jpg")

# AQUÍ CONTINÚA TODO TU CÓDIGO COMO YA LO TENÍAS


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
                    
                    #DATOS BÁSICOS DEL JUGADOR
                    kills = jugador["kills"]
                    deaths = jugador["deaths"]
                    assists = jugador["assists"]
                    victoria = jugador["win"]
                    team_id = jugador["teamId"]
                    
                    #ITEMS
                    items = [
                        jugador["item0"],
                        jugador["item1"],
                        jugador["item2"],
                        jugador["item3"],
                        jugador["item4"],
                        jugador["item5"],
                        jugador["item6"],
                    ]
                    
                    #HECHIZOS DE INVOCADOR
                    hechizo1 = jugador["summoner1Id"]
                    hechizo2 = jugador["summoner2Id"]
                    #OBTENEMOS EL NOMBRE DEL HECHIZO USANDO EL DICCIONARIO DE HECHIZOS
                    nombre_hechizo1 = hechizos.get(hechizo1, "Desconocido")
                    nombre_hechizo2 = hechizos.get(hechizo2, "Desconocido")
                    #OBTENER EL NOMBBRE DE LA IMAGEN DE HECHIZOS
                    archivo_hechizo1 = imagenes_hechizos.get(hechizo1, "Desconocido")
                    archivo_hechizo2 = imagenes_hechizos.get(hechizo2, "Desconocido")
                    #URL DE LA IMAGEN DEL HECHIZO
                    imagen_hechizo1 = f"https://ddragon.leagueoflegends.com/cdn/16.15.1/img/spell/{archivo_hechizo1}.png"
                    imagen_hechizo2 = f"https://ddragon.leagueoflegends.com/cdn/16.15.1/img/spell/{archivo_hechizo2}.png"                   
                    

                    #DURACIÓN DE LA PARTIDA
                    duracion = detalle_partida["info"]["gameDuration"]
                    duracion_minutos = round(duracion / 60, 2)

                    #FARMEO
                    minioms = jugador["totalMinionsKilled"]
                    monstruos = jugador["neutralMinionsKilled"]
                    cs = minioms + monstruos
                    cs_por_minuto = round(cs / duracion_minutos, 2)

                    #OROc
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
                    with st.container(border=True,key=f"partida_{partida_id}"):
                        col1, col2, col3= st.columns([1.2,2,2])
                        # Aquí usamos f-strings para combinar las variables de arriba en KDA, ORO, DAÑO ETC...
                        
                        #CAMPEÓN 
                        with col1:
                            st.markdown(
                                f"<h3 style='margin-top: -17px; margin-bottom: 0px;'>{champion_name}</h3>",
                                unsafe_allow_html=True
                            )
                            champ_col, spells_col = st.columns([1,1.5])
                            
                            with champ_col:
                                st.image(imagen_champion, width=80)
                            
                            with spells_col:
                                st.image(imagen_hechizo1, width=32)
                                st.image(imagen_hechizo2, width=32)
                            st.caption(f"Duración: {duracion_minutos} min")
                            
                            #===============================================
                            #ITEMS Y RESULTADO
                            #==============================================
                            
                            items_col, resultado_col = st.columns([4.5, 1.5])
                            
                            # ITEMS
                            with items_col:

                                st.markdown(
                                    """
                                    <div style="
                                        font-size: 13px;
                                        font-weight: bold;
                                        color: #ffffff;
                                        margin-bottom: 6px;
                                    ">
                                        ITEMS:
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                                item_cols = st.columns(7)

                                for i, item_id in enumerate(items):

                                    with item_cols[i]:

                                        if item_id != 0:

                                            imagen_item = (
                                                f"https://ddragon.leagueoflegends.com/"
                                                f"cdn/16.15.1/img/item/{item_id}.png"
                                            )

                                            st.image(
                                                imagen_item,
                                                width=55
                                            )
                            
                                
                        
                        #DATOS PRINCIPALES
                        with col2:

                            # KDA
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#fbbf24; font-size:21px;">⚔</span>
                                    &nbsp;&nbsp;KDA:
                                    <span style="color:#4ade80;">{kills}</span> /
                                    <span style="color:#f87171;">{deaths}</span> /
                                    <span style="color:#60a5fa;">{assists}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # CS
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#c084fc; font-size:21px;">⚔</span>
                                    &nbsp;&nbsp;CS: {cs}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # CS POR MINUTO
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#60a5fa; font-size:21px;">◈</span>
                                    &nbsp;&nbsp;CS/min: {cs_por_minuto}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # KILL PARTICIPATION
                            st.markdown(
                                f"""
                                <div style="
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#4ade80; font-size:21px;">◎</span>
                                    &nbsp;&nbsp;KP: {kp}%
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        # ECONOMIA Y DAÑO
                        with col3:

                            # ORO
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#fbbf24; font-size:21px;">●</span>
                                    &nbsp;&nbsp;Oro: {gold}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # ORO POR MINUTO
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#f59e0b; font-size:21px;">◆</span>
                                    &nbsp;&nbsp;Oro/min: {gold_minuto}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # DAÑO
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#f87171; font-size:21px;">✦</span>
                                    &nbsp;&nbsp;Daño: {damage}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # DAÑO POR MINUTO
                            st.markdown(
                                f"""
                                <div style="
                                    margin-bottom: 22px;
                                    font-size: 17px;
                                    font-weight: bold;
                                    color: white;
                                ">
                                    <span style="color:#fb7185; font-size:21px;">✹</span>
                                    &nbsp;&nbsp;Daño/min: {damage_minuto}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                                            
                                

                    st.divider()
                    
            
elif seccion == "Análisis":
    st.header("Análisis de rendimiento")
    
elif seccion == "Timeline":
    st.header("Timeline de partidas")

#elif nos sirve como condicional, si "if" no se cumple compruba la siguiente si hicieramos 4 ifs 
#comprobaria todos los resultados

# ============================================================
# INICIAR APP
# ============================================================
# En la terminal de VS Code:
# cd "C:\Users\danel\OneDrive\Escritorio\Python\League Of Legends"
# py -m streamlit run app.py
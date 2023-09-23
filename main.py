import streamlit
import streamlit_authenticator
import streamlit_option_menu
from inscription import inscription_function
from ranger import store_function
from other_functions import database_connect_function, open_file, check_ability
from validate import validate_function
from analyse import analyse_function
from acceder import access_function
from dashboard import dashboard_function
from tools import tools_function
from rapport import rapport_function
from sites import site_function
from assurance_qualite import assurance_qualite_function


streamlit.set_page_config(
    page_title="library",
    page_icon=":fleur_de_lis",
    layout="wide"
)

# Necessary variables
# Connection
connection = database_connect_function()


# Authentication
# Get user data
cursor = connection.cursor()
query = "SELECT nom, prenom, mail, password FROM users"
cursor.execute(query)
result = cursor.fetchall()


# Create user data dict
data = {"usernames": {}}
for row in result:
    username = row[1]  # prenom
    name = row[2]  # On utilise le mail pour plus d'unicité que le 'nom + prenom'
    email = row[2]
    password = row[3]

    data["usernames"][name] = {
        "name": name,
        "email": email,
        "password": password
    }


# Authentication
with streamlit.container():
    left, middle, right = streamlit.columns(3)

    with left, right:
        streamlit.empty()
    with middle:
        streamlit.subheader("Archival System")
        authenticator = streamlit_authenticator.Authenticate(data, "library", "lb", 30)
        name, authenticator_status, username = authenticator.login("Login", "main")


if not authenticator_status:
    with streamlit.container():
        left, middle, right = streamlit.columns(3)

        with left, right:
            streamlit.empty()
        with middle:
            streamlit.warning("Identifiants incorrects")


elif authenticator_status:
    # Logout button
    authenticator.logout("Se deconnecter", "sidebar")

    # ------------ App -----------------
    # Navigation menu
    with streamlit.sidebar:
        streamlit.success(f"* Hi !")
        streamlit.write("Version : v1.0.5")

        choice = streamlit_option_menu.option_menu(
            menu_title="Menu",
            options=["Inscription", "Ranger", "Valider", "Analyser", "Assurance qualité", "Acceder", "Dashboard", "Rapport", "Sites", "Outils"]

        )

    # Mail storage for identification
    user_datas = name

    if choice == "Inscription":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin"]:
            inscription_function(connection, connection.cursor())
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Ranger":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin", "Archiviste"]:
            store_function(user_datas, connection, connection.cursor())
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Valider":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin", "Chargé de validation"]:
            validate_function(connection, connection.cursor(), open_file)
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Analyser":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin", "Analyste"]:
            analyse_function(user_datas, connection, connection.cursor(), open_file)
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Assurance qualité":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin", "Assurance qualité"]:
            assurance_qualite_function(connection, connection.cursor(), open_file)
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Acceder":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin", "Expert", "Chargé de validation"]:
            access_function(connection.cursor(), open_file)
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Dashboard":
        dashboard_function(connection.cursor())

    elif choice == "Rapport":
        if check_ability(user_datas, connection.cursor()) in ["Super admin"]:
            rapport_function(user_datas, connection, connection.cursor(), open_file)
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")

    elif choice == "Sites":
        site_function()

    elif choice == "Outils":
        if check_ability(user_datas, connection.cursor()) in ["Super admin", "Admin"]:
            tools_function(connection, connection.cursor())
        else:
            streamlit.error("Vous n'avez pas l'abilitation requise")






















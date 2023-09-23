import base64
import io
import os
import zipfile
import streamlit
import time


def tools_function(connection, cursor):
    streamlit.subheader("Outils")
    streamlit.markdown("<br />" * 3, unsafe_allow_html=True)

# FIRST BLOCK
    with streamlit.container():
        left, right = streamlit.columns(2)

        with left:
            streamlit.error(f"Effacer une entrée (Irréversible)")
            file_name = streamlit.text_input("Saisissez le nom du fichier à supprimer")
            if streamlit.button("Effacer le fichier"):
                query = "SELECT * FROM files WHERE file_name = %s"
                cursor.execute(query, (file_name,))
                result = cursor.fetchone()
                if result:
                    """Deleting from files database"""
                    cursor.execute("DELETE FROM files WHERE file_name = %s", (file_name,))
                    connection.commit()
                    try:
                        cursor.execute("DELETE FROM analyse WHERE sec_id = %s", (result[0],))
                        connection.commit()
                    except:
                        pass

                    """Deleting from files_backup database"""
                    cursor.execute("SELECT * FROM files_backup WHERE file_name = %s", (file_name,))
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("DELETE FROM files_backup WHERE file_name = %s", (file_name,))
                        connection.commit()
                        try:
                            cursor.execute("DELETE FROM analyse_backup WHERE sec_id = %s", (result[0],))
                            connection.commit()
                        except:
                            pass
                        streamlit.success(f"Fichier {file_name} supprimé !")
                    else:
                        streamlit.success(f"Fichier {file_name} supprimé !")

                else:
                    streamlit.error("Aucun fichier de ce nom trouvé !")

        with right:
            streamlit.error("Effacer un utilisateur (Irréversible)")
            user_mail = streamlit.text_input("Saisissez le mail de l'utilisateur à supprimer")
            if streamlit.button("Effacer l'utilisateur"):
                query = "SELECT mail FROM users WHERE mail = %s"
                cursor.execute(query, (user_mail,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("DELETE FROM users WHERE mail = %s", (user_mail,))
                    connection.commit()
                    streamlit.success("Utilisateur supprimé !")
                else:
                    streamlit.error("Utilisateur introuvable !")

        streamlit.markdown("<br />", unsafe_allow_html=True)


# SECOND BLOCK
    with streamlit.container():
        left, right = streamlit.columns(2)

        with left:
            streamlit.error(f"Effacer une fiche d'analyse (Irréversible)")
            file_name = streamlit.text_input("Saisissez le nom du fichier correspondant à la fiche d'analyse")
            if streamlit.button("Effacer la fiche d'analyse"):
                query = "SELECT * FROM files WHERE file_name = %s"
                cursor.execute(query, (file_name,))
                result = cursor.fetchone()
                if result:
                    """Deleting from analyse database"""
                    cursor.execute("DELETE FROM analyse WHERE sec_id = %s", (result[0],))
                    connection.commit()
                    """Deleting from analyse database"""
                    cursor.execute("DELETE FROM analyse_backup WHERE sec_id = %s", (result[0],))
                    connection.commit()
                    streamlit.success("Fiche d'analyse supprimé !")
                else:
                    streamlit.error("Fichier introuvable !")

        with right:
            streamlit.error(f"Effacer un rapport (Irréversible)")
            file_name = streamlit.text_input("Saisissez le nom du fichier rapport")
            if streamlit.button("Effacer le rapport"):
                query = "SELECT * FROM rapport WHERE file_name = %s"
                cursor.execute(query, (file_name,))
                result = cursor.fetchone()
                if result:
                    """Deleting from rapport database"""
                    cursor.execute("DELETE FROM rapport WHERE file_name = %s", (file_name,))
                    connection.commit()
                    streamlit.success("Rapport supprimé !")
                else:
                    streamlit.error("Rapport introuvable !")

        streamlit.write("---")
        streamlit.markdown("<br />" * 4, unsafe_allow_html=True)


# THIRD BLOCK
    with streamlit.container():
        if streamlit.checkbox("Outils d'optimisation"):
            left, right = streamlit.columns(2)

            with left:
                streamlit.success("Outil d'optimisation (Cela peut prendre plusieurs minutes !)")
                if streamlit.button("COMMENCER"):
                    with streamlit.spinner(f":car: Process en cours..."):
                        time.sleep(4)

                        # Delete entries from 'files' and 'analyse' tables
                        cursor.execute("DELETE FROM files")
                        connection.commit()
                        cursor.execute("DELETE FROM analyse")
                        connection.commit()

                    streamlit.success("Optimisé !")

                streamlit.markdown("<br />" * 3, unsafe_allow_html=True)

                # Fast mode
                streamlit.error("Alleger la base de données (Efface les documents Non-approuvés !)")
                if streamlit.button("Alleger"):
                    with streamlit.spinner(f":car: En cours..."):
                        # Delete entries from 'files' and 'analyse' tables
                        statut = "Non approuvé"
                        cursor.execute("DELETE FROM files_backup WHERE statut = %s", (statut,))
                        connection.commit()

                    streamlit.success("Réussis !")


# FOURTH BLOCK
    with streamlit.container():
        selected_pole, selected_subject, selected_secteur_thematique, mission_intitule = ["", "", "", ""]
        if streamlit.checkbox("Fichiers de mission"):
            poles = ["Pole budgetaire", "Pole Audit Contrôle Fiscalité", "Pole P4P"]

            pole_budgetaire_options = [
                "Revue des dépenses politiques et analyses budgétaire et financière",
                "Enquête de traçabilité des dépenses publiques",
                "Etudes de plaidoyer d'investissement",
                "Analyse de l'espace budgétaire",
                "Etude et assistance en matière de programmation budgétaire",
                "Etude fiscale et assistance en politique fiscale",
                "Analyse de l'efficience"
            ]

            pole_audit_fiscalite = [
                "Exécution budgétaire",
                "Evaluation de projets/programmes",
                "Audit",
                "PETS",
                "Services financiers et renforcement capacité",
                "Microfinance ou services financiers décentralisés (SFD)",
                "Partenariat public-privé (PPD)",
                "Controle interne et controle de gestion",
                "Fiscalité",
                "Gestion administrative et financière",
                "Finance inclusive"
            ]  # Add options for Pole Audit Fiscalite here

            pole_p4p = [
                "Evaluation et evalution d'impact des politiques publiques, projets et programmes",
                "Enquêtes",
                "Monitoring et conception de dispositifs",
                "PETS"
            ]  # Add options for Pole Audit Fiscalite here

            subjects = [
                "Protection sociale",
                "Gouvernance",
                "Enfance",
                "Programme projet",
                "Eau, hygiène et assainissement",
                "Santé",
                "Agriculture",
                "Climat",
                "Education",
                "Nutrition",
                "Décentralisation",
                "Genre"
            ]

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Dropdown select for pole
            selected_pole = streamlit.selectbox("Sélectionner un pôle", poles)

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Dropdown select for subject based on selected pole
            if selected_pole == "Pole budgetaire":

                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_budgetaire_options
                )
            elif selected_pole == "Pole Audit Contrôle Fiscalité":

                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_audit_fiscalite
                )
            elif selected_pole == "Pole P4P":

                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_p4p
                )
            else:
                selected_subject = ""

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)

            selected_secteur_thematique = streamlit.selectbox("Sélectionner un secteur/thématique",
                                                              subjects)

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Input field for "Intitulé de la mission"
            mission_intitule = streamlit.text_input("Intitulé de la mission")
            if streamlit.checkbox("Voir les intitulés de mission disponibles"):
                cursor.execute("SELECT mission_intitule FROM files_backup")
                test = cursor.fetchall()
                test = [row[0] for row in test]
                test = list(set(test))
                for i in test:
                    streamlit.info(f"* {i}")

        file_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                 mission_intitule)

        # Retrieve approved files from the database based on the generated file path
        query = ("SELECT id, file_data, file_name, statut, lien FROM files_backup WHERE "
                 "mission_path = %s AND statut = 'Approuvé'")
        cursor.execute(query, (file_path,))
        files = cursor.fetchall()

        if files:
            # Create an in-memory buffer to store the ZIP file
            zip_buffer = io.BytesIO()

            # Create the ZIP file directly in the buffer
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for file in files:
                    file_id, file_data, file_name, status, lien = file
                    with zipf.open(file_name, "w") as zf:
                        zf.write(file_data)

                    # Check if the file has been analyzed
                    query = "SELECT * FROM analyse_backup WHERE sec_id = %s"
                    cursor.execute(query, (file_id,))
                    analyse_file = cursor.fetchone()
                    if analyse_file:
                        analyse_data = analyse_file[2]
                        analyse_name = analyse_file[3]
                        with zipf.open(analyse_name, "w") as azf:
                            azf.write(analyse_data)

            # Get the ZIP file data from the buffer
            zip_data = zip_buffer.getvalue()

            # Generate a download link for the ZIP file
            b64_zip_data = base64.b64encode(zip_data).decode("utf-8")
            zip_href = f'<a href="data:application/zip;base64,{b64_zip_data}" download="all_files.zip">Tout télécharger</a>'

            # Display the download link using Streamlit
            streamlit.markdown(zip_href, unsafe_allow_html=True)



















import streamlit
import os
import io
import base64


def access_function(cursor, open_file):

    streamlit.subheader("Acceder")

    with streamlit.container():
        left_block_2, right_block_2 = streamlit.columns((2, 1))

        with right_block_2:
            streamlit.empty()


        with left_block_2:
            # Dropdown select options
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
    query = ("SELECT id, file_data, file_path, file_name, statut, lien FROM files_backup WHERE "
             "mission_path = %s AND statut = 'Approuvé'")
    cursor.execute(query, (file_path,))
    files = cursor.fetchall()

    streamlit.write("---")

    # Display file details and download button for each file
    for file in files:
        file_id, file_data, file_path, file_name, status, lien = file

        streamlit.write("---")
        streamlit.info(f"Fichier : {file_name}")
        streamlit.info(f"Arborescence : {file_path}")

        # Create a file-like object in memory
        file_object = io.BytesIO(file_data)

        # Button to view the file
        if streamlit.button("Voir", key=file_name):
            open_file(file_object, file_name)

        # Providing the link
        streamlit.write(f"Lien : {lien}")

        # Provide the file as a downloadable link
        b64_data = base64.b64encode(file_data).decode("utf-8")
        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{file_name}">Télécharger</a>'
        streamlit.markdown(href, unsafe_allow_html=True)

        # Check if the file has been analyzed
        query = "SELECT * FROM analyse_backup WHERE sec_id = %s AND statut = %s"
        cursor.execute(query, (file_id, "Analysé",))
        analyse_file = cursor.fetchone()

        if analyse_file:
            streamlit.success(f"- Analysé !")
            streamlit.success(f"Fichier d'analyse : {analyse_file[3]}")

            # Button to view the analysis file
            if streamlit.button("Voir le fichier d'analyse", key=f"view_analysis_{file_id}"):
                # Create a file-like object in memory for the analysis file
                analysis_file_object = io.BytesIO(analyse_file[2])
                open_file(analysis_file_object, analyse_file[3])

            # Provide the file as a downloadable link
            if analyse_file[3].lower().endswith((".pdf", ".doc", ".docx")):
                # For PDF, DOC, and DOCX files, use the original file name
                href = f'<a href="data:application/octet-stream;base64,{base64.b64encode(analyse_file[2]).decode("utf-8")}" download="{analyse_file[3]}">Télécharger</a>'
            else:
                # For other file types, append ".pdf" as the file extension for downloading
                href = f'<a href="data:application/octet-stream;base64,{base64.b64encode(analyse_file[2]).decode("utf-8")}" download="{analyse_file[3]}.pdf">Télécharger</a>'
            streamlit.markdown(href, unsafe_allow_html=True)
        else:
            streamlit.error(f"- Non analysé !")

        streamlit.write("---")

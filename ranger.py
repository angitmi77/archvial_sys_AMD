import json
import streamlit
import streamlit_lottie
import os
import pycountry
import time


def store_function(user_datas, connection, cursor):

    streamlit.header("Ranger")

    with streamlit.container():
        left_block_2, right_block_2 = streamlit.columns((2, 1))

        with right_block_2:
            streamlit.markdown("<br>" * 70, unsafe_allow_html=True)
            streamlit_lottie.st_lottie(json.load(open("style/storebook.json", "r")), key="storebook")


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
                "Monitoring et conception de dispositifs"
            ]  # Add options for Pole Audit Fiscalite here


            document_types = [
                "Textes",
                "Documents de politiques",
                "Evaluations",
                "Annuaire",
                "Documents de projets",
                "Etudes diagnostics, Etudes comparatives, Guides Manuels",
                "Documents budgétaires",
                "Rapports"
            ]

            budget_document_types = [
                "Document de programmation Pluriannuelle des Dépenses",
                "Document de programmation budgétaire et Economique Pluriannuelle",
                "Projet annuel de performance",
                "Loi de finances",
                "Rapport annuel de performance",
                "Base de données budgétaire",
                "Loi de finances rectificative",
                "Loi de règlement"
            ]

            report_types = [
                "Rapport d'enquête",
                "Rapport d'évaluation",
                "Rapport d'étude",
                "Rapport d'activité"
            ]

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Dropdown select for pole
            selected_pole = streamlit.selectbox("Sélectionner un pôle", poles)

            # Dropdown select for subject based on selected pole
            if selected_pole == "Pole budgetaire":
                streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_budgetaire_options
                )
            elif selected_pole == "Pole Audit Contrôle Fiscalité":
                streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_audit_fiscalite
                )
            elif selected_pole == "Pole P4P":
                streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
                selected_subject = streamlit.selectbox(
                    "Sélectionner un domaine",
                    pole_p4p
                )
            else:
                selected_subject = ""

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Dropdown select for secteur/thematique
            secteur_thematique_options = [
                "Protection sociale",
                "Eau, hygiène et assainissement",
                "Santé",
                "Agriculture",
                "Genre",
                "Climat",
                "Education",
                "Nutrition",
                "Décentralisation"
            ]
            selected_secteur_thematique = streamlit.selectbox("Sélectionner un secteur/thématique",
                                                              secteur_thematique_options)

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

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Auto-complete input for selecting the country
            country_options = [country.name for country in pycountry.countries]
            selected_country = streamlit.multiselect("Sélectionner le pays", country_options, key="selected_country")

            # When generating the file path, join the country names with underscores
            if len(selected_country) > 0:
                selected_countries_str = "_".join(selected_country)
            else:
                selected_countries_str = ""

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # User input for ministry or institution
            selected_ministry_institution = streamlit.text_input("Ministère/Institution")

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Lien source
            link = streamlit.text_input("Lien source")

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Dropdown select for document type
            selected_document_type = streamlit.selectbox("Sélectionner un type de document", document_types)

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Additional dropdown select based on document type
            selected_report_type = ""
            if selected_document_type == "Documents budgétaires":
                selected_budget_document_type = streamlit.selectbox("Sélectionner un type de document budgétaire",
                                                                    budget_document_types)
                streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
                streamlit.subheader(f"Type de document budgétaire sélectionné : -- {selected_budget_document_type} --")
            elif selected_document_type == "Rapports":
                selected_report_type = streamlit.selectbox("Sélectionner un type de rapport", report_types)
                streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            else:
                selected_report_type = ""  # Define an empty string if document type is not "Rapports"

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Display the selected pole, subject, country, and document type
            streamlit.subheader(f"Pôle sélectionné : -- {selected_pole} -- ")
            streamlit.subheader(f"Domaine sélectionné : -- {selected_subject} --")
            streamlit.subheader(f"Secteur/Thématique sélectionné : -- {selected_secteur_thematique} --")
            streamlit.subheader(f"Intitulé de la mission : -- {mission_intitule} --")
            streamlit.subheader(f"Pays sélectionné : -- {selected_countries_str} --")
            streamlit.subheader(f"Ministère ou institution : -- {selected_ministry_institution} --")
            streamlit.subheader(f"Lien source : -- {link} --")
            streamlit.subheader(f"Type de document sélectionné : -- {selected_document_type} --")
            streamlit.subheader(f"Type de rapport sélectionné : -- {selected_report_type} --")

            streamlit.markdown("<br>" * 3, unsafe_allow_html=True)
            # Input file form for PDF and DOC
            uploaded_file = streamlit.file_uploader("Uploader le fichier (PDF ou DOC)")

            # Handle file upload
            # Modify the code in the if block where the file is saved
            if uploaded_file is not None:
                # Check if the uploaded file is a PDF or DOC file
                if uploaded_file.name.endswith((".pdf", ".doc", ".docx")):
                    # Get the file data
                    file_data = uploaded_file.read()

                    # Generate the file path
                    if selected_document_type == "Documents budgétaires":
                        file_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                 mission_intitule,
                                                 selected_countries_str, selected_ministry_institution,
                                                 selected_document_type,
                                                 selected_budget_document_type, uploaded_file.name)
                        # ACCESS FUNCTION PATH NEED
                        file_access_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                        mission_intitule,
                                                        selected_countries_str, selected_ministry_institution,
                                                        selected_document_type,
                                                        selected_budget_document_type)

                    elif selected_document_type == "Rapports":
                        file_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                 mission_intitule,
                                                 selected_countries_str, selected_ministry_institution,
                                                 selected_document_type,
                                                 selected_report_type, uploaded_file.name)
                        # ACCESS FUNCTION PATH NEED
                        file_access_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                        mission_intitule,
                                                        selected_countries_str, selected_ministry_institution,
                                                        selected_document_type,
                                                        selected_report_type)
                    else:
                        file_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                 mission_intitule,
                                                 selected_countries_str, selected_ministry_institution,
                                                 selected_document_type,
                                                 uploaded_file.name)
                        # ACCESS FUNCTION PATH NEED
                        file_access_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                        mission_intitule,
                                                        selected_countries_str, selected_ministry_institution,
                                                        selected_document_type)

                    # Mission path
                    mission_path = os.path.join(selected_pole, selected_subject, selected_secteur_thematique,
                                                mission_intitule)
                    # Check if file with the same name already exists in the database
                    query = "SELECT COUNT(*) FROM files WHERE file_name = %s"
                    cursor.execute(query, (uploaded_file.name,))
                    result = cursor.fetchone()

                    if result[0] > 0:
                        streamlit.error(
                            "Un fichier avec le même nom existe déjà. Veuillez utiliser un nom de fichier différent.")
                    else:
                        # Get user information based on user_datas
                        query = "SELECT * FROM users WHERE mail = %s"
                        cursor.execute(query, (user_datas,))
                        result = cursor.fetchone()

                        with streamlit.spinner(f":wave: Veuillez patientez svp !"):
                            # Insert file details into the files database
                            query = "INSERT INTO files (file_data, file_path, file_access_path, mission_path, mission_intitule, file_name, nom, prenom, lien) " \
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            values = (
                                file_data, file_path, file_access_path, mission_path, mission_intitule, uploaded_file.name, result[1], result[2], link)
                            cursor.execute(query, values)
                            connection.commit()

                            # Insert file details into the files_backup database
                            query = "INSERT INTO files_backup (file_data, file_path, file_access_path, mission_path, mission_intitule, file_name, nom, prenom, lien) " \
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            values = (
                                file_data, file_path, file_access_path, mission_path, mission_intitule, uploaded_file.name, result[1], result[2], link)
                            cursor.execute(query, values)
                            connection.commit()

                            time.sleep(2)

                        streamlit.success("Le fichier a été sauvegardé avec succès.")


                else:
                    streamlit.error("Veuillez sélectionner un fichier au format PDF ou DOC.")
import json
import os
import streamlit
import streamlit_lottie
import io
import base64


def rapport_function(user_datas, connection, cursor, open_file):

    streamlit.header("Ranger")
    streamlit.markdown("<br>", unsafe_allow_html=True)

    with streamlit.container():
        left_block_2, right_block_2 = streamlit.columns((2, 1))

        with right_block_2:
            streamlit_lottie.st_lottie(json.load(open("style/storebook.json", "r")), key="storebook")

        with left_block_2:
            if streamlit.checkbox("Ranger un rapport"):

                # Dropdown select options
                poles = ["Pole budgetaire", "Pole Audit Contrôle Fiscalité", "Pole P4P"]

                # Dropdown select for pole
                selected_pole = streamlit.selectbox("Sélectionner un pôle", poles)

                streamlit.markdown("<br>", unsafe_allow_html=True)
                # Input field for "Intitulé de la mission"
                mission_intitule = streamlit.text_input("Intitulé de la mission")

                # ACCESS FUNCTION PATH NEED
                file_access_path = os.path.join(selected_pole, mission_intitule)

                streamlit.markdown("<br>", unsafe_allow_html=True)
                uploaded_file = streamlit.file_uploader("Uploader le fichier (PDF ou DOC)")

                # Handle file upload
                # Modify the code in the if block where the file is saved
                if uploaded_file is not None:
                    # Check if the uploaded file is a PDF or DOC file
                    if uploaded_file.name.endswith((".pdf", ".doc", ".docx")):
                        # Get the file data
                        file_data = uploaded_file.read()

                        # Check if file with the same name already exists in the database
                        query = "SELECT COUNT(*) FROM rapport WHERE file_name = %s"
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

                            # Insert file details into the database
                            query = "INSERT INTO rapport (file_data, file_name, file_access_path, mission_intitule, nom, prenom) " \
                                    "VALUES (%s, %s, %s, %s, %s, %s)"
                            values = (
                                file_data, uploaded_file.name, file_access_path, mission_intitule, result[1], result[2])
                            cursor.execute(query, values)
                            connection.commit()

                            streamlit.success("Le fichier a été sauvegardé avec succès.")
                    else:
                        streamlit.error("Veuillez sélectionner un fichier au format PDF ou DOC.")

            streamlit.markdown("<br />" * 4, unsafe_allow_html=True)
            if streamlit.checkbox("Acceder à un rapport"):

                # Dropdown select options
                poles = ["Pole budgetaire", "Pole Audit Contrôle Fiscalité", "Pole P4P"]

                # Dropdown select for pole
                selected_pole = streamlit.selectbox("Sélectionner un pôle", poles, key="acess_pole")

                streamlit.markdown("<br>", unsafe_allow_html=True)
                # Input field for "Intitulé de la mission"
                mission_intitule = streamlit.text_input("Intitulé de la mission", key="access_intitule")
                if streamlit.checkbox("Voir les intitulés de mission disponibles"):
                    cursor.execute("SELECT mission_intitule FROM rapport")
                    test = cursor.fetchall()
                    test = [row[0] for row in test]
                    test = list(set(test))
                    for i in test:
                        streamlit.info(f"* {i}")

                # ACCESS FUNCTION PATH NEED
                file_access_path = os.path.join(selected_pole, mission_intitule)

                # Retrieve approved files from the database based on the generated file path
                query = ("SELECT id, file_data, file_access_path, file_name, nom, prenom FROM rapport WHERE "
                         "file_access_path = %s")
                cursor.execute(query, (file_access_path,))
                files = cursor.fetchall()

                # Search input for file name
                search_query = streamlit.text_input("Rechercher par nom de fichier")

                # Display file details and download button for each file
                for file in files:
                    file_id, file_data, file_access_path, file_name, nom, prenom = file

                    # Check if the search query matches the file name
                    if search_query.lower() in file_name.lower():
                        streamlit.write("---")
                        streamlit.info(f"Fichier : {file_name}")

                        # Create a file-like object in memory
                        file_object = io.BytesIO(file_data)

                        # Button to view the file
                        if streamlit.button("Voir", key=file_name):
                            open_file(file_object, file_name)

                        # Provide the file as a downloadable link
                        b64_data = base64.b64encode(file_data).decode("utf-8")
                        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{file_name}">Télécharger</a>'
                        streamlit.markdown(href, unsafe_allow_html=True)

                        streamlit.write("---")
                        streamlit.markdown("<br />" * 2, unsafe_allow_html=True)

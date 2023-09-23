import streamlit
import io
import base64


def analyse_function(user_datas, connection, cursor, open_file):
    # Retrieve approved files from the database
    query = ("SELECT id, file_data, file_path, file_name, statut, lien  FROM files WHERE statut = 'Approuvé' "
             "ORDER BY id DESC LIMIT 10")
    cursor.execute(query)
    files = cursor.fetchall()

    streamlit.title("Analyse")

    # Display file details and buttons for each approved file
    for file in files:
        file_id, file_data, file_path, file_name, status, lien = file

        streamlit.write("---")

        # Show file details
        streamlit.subheader(file_name)
        streamlit.info(f"- {file_name}")
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
        query = "SELECT * FROM analyse WHERE sec_id = %s"
        cursor.execute(query, (file_id,))
        analyse_file = cursor.fetchone()

        if analyse_file:
            streamlit.success(f"- Fiche d'analyse disponible !")
            streamlit.success(f"Fichier d'analyse : {analyse_file[3]}")

            # Button to view the analysis file
            if streamlit.button("Voir le fichier d'analyse", key=f"view_analysis_{file_id}"):
                # Create a file-like object in memory for the analysis file
                analysis_file_object = io.BytesIO(analyse_file[2])
                open_file(analysis_file_object, analyse_file[3])

            # Provide the analysed file as a downloadable link
            if analyse_file[3].lower().endswith((".pdf", ".doc", ".docx")):
                # For PDF, DOC, and DOCX files, use the original file name
                href = f'<a href="data:application/octet-stream;base64,{base64.b64encode(analyse_file[2]).decode("utf-8")}" download="{analyse_file[3]}">Télécharger</a>'
            else:
                # For other file types, append ".pdf" as the file extension for downloading
                href = f'<a href="data:application/octet-stream;base64,{base64.b64encode(analyse_file[2]).decode("utf-8")}" download="{analyse_file[3]}.pdf">Télécharger</a>'
            streamlit.markdown(href, unsafe_allow_html=True)

        else:
            streamlit.error(f"- Aucune fiche d'analyse")

            # Input file form for PDF and DOC
            uploaded_file = streamlit.file_uploader("Uploader un fichier d'analyse (PDF ou DOC)", key=file_id)

            # Modify the code in the if block where the file is saved
            if uploaded_file is not None:
                # Check if the uploaded file is a PDF or DOC file
                if uploaded_file.name.endswith((".pdf", ".doc", ".docx")):
                    # Get user information based on user_datas
                    query = "SELECT * FROM users WHERE mail = %s"
                    cursor.execute(query, (user_datas,))
                    result = cursor.fetchone()

                    # Store the file data in the database
                    query = ("INSERT INTO analyse(sec_id, analyse_data, analyse_name, nom, prenom) "
                             "VALUES(%s, %s, %s, %s, %s)")
                    cursor.execute(query, (file_id, uploaded_file.read(), uploaded_file.name, result[1], result[2]))
                    connection.commit()

                    # Store the file data in the backup now
                    query = ("INSERT INTO analyse_backup(sec_id, analyse_data, analyse_name, nom, prenom) "
                             "VALUES(%s, %s, %s, %s, %s)")
                    cursor.execute(query, (file_id, uploaded_file.read(), uploaded_file.name, result[1], result[2]))
                    connection.commit()
                    streamlit.success("Le fichier a été sauvegardé avec succès.")

        streamlit.write("---")
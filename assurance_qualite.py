import streamlit
import io
import base64


def assurance_qualite_function(connection, cursor, open_file):

    streamlit.title("Assurance qualité")
    # Calculate the offset based on the page number and items per page
    page_number = 1
    items_per_page = 10
    offset = (page_number - 1) * items_per_page

    # Retrieve stored files from the database ordered by ID in descending order with LIMIT and OFFSET
    query = "SELECT * FROM analyse_backup ORDER BY id DESC LIMIT %s OFFSET %s"
    cursor.execute(query, (items_per_page, offset))
    files = cursor.fetchall()

    # Display file details and download button for each file
    for file in files:
        file_id, file_sec_id, analyse_data, analyse_name, nom, prenom, status = file
        query = "SELECT file_name, file_data FROM files WHERE id = %s"
        cursor.execute(query, (file_sec_id,))
        files = cursor.fetchone()

        streamlit.write("---")
        streamlit.subheader(f" Document : {files[0]}")


        # Provide the file as a downloadable link
        b64_data = base64.b64encode(files[1]).decode("utf-8")
        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{files[0]}">Télécharger le document</a>'
        streamlit.markdown(href, unsafe_allow_html=True)

        # Dropdown select for updating the file status
        new_status = streamlit.selectbox("",
                                          ["-- Choisissez un statut --", "Analysé", "Non analysé", "None"],
                                          index=0, key=analyse_name, label_visibility="hidden")

        # Update the file status in the database only if a new status is selected
        if new_status != "-- Choisissez un statut --" and new_status != status:
            query = "UPDATE files SET analyse = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_sec_id))
            query = "UPDATE analyse SET statut = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_id))

            # For files_backup
            query = "UPDATE files_backup SET analyse = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_sec_id))
            query = "UPDATE analyse_backup SET statut = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_id))

            connection.commit()

            # Update the status variable to reflect the new status
            status = new_status

        # Show status messages based on the file status
        if status == "Analysé":
            streamlit.success(f"- Fiche d'analyse : {analyse_name}, Analysé")
            streamlit.success(f"Ajoutée par : {nom}, {prenom}")
        elif status == "Non analysé":
            streamlit.error(f"- Fiche d'analyse : {analyse_name}, Non analysé")
            streamlit.error(f"Ajoutée par : {nom}, {prenom}")
        else:
            streamlit.warning(f"- Fiche d'analyse : {analyse_name} - None")
            streamlit.warning(f"Ajoutée par : {nom}, {prenom}")

        # Create a file-like object in memory
        file_object = io.BytesIO(analyse_data)

        # Button to view the file
        view_button = streamlit.button("Voir", key=file_id)
        if view_button:
            open_file(file_object, analyse_name)

        # Provide the file as a downloadable link
        b64_data = base64.b64encode(analyse_data).decode("utf-8")
        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{analyse_name}">Télécharger la fiche d\'analyse</a>'
        streamlit.markdown(href, unsafe_allow_html=True)

        streamlit.write("---")
        streamlit.markdown("<br />" * 3, unsafe_allow_html=True)

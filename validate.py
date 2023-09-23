import streamlit
import io
import base64


def validate_function(connection, cursor, open_file):

    streamlit.title("Valider")
    # Calculate the offset based on the page number and items per page
    page_number = 1
    items_per_page = 10
    offset = (page_number - 1) * items_per_page

    # Retrieve stored files from the database ordered by ID in descending order with LIMIT and OFFSET
    query = "SELECT id, file_path, file_name, statut,  file_data, lien FROM files ORDER BY id DESC LIMIT %s OFFSET %s"
    cursor.execute(query, (items_per_page, offset))
    files = cursor.fetchall()

    # Display file details and download button for each file
    for file in files:
        file_id, file_path, file_name, status, file_data, lien = file

        streamlit.write("---")
        streamlit.subheader(file_name)
        # Dropdown select for updating the file status
        new_status = streamlit.selectbox("",
                                          ["-- Choisissez un statut --", "Approuvé", "Non approuvé", "None"],
                                          index=0, key=file_path, label_visibility="hidden")

        # Update the file status in the database only if a new status is selected
        if new_status != "-- Choisissez un statut --" and new_status != status:
            query = "UPDATE files SET statut = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_id))

            # For files_backup
            query = "UPDATE files_backup SET statut = %s WHERE id = %s"
            cursor.execute(query, (new_status, file_id))

            connection.commit()

            # Update the status variable to reflect the new status
            status = new_status

        # Show status messages based on the file status
        if status == "Approuvé":
            streamlit.success(f"- Approuvé")
            streamlit.success(file_path)
        elif status == "Non approuvé":
            streamlit.error(f"{file_name} - Non approuvé")
            streamlit.error(file_path)
        else:
            streamlit.warning(f"{file_name} - None")
            streamlit.warning(file_path)

        # Create a file-like object in memory
        file_object = io.BytesIO(file_data)

        # Button to view the file
        view_button = streamlit.button("Voir", key=file_id)
        if view_button:
            open_file(file_object, file_name)

        # Providing the link
        streamlit.write(f"Lien : {lien}")

        # Provide the file as a downloadable link
        b64_data = base64.b64encode(file_data).decode("utf-8")
        href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{file_name}">Télécharger</a>'
        streamlit.markdown(href, unsafe_allow_html=True)
import json
import streamlit
import pandas
import streamlit_lottie
import plotly.express

def dashboard_function(cursor):

    streamlit.subheader("Dashboard")
    streamlit.markdown("<br>" * 3, unsafe_allow_html=True)

    # Turning database into a dataframe
    cursor.execute("SELECT nom, prenom, statut, analyse FROM files_backup")
    dataframe = pandas.DataFrame(cursor.fetchall(), columns=["nom", "prenom", "statut", "analyse"])

    # First block -- General statistics
    with streamlit.container():
        left, right = streamlit.columns(2)

        with left:
            streamlit.info(f"Fichiers stockés : {dataframe['statut'].count()}")
            streamlit.info(f"Fichiers approuvés : {sum(dataframe['statut'] == 'Approuvé')}")
            streamlit.info(f"Fichiers non approuvés : {sum(dataframe['statut'] == 'Non approuvé')}")
            streamlit.info(f"Fichiers analysés : {sum(dataframe['analyse'] == 'Analysé')}")
            streamlit.info(f"Fichiers non analysés : {sum(dataframe['analyse'] == '')}")

        with right:
            streamlit_lottie.st_lottie(json.load(open("style/stastics_block1.json", "r")), key="infinityloop",
                                       height=300)

        streamlit.write("---")

    # Second block -- Archivistes
    if streamlit.checkbox(f"Statistiques archivistes"):
        with streamlit.container():
            streamlit.subheader("Fichiers stockés par archivistes")
            # Group by nom and prenom, count number of files
            files_per_user = dataframe.groupby(['nom', 'prenom'])['statut'].count().reset_index(name='count')

            # Create dataframe
            streamlit.dataframe(files_per_user, width=600)

            # Create bar chart
            fig = plotly.express.bar(files_per_user, x='nom', y='count', color='prenom', text='count')
            streamlit.plotly_chart(fig)

            streamlit.write("---")

        with streamlit.container():
            streamlit.subheader("Fichiers approuvés et non-approuvés par archivistes")

            # Group by nom, prenom, and statut, count number of files
            approval_status_counts = dataframe.groupby(['nom', 'prenom', 'statut'])[
                'analyse'].count().reset_index(name='count')

            # Pivot the DataFrame to have 'Approuvé' and 'Non approuvé' as columns
            pivot_table = approval_status_counts.pivot(index=['nom', 'prenom'], columns='statut',
                                                       values='count').reset_index()
            pivot_table = pivot_table.fillna(0)  # Fill NaN values with 0

            # Create a new column 'Total' to calculate the total number of files for each user
            pivot_table['Total'] = pivot_table['Approuvé'] + pivot_table['Non approuvé']

            # Display the DataFrame
            streamlit.dataframe(pivot_table, width=800)

            # Create a bar chart to visualize the information
            fig = plotly.express.bar(pivot_table, x=['Approuvé', 'Non approuvé'], y='prenom',
                         title='Nombre de fichiers approuvés et non approuvés par utilisateur',
                         labels={'value': 'Nombre de fichiers', 'prenom': 'Utilisateur'},
                         color_discrete_map={'Approuvé': 'green', 'Non approuvé': 'red'})
            streamlit.plotly_chart(fig)

        streamlit.write("---")

        with streamlit.container():
            streamlit.subheader("Fichiers analysés et non-analysés par archivistes")

            # Group by nom, prenom, and analyse, count number of files
            analysis_status_counts = dataframe.groupby(['nom', 'prenom', 'analyse'])['statut'].count().reset_index(
                name='count')

            # Pivot the DataFrame to have 'Analysé' and 'Non analysé' as columns
            pivot_table = analysis_status_counts.pivot(index=['nom', 'prenom'], columns='analyse',
                                                       values='count').reset_index()
            pivot_table = pivot_table.fillna(0)  # Fill NaN values with 0

            # Visualize the dataframe
            streamlit.dataframe(pivot_table)

            # Create a bar chart to visualize the information
            fig = plotly.express.bar(pivot_table, x=['Analysé', ''], y='prenom',
                         title='',
                         labels={'value': 'Nombre de fichiers', 'prenom': 'Archivistes'},
                         color_discrete_map={'Analysé': 'blue', 'Non analysé': 'red'})
            streamlit.plotly_chart(fig)

        streamlit.write("---")


    # Third block -- Analystes
    if streamlit.checkbox(f"Statistiques analystes"):
        with streamlit.container():


            streamlit.subheader("Fichiers stockés par analystes")
            cursor.execute("SELECT nom, prenom FROM analyse_backup")

            dataframe = pandas.DataFrame(cursor.fetchall(), columns=["nom", "prenom"])

            # Group and count data
            user_counts = dataframe.groupby(['nom', 'prenom']).size().reset_index(name='file_count')

            # Display the DataFrame
            streamlit.dataframe(user_counts, width=600)

            # Create bar chart using Plotly
            fig = plotly.express.bar(user_counts, x='nom', y='file_count', color=None, text='file_count')
            streamlit.plotly_chart(fig)

            streamlit.write("---")

        with streamlit.container():
            streamlit.subheader("Fichiers analysés et non analysés par analystes")
            cursor.execute("SELECT nom, prenom, statut FROM analyse_backup")
            dataframe = pandas.DataFrame(cursor.fetchall(), columns=["nom", "prenom", "statut"])

            # Group by nom, prenom, and statut, count number of files
            analysis_status_counts = dataframe.groupby(['nom', 'prenom', 'statut'])[
                'statut'].count().reset_index(name='count')

            # Pivot the DataFrame to have 'Analysé' and 'Non analysé' as columns
            pivot_table = analysis_status_counts.pivot(index=['nom', 'prenom'], columns='statut',
                                                       values='count').reset_index()
            pivot_table = pivot_table.fillna(0)  # Fill NaN values with 0

            # Create a new column 'Total' to calculate the total number of files for each user
            pivot_table['Total'] = pivot_table['Analysé'] + pivot_table['Non analysé']

            # Display the DataFrame
            streamlit.dataframe(pivot_table, width=800)

            # Create a bar chart to visualize the information
            fig = plotly.express.bar(pivot_table, x=['Analysé', 'Non analysé'], y='prenom',
                         title='Nombre de fichiers analysés et non analysés par utilisateur',
                         labels={'value': 'Nombre de fichiers', 'prenom': 'Utilisateur'},
                         color_discrete_map={'Analysé': 'green', 'Non analysé': 'red'})
            streamlit.plotly_chart(fig)

            streamlit.write("---")




    # Historique des fichiers
    if streamlit.checkbox("Historique"):
        if streamlit.checkbox("Archivistes"):
            streamlit.subheader("Historique archivistes")
            # Retrieve approved files from the database based on the generated file path
            cursor.execute("SELECT file_path, file_name, nom, prenom, statut, analyse FROM files_backup LIMIT 20")

            dataframe_2 = pandas.DataFrame(cursor.fetchall(),
                                           columns=["Arborescence", "Nom du fichier", "Nom", "Prenom",
                                                    "Statut", "Analyse"])
            streamlit.dataframe(dataframe_2, height=400, width=1000)

        if streamlit.checkbox("Analystes"):
            streamlit.subheader("Historique analystes")
            # Retrieve approved files from the database based on the generated file path
            cursor.execute("SELECT analyse_name, nom, prenom, statut FROM analyse_backup LIMIT 20")

            dataframe_2 = pandas.DataFrame(cursor.fetchall(),
                                           columns=["Nom du fichier", "Nom", "Prenom",
                                                    "Statut"])
            streamlit.dataframe(dataframe_2, height=400, width=1000)

















import streamlit
import streamlit_authenticator
import streamlit_lottie
import json


def inscription_function(connection, cursor):
    with streamlit.container():
        left_block_1, right_block_1 = streamlit.columns(2)

        with right_block_1:
            streamlit_lottie.st_lottie(json.load(open("style/signup.json", "r")), key="signuplottie")

        with left_block_1:
            streamlit.subheader("Inscription")
            nom = streamlit.text_input("Votre nom")
            prenom = streamlit.text_input("Votre Prenom")
            mmail = streamlit.text_input("Votre Adresse mail")
            role = streamlit.selectbox("Rôle ",
                                       ("Super admin", "Admin", "Archiviste", "Expert", "Analyste", "Chargé de validation", "Assurance qualité"))
            mpass = streamlit.text_input("Votre mot de passe", type="password")
            mpass2 = streamlit.text_input("Ressaisir le mot de passe", type="password")
            streamlit.write("##")
            if streamlit.button("S'inscrire"):
                if mpass != mpass2:
                    streamlit.error("Les mots de passe ne correspondent pas !")
                else:
                    if nom and prenom and mmail and mpass and role:
                        # Execute a query to check if the email exists in the database
                        query = "SELECT * FROM users WHERE mail = %s"
                        cursor.execute(query, (mmail,))

                        # Fetch the first row from the result
                        result = cursor.fetchone()

                        if result:
                            # If a matching record is found, display an error message
                            streamlit.error("Utilisateur existant !")
                        else:
                            # Hash the password using bcrypt and encode it to store in the database
                            hashed_pw = streamlit_authenticator.Hasher([mpass]).generate()

                            # Execute the query with the corrected values list
                            values = (nom, prenom, mmail, hashed_pw[0], role)  # Convert to tuple
                            query = "INSERT INTO users(nom, prenom, mail, password, rule) VALUES(%s, %s, %s, %s, %s)"
                            cursor.execute(query, values)
                            connection.commit()
                            streamlit.success("Inscription réussie !")
                    else:
                        streamlit.warning("Veuillez entrez tous les champs !")


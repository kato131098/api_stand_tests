import sender_stand_request
import data

def get_user_body(first_name):

    current_body = data.user_body.copy()
    current_body['firstName'] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):

    user_body = get_user_body(first_name)
    print(user_body)
    response = sender_stand_request.post_new_user(user_body)
    print(response)
    assert response.status_code == 400

    assert response.json()['code'] == 400

def negative_assert_no_first_name(user_body):

    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    print(response.status_code)

    assert response.json()['code'] == 400


# Prueba 1. Usuario o usuaria creada con éxito. El parámetro firstName contiene 2 caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. Usuario o usuaria creada con éxito. El parámetro firstName contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Prueba 3. Error. El parámetro firstName contiene 1 carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Prueba 4. Error. El parámetro firstName ontiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Prueba 5. Usuario o usuaria creada con éxito. El parámetro firstName contiene caracteres latinos
def test_create_user_has_space_in_first_name_get_success_response():
    negative_assert_symbol("A Aaa")

# Prueba 6. Error. El parámetro firstName contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Prueba 7. Error. El parámetro firstName contiene un string de dígitos
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Prueba 8. Error. Falta el parámetro firstName en la solicitud
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_first_name(user_body)

# Prueba 9. Error. El parámetro contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_first_name(user_body)

# Prueba 10. Error. El tipo del parámetro firstName: número
def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400


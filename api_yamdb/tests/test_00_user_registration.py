import pytest
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class Test00UserRegistration:
    url_signup = "/api/v1/auth/signup/"
    url_token = "/api/v1/auth/token/"
    url_admin_create_user = "/api/v1/users/"

    @pytest.mark.django_db(transaction=True)
    def test_00_nodata_signup(self, client):
        request_type = "POST"
        response = client.post(self.url_signup)

        assert response.status_code != 404, (
            f"Страница `{self.url_signup}` не найдена, "
            f"проверьте этот адрес в *urls.py*"
        )
        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"без параметров не создается пользователь "
            f"и возвращается статус {code}"
        )
        response_json = response.json()
        empty_fields = ["email", "username"]
        for field in empty_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f"Проверьте, что при {request_type} запросе "
                f"`{self.url_signup}` без параметров в ответе есть сообщение "
                f"о том, какие поля заполенены неправильно"
            )

    @pytest.mark.django_db(transaction=True)
    def test_00_invalid_data_signup(self, client):
        invalid_email = "invalid_email"
        invalid_username = "invalid_username@yamdb.fake"

        invalid_data = {"email": invalid_email, "username": invalid_username}
        request_type = "POST"
        response = client.post(self.url_signup, data=invalid_data)

        assert response.status_code != 404, (
            f"Страница `{self.url_signup}` не найдена, "
            f"проверьте этот адрес в *urls.py*"
        )
        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с невалидными данными не создается пользователь "
            f"и возвращается статус {code}"
        )

        response_json = response.json()
        invalid_fields = ["email"]
        for field in invalid_fields:
            assert field in response_json.keys() and isinstance(
                response_json[field], list
            ), (
                f"Проверьте, что при {request_type} запросе "
                f"`{self.url_signup}` с невалидными параметрами, в ответе "
                f"есть сообщение о том, какие поля заполенены неправильно"
            )

        valid_email = "validemail@yamdb.fake"
        invalid_data = {
            "email": valid_email,
        }
        response = client.post(self.url_signup, data=invalid_data)
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"без username нельзя создать пользователя и "
            f"возвращается статус {code}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_valid_data_user_signup(self, client):

        valid_email = "valid@yamdb.fake"
        valid_username = "valid_username"
        outbox_before_count = len(mail.outbox)

        valid_data = {"email": valid_email, "username": valid_username}
        request_type = "POST"
        response = client.post(self.url_signup, data=valid_data)
        outbox_after = mail.outbox  # email outbox after user create

        assert response.status_code != 404, (
            f"Страница `{self.url_signup}` не найдена, "
            f"проверьте этот адрес в *urls.py*"
        )

        code = 200
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными создается пользователь "
            f"и возвращается статус {code}"
        )
        assert response.json() == valid_data, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными создается пользователь "
            f"и возвращается статус {code}"
        )

        new_user = User.objects.filter(email=valid_email)
        assert new_user.exists(), (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными создается пользователь "
            f"и возвращается статус {code}"
        )

        # Test confirmation code
        assert len(outbox_after) == outbox_before_count + 1, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными пользователю приходит "
            f"email с кодом подтверждения"
        )
        assert valid_email in outbox_after[0].to, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными, пользователю приходит письмо "
            f"с кодом подтверждения на email, "
            f"который он указал при регистрации"
        )

        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_00_valid_data_admin_create_user(self, admin_client):

        valid_email = "valid@yamdb.fake"
        valid_username = "valid_username"
        outbox_before_count = len(mail.outbox)

        valid_data = {"email": valid_email, "username": valid_username}
        request_type = "POST"
        response = admin_client.post(
            self.url_admin_create_user, data=valid_data
        )
        outbox_after = mail.outbox

        assert response.status_code != 404, (
            f"Страница `{self.url_admin_create_user}` не найдена, "
            f"проверьте этот адрес в *urls.py*"
        )

        code = 201
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе "
            f"`{self.url_admin_create_user}` с валидными данными "
            f"от имени администратора, создается пользователь "
            f"и возвращается статус {code}"
        )
        response_json = response.json()
        for field in valid_data:
            assert field in response_json and valid_data.get(
                field
            ) == response_json.get(field), (
                f"Проверьте, что при {request_type} запросе "
                f"`{self.url_admin_create_user}` с валидными данными "
                f"от имени администратора, в ответ приходит "
                f"созданный объект пользователя в виде словаря"
            )

        new_user = User.objects.filter(email=valid_email)
        assert new_user.exists(), (
            f"Проверьте, что при {request_type} запросе "
            f"`{self.url_admin_create_user}` с валидными данными "
            f"от имени администратора, в БД создается пользователь "
            f"и возвращается статус {code}"
        )

        # Test confirmation code not sent to user after admin registers him
        assert len(outbox_after) == outbox_before_count, (
            f"Проверьте, что при {request_type} запросе "
            f"`{self.url_admin_create_user}` с валидными данными "
            f"от имени администратора, пользователю НЕ приходит email "
            f"с кодом подтверждения"
        )

        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_00_obtain_jwt_token_invalid_data(self, client):

        request_type = "POST"
        response = client.post(self.url_token)
        assert response.status_code != 404, (
            f"Страница `{self.url_token}` не найдена, "
            f"проверьте этот адрес в *urls.py*"
        )

        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при POST запросе `{self.url_token}` "
            f"без параметров, возвращается статус {code}"
        )

        invalid_data = {"confirmation_code": 12345}
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == code, (
            f"Проверьте, что при POST запросе `{self.url_token}` "
            f"без username, возвращается статус {code}"
        )

        invalid_data = {
            "username": "unexisting_user",
            "confirmation_code": 12345,
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 404
        assert response.status_code == code, (
            f"Проверьте, что при POST запросе `{self.url_token}` "
            f"с несуществующим username, возвращается статус {code}"
        )

        valid_email = "valid@yamdb.fake"
        valid_username = "valid_username"

        valid_data = {"email": valid_email, "username": valid_username}
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"с валидными данными создается пользователь "
            f"и возвращается статус {code}"
        )

        invalid_data = {
            "username": valid_username,
            "confirmation_code": 12345,
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при POST запросе `{self.url_token}` "
            f"с валидным username, но невалидным confirmation_code, "
            f"возвращается статус {code}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_registration_me_username_restricted(self, client):
        valid_email = "valid@yamdb.fake"
        invalid_username = "me"
        request_type = "POST"

        valid_data = {"email": valid_email, "username": invalid_username}
        response = client.post(self.url_signup, data=valid_data)
        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f'нельзя создать пользователя с username = "me" '
            f"и возвращается статус {code}"
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_registration_same_email_restricted(self, client):
        valid_email_1 = "test_duplicate_1@yamdb.fake"
        valid_email_2 = "test_duplicate_2@yamdb.fake"
        valid_username_1 = "valid_username_1"
        valid_username_2 = "valid_username_2"
        request_type = "POST"

        valid_data = {"email": valid_email_1, "username": valid_username_1}
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"можно создать пользователя с валидными данными "
            f"и возвращается статус {code}"
        )

        duplicate_email_data = {
            "email": valid_email_1,
            "username": valid_username_2,
        }
        response = client.post(self.url_signup, data=duplicate_email_data)
        code = 400
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"нельзя создать пользователя, email которого "
            f"уже зарегистрирован и возвращается статус {code}"
        )
        duplicate_username_data = {
            "email": valid_email_2,
            "username": valid_username_1,
        }
        response = client.post(self.url_signup, data=duplicate_username_data)
        assert response.status_code == code, (
            f"Проверьте, что при {request_type} запросе `{self.url_signup}` "
            f"нельзя создать пользователя, username которого"
            f" уже зарегистрирован и возвращается статус {code}"
        )

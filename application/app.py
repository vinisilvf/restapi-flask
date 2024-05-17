import re
from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from mongoengine import NotUniqueError
from .model import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "first_name",
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    "last_name",
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    "cpf",
    type=str,
    required=True,
    help="Campo CPF não valido."
)
_user_parser.add_argument(
    "email",
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    "birth_date",
    type=str,
    required=True,
    help="This field cannot be blank."
)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def validate_cpf(self, cpf):
        # Verifica a formatação do CPF
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid!"}, 400

        try:
            response = UserModel(**data).save()
            return {"message": "User %s sucessfully created!" % response.id}
        except NotUniqueError:
            return {"message": "CPF already exists in database!"}, 400

    def get(self, cpf):
        response = jsonify(UserModel.objects(cpf=cpf))

        if response:
            return jsonify({response})

        return {"message": "User does not exist in database!"}, 400

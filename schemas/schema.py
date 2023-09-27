from app import ma
from marshmallow import fields

class UsuarioBasicSchema(ma.Schema):
    nombre = fields.String()

    def get_username(self, obj):
        return f'hi {obj.nombre}'

class UsuarioAdminSchema(UsuarioBasicSchema):
    id = fields.Integer(dump_only=True)
    password_hash = fields.String()
    nombre = fields.Method('get_username')

class PaisBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()

class ProvinciaBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    pais = fields.Integer()
    pais_obj = fields.Nested(PaisBasicSchema, exclude={'id',})

class LocalidadBasicSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    provincia = fields.Integer()
    prov_obj = fields.Nested(ProvinciaBasicSchema, exclude={'id', 'pais'})
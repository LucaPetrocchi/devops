#IMPORTS NATIVOS
from datetime import datetime, timedelta

#NATIVOS DE FRAMEWORK [FLASK]
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
)

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

#VARIABLES NUESTRAS
from app import app, db, jwt
from models.models import (
    Usuario, 
    Paises, 
    Provincia, 
    Localidad, 
    Personas,
    )
from schemas.schema import (
    UsuarioAdminSchema,
    UsuarioBasicSchema,
    PaisBasicSchema,
    ProvinciaBasicSchema,
    LocalidadBasicSchema,
)


@app.route('/users', methods=['POST'])
@jwt_required()
def get_all_users():
    page = request.args.get('page', 1, type=int)
    cant = request.args.get('cant', 1000, type=int)
    usuarios = db.session.query(Usuario).paginate(page=page, per_page=cant)
    additional_info = get_jwt()
    # print(usuarios.has_prev)
    # print(usuarios.has_next)
    # print(usuarios.next_num)
    # print(usuarios.next())

    print(
        url_for('get_all_users', page=usuarios.next_num) if usuarios.has_next else None
        )
    if additional_info['is_admin']:
        return jsonify(
            {
                "results": UsuarioAdminSchema().dump(usuarios, many=True),
                "next": url_for('get_all_users', page=usuarios.next_num) if usuarios.has_next else None,
                "prev": url_for('get_all_users', page=usuarios.prev_num) if usuarios.has_prev else None
            })
    return UsuarioBasicSchema().dump(usuarios, many=True)

@app.route('/localidades', methods=['POST'])
def get_all_paises():
    # paises = Paises.query.all()
    # paischema = PaisBasicSchema().dump(paises, many=True)

    # provincias = Provincia.query.all()
    # provinschema = ProvinciaBasicSchema().dump(provincias, many=True)

    localidades = Localidad.query.all()
    localischema = LocalidadBasicSchema().dump(localidades, many=True)

    return jsonify(localischema)

@app.context_processor
def inject_paises():
    countries = db.session.query(Paises).all()
    return dict(paises = countries)
                # {"paises": countries}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/adduser", methods=['POST'])
def adduser():
    if request.method=='POST':
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin')
        password_hash = generate_password_hash(
            password, method='pbkdf2', salt_length=16
        )
        
        nuevo_usuario = Usuario(nombre=username, password_hash=password_hash, is_admin=is_admin)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({'Se recibio':'la data',
                        'username':username,
                        'password_hash':password_hash}, 200)

@app.route('/login', methods=["POST"])
def login():
        data = request.authorization

        username = data.get('username')
        password = data.get('password')

        user = Usuario.query.filter_by(nombre=username).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(
                identity=username,
                expires_delta = timedelta(minutes=60),
                additional_claims = dict(
                    is_admin = user.is_admin,
                ),
            )
            return jsonify({'ok':access_token})
        return jsonify(Error="No pude generar el token")


@app.route("/agregar_pais", methods=['POST'])
def nuevo_pais():
    if request.method=="POST":
        nombre_pais = request.form['nombre']

        nuevo_pais = Paises(nombre=nombre_pais)

        db.session.add(nuevo_pais)
        db.session.commit()

        return redirect(url_for('index'))
    
@app.route("/borrar_pais/<id>")
def borrar_pais(id):
    
    pais = Paises.query.get(id)
    db.session.delete(pais)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/ruta_restringida")
@jwt_required()
def ruta_restringida():
    current_user = get_jwt_identity()
    additional_info = get_jwt()
    if additional_info['user_type'] == 1:
        return jsonify(
            {"Mensaje": f"el usuario {current_user} tiene acceso.",
             "Info Adicional": f"{additional_info}"}
        )
    
    return jsonify(
            {"Mensaje": f"el usuario {current_user} NO tiene acceso a esta ruta"}
        )

@jwt.invalid_token_loader
def unauthorized_user(reason):


    return jsonify(mensaje=f"access denied: {reason}")






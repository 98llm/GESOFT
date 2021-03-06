import os

from flask.helpers import flash
from werkzeug.wrappers import response # noqa
from __init__ import app, login_manager
from models import * # noqa
from flask_cors import cross_origin
from flask import (
    session,
    render_template,
    request,
    url_for,
    redirect,
    jsonify
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


@app.route('/')
@login_required
def index():
    ops_abertas = OP.query.filter_by(status='Em andamento')
    anotacoes = Anotacao.query.all()
    if request.method == "POST":
        anotacao = Anotacao(assunto=request.form['anotacao_assunto'],
                            descricao=request.form['descricao'],
                            dt_anotacao=datetime.now(tz=pytz.UTC),
                            id_usuario=current_user.id)
        db.session.add(anotacao)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('home.html',
                           user=current_user,
                           ops_abertas=ops_abertas,
                           anotacoes=anotacoes)


@app.route('/anotacao/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_anotacao(id):
    anotacao = Anotacao.query.get(id)
    db.session.delete(anotacao)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Usuario.query.filter_by(username=username).first()
    if user:
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['username'] = user.username
            return redirect(url_for('index'))
        flash("erro")
    return render_template('login.html')


@app.route('/cliente', methods=['GET', 'POST'], defaults={'page_num': 1})
@app.route('/cliente/<int:page_num>', methods=['GET', 'POST'])
@login_required
def cliente(page_num):
    clientes = Cliente.query.filter_by(ativo=1)
    clientes = Cliente.query.paginate(per_page=5,
                                      page=page_num,
                                      error_out=True)
    total = clientes.total
    return render_template('cliente.html',
                           user=current_user,
                           clientes=clientes,
                           total=total)


@app.route('/cliente/adicionar', methods=['POST', 'GET'])
@login_required
def add_cliente():
    if request.method == 'POST':
        new_entity = Cliente(
            nome=request.form['nome_cliente'],
            cnpj=request.form['cnpj']
        )
        db.session.add(new_entity)
        db.session.commit()

        new_telefone = Telefone(
            numero=request.form['telefone'],
            id_cliente=new_entity.id  # fk
        )
        new_endereco = Endereco_cliente(
            logradouro=request.form['logradouro'],
            numero=request.form['numero'],
            bairro=request.form['bairro'],
            cep=request.form['cep'],
            uf=request.form['uf'],
            id_cliente=new_entity.id  # fk
        )
        db.session.add(new_telefone)
        db.session.add(new_endereco)
        db.session.commit()
        return redirect(url_for('cliente'))
    return render_template('adiciona_cliente.html',
                           user=current_user)


@app.route('/cliente/editar/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_cliente(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome_cliente']
        cliente.cnpj = request.form['cnpj']

        cliente.telefone.numero = request.form['telefone']

        cliente.endereco.logradouro = request.form['logradouro']
        cliente.endereco.numero = request.form['numero'],
        cliente.endereco.logradouro = request.form['bairro']
        cliente.endereco.cep = request.form['cep']
        cliente.endereco.uf = request.form['uf']
        try:
            db.session.commit()
            flash('Cadastro atualizado', "Sucess")
            return redirect(url_for('cliente'))
        except Exception:
            db.session.rollback()
            flash('Atualização invalida', "Error")
    return render_template('editar_cliente.html',
                           user=current_user,
                           cliente=cliente)


@app.route('/cliente/delete/<int:cliente>', methods=['POST', 'GET'])
@login_required
def delete_cliente(cliente):
    cliente = Cliente.query.get(cliente)
    cliente.ativo = 0
    db.session.commit()
    return redirect(url_for('cliente'))


# rota para vizualizacao das OPs| Define pagina 1 como padrao
@app.route('/op', methods=['GET', 'POST'], defaults={'page_num': 1})
@app.route('/op/<int:page_num>', methods=['GET', 'POST'])
@login_required
def op(page_num):
    ops = OP.query.paginate(per_page=5, page=page_num, error_out=True)
    total = ops.total
    return render_template('op.html', user=current_user, ops=ops, total=total)


@app.route('/componente', methods=['GET', 'POST'], defaults={'page_num': 1})
@app.route('/componente/<int:page_num>', methods=['GET', 'POST'])
@login_required
def componente(page_num):
    componentes = Componente.query.filter_by(ativo=1)
    componentes = componentes.paginate(per_page=5,
                                       page=page_num,
                                       error_out=True)
    total = componentes.total
    return render_template('componente.html',
                           user=current_user,
                           componentes=componentes,
                           total=total)


@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', user=current_user)


@app.route('/componente/adicionar', methods=['POST', 'GET'])
@login_required
def add_componente():
    if request.method == 'POST':
        componente = Componente(
            codigo=request.form['codigo'],
            tipo=request.form['tipo_componente'],
            nome=request.form['nome'],# noqa
            referencia=request.form['referencia']
        )
        db.session.add(componente)
        try:
            db.session.commit()
            flash("Componente adicionado", "Sucesso")
            return redirect(url_for('componente'))
        except Exception:
            db.session.rollback()
            flash("este componente ja existe", "error")
    return render_template('adicionar_componente.html',
                           user=current_user)


@app.route('/componente/editar/<int:componente>', methods=['POST', 'GET'])
@login_required
def edit_componente(componente):
    componente = Componente.query.get(componente)
    if request.method == 'POST':
        componente.codigo = request.form['codigo']
        componente.nome = request.form['nome']
        componente.tipo = request.form['tipo_componente']
        componente.referencia = request.form['referencia']
        try:
            db.session.commit()
            flash("Componente atualizado", "Sucesso")
            return redirect(url_for('componente'))
        except Exception:
            db.session.rollback()
            flash("este componente ja existe", "error")
    return render_template('editar_componente.html',
                           user=current_user,
                           componente=componente)


@app.route('/componente/delete/<int:componente>', methods=['POST', 'GET'])
@login_required
def delete_componente(componente):
    componente = Componente.query.get(componente)
    componente.ativo = 0
    db.session.commit()
    return redirect(url_for('componente'))


@app.route('/op/visualizar/<int:op_id>', methods=['POST', 'GET'])
@login_required
def op_visualizar(op_id):
    op = OP.query.get(op_id)
    return render_template('op_visualizar.html', user=current_user, op=op)


@app.route('/op/adicionar', methods=['POST', 'GET'])
@login_required
def add_op():
    clientes = Cliente.query.all()
    if request.method == 'POST':
        new_op = OP(
            qtd_placas=request.form['qtd_placas'],
            num_romaneio=request.form['num_romaneio'],
            valor=request.form['valor'],
            id_usuario=current_user.id,  # fk
            dt_emissao=datetime.now(tz=pytz.UTC),
            dt_entrega=request.form['dt_entrega'],
            id_cliente=request.form.get('cliente'),
            id_placa=request.form.get('placa'))
        db.session.add(new_op)
        db.session.commit()
        return redirect(url_for('op'))
    return render_template('adicionar_op.html',
                           user=current_user,
                           clientes=clientes)


@app.route('/op/editar/<int:op>', methods=['POST', 'GET'])
@login_required
def edit_op(op):
    op = OP.query.get(op)
    clientes = Cliente.query.all()
    if request.method == 'POST':
        op.qtd_placas = request.form['qtd_placas']
        op.num_romaneio = request.form['num_romaneio']
        op.status = request.form.get('status')
        op.id_placa = request.form.get('placa')
        db.session.commit()
        return redirect(url_for('op'))
    return render_template('editar_op.html',
                           user=current_user,
                           op=op,
                           clientes=clientes)


@app.route('/op/delete/<int:op>', methods=['POST', 'GET'])
@login_required
def delete_op(op):
    op = OP.query.get(op)
    db.session.delete(op)
    db.session.commit()
    return redirect(url_for('op'))


@app.route('/placa', methods=['POST', 'GET'])
@login_required
def placa():
    placas = Placa.query.filter_by(ativo=1)
    return render_template('placa.html', placas=placas, user=current_user)


@app.route('/placa/add', methods=['POST', 'GET'])
@login_required
def add_placa():
    clientes = Cliente.query.all()
    componentes = Componente.query.filter_by(ativo=1)
    if request.method == 'POST':
        # componentes = request.form.getlist('componente')
        # qtd_componentes = request.form.getlist('qtd_componentes')

        placa = Placa(
            codigo=request.form['codigo'],
            descricao=request.form['descricao'],
            modelo=request.form['modelo'],
            qtd_componentes=request.form['qtd_componentes'],
            id_cliente=request.form['id_cliente'])
        db.session.add(placa)
        try:
            db.session.commit()
            flash("Placa adicionada", "Sucesso")
            return redirect(url_for('placa'))
        except Exception:
            db.session.rollback()
            flash("esta placa ja existe", "error")
    return render_template('adicionar_placa.html',
                           clientes=clientes,
                           user=current_user,
                           componentes=componentes)


@app.route('/placa/editar/<int:id_placa>', methods=['POST', 'GET'])
@login_required
def edit_placa(id_placa):
    placa = Placa.query.get(id_placa)
    clientes = Cliente.query.all()

    if request.method == 'POST':
        placa.codigo = request.form['codigo'],
        placa.descricao = request.form['descricao'],
        placa.modelo = request.form['modelo'],
        placa.qtd_componentes = request.form['qtd_componentes'],
        placa.id_cliente = request.form['id_cliente']
        db.session.commit()
        return redirect(url_for('placa'))
    return render_template('editar_placa.html',
                           placa=placa,
                           user=current_user,
                           clientes=clientes)


@app.route('/placa/delete/<int:id_placa>', methods=['POST', 'GET'])
@login_required
def delete_placa(id_placa):
    placa = Placa.query.get(id_placa)
    placa.ativo = 0
    db.session.commit()
    return redirect(url_for('placa'))


@app.route('/dashboards/', methods=['POST', 'GET'])
@login_required
def dashboards():
    ops = OP.query.all()
    return render_template('dashboards.html',
                           user=current_user,
                           ops=ops)


@app.route('/api/cliente/<int:id_cliente>', methods=['GET'])
@cross_origin()
def api_placas(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    clienteDict = {}
    clienteDict['id'] = cliente.id
    clienteDict['nome'] = cliente.nome
    clienteDict['placas'] = []
    '''
    Para cada placa do cliente informado,
    adiciona as informações da mesma em um
    dict
    '''
    for placa in cliente.placas:
        if placa.ativo == 1:
            placas_cliente = {}
            placas_cliente['id'] = placa.id
            placas_cliente['codigo'] = placa.codigo
            placas_cliente['descricao'] = placa.descricao
            placas_cliente['modelo'] = placa.modelo
            clienteDict['placas'].append(placas_cliente)
            return jsonify({'cliente': clienteDict})
    return jsonify()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

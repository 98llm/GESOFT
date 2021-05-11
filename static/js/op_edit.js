///regra do formulario adicionar op
var cliente_select = document.getElementById('id_cliente');
let placa_select = document.getElementById('id_placa');




    //captura o valor selecionado no campo "cliente"
    cliente = cliente_select.value

    console.log(cliente)

    //consome a api | Json
    fetch('http://127.0.0.1:5000/api/cliente/' + cliente).then(function(response){

        response.json().then(function(data){

            let optionHTML = '';
            placas = (data.cliente.placas);

            for(let placa of placas){
                optionHTML += '<option value="' + placa.id + '">' + placa.id + ' - ' + placa.modelo + '</option>';
            }
            placa_select.innerHTML = optionHTML;
        });
    });



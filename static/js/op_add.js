///regra do formulario adicionar op
var cliente_select = document.getElementById('id_cliente');
var placa_select = document.getElementById('id_placa');


cliente_select.onchange = function () {
    //captura o valor selecionado no campo "cliente"
    cliente = cliente_select.value

    //consome a api | Json
    fetch('http://127.0.0.1:8080/api/cliente/' + cliente).then(function (response) {

        response.json().then(function (data) {
            let optionHTML = '';
            if (data.cliente) {
                placas = (data.cliente.placas);
                for (let placa of placas) {
                    if (placa) {
                        optionHTML += '<option value="' + placa.id + '">' + placa.id + ' - ' + placa.modelo + '</option>';
                    }
                }
            }
            else {
                optionHTML += '<option value="" disabled selected></option>';
            }
            placa_select.innerHTML = optionHTML;
        });
    });

};


$('.datepicker').datepicker({
    format: "dd/mm/yyyy",
    clearBtn: true,
    startDate: "-infinity",
    language: "pt-BR",
    orientation: "bottom auto",
    todayHighlight: true,
    todayBtn: "linked"
});
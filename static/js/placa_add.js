function duplicarCampos(){
	var clone = document.getElementById('origem').cloneNode(true);
	var destino = document.getElementById('destino');
	destino.appendChild(clone);

	
	// for(i=0; i<camposClonados.length;i++){
	// 	camposClonados[i].value = "";
	// }
}

function removerCampos(id){
	var teste = document.getElementsByClassName('clone')
	var node1 = document.getElementById('destino');
	tamanho = teste.length
	node1.removeChild(node1.childNodes[tamanho]);
}

  function clearInputUrlNumberText(name) {
    var destinos = document.querySelectorAll("div[id='"+name+"']");
    [].map.call(destinos, destinos => destinos.value = '');
  }

  document.getElementById("origem").addEventListener("click", function() {
    clearInputUrlNumberText("destino");
  });
function duplicarCampos(){
	var clone = document.getElementById('origem').cloneNode(true);
	var destino = document.getElementById('destino');
	var limpar = destino.appendChild(clone);
	limpar.value = ''
	var camposClonados = clone.getElementTagValue('input');
	
	// for(i=0; i<camposClonados.length;i++){
	// 	camposClonados[i].value = "";
	// }
}

function removerCampos(id){
	var node1 = document.getElementById('destino');
	node1.removeChild(node1.childNodes[0]);
}

  function clearInputUrlNumberText(name) {
    var destinos = document.querySelectorAll("div[id='"+name+"']");
    [].map.call(destinos, destinos => destinos.value = '');
  }

  document.getElementById("origem").addEventListener("click", function() {
    clearInputUrlNumberText("destino");
  });
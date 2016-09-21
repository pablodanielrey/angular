//***** Saber si un array contiene un elemento *****
Array.prototype.contains = function (element){		
	for(var i in this){
		if (this[i] == element)	return true;
	}
	return null;
};


//*****  Retornar la posicion de un elemento en un array *****
Array.prototype.position = function (element){		
	for(var i in this){
		if (this[i] == element)	return i;
	}
	return null;
};

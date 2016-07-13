
//***** Remplaza vocales acentuadas por no acentuadas, enie por ene, caracter ' por espacio en blanco *****
String.prototype.latinReplace=function(){
   return this.replace(/\u00C1/g,"A").replace(/\u00C9/g,"E").replace(/\u00CD/g,"I").replace(/\u00D1/g,"N").replace(/\u00D3/g,"O").replace(/\u00DA/g,"U").replace(/\u00E1/g,"a").replace(/\u00E9/g,"e").replace(/\u00ED/g,"i").replace(/\u00F1/g,"n").replace(/\u00F3/g,"o").replace(/\u00FA/g,"u").replace(/\u0027/g," ");
};

//***** primer caracter de una cadena en mayuscula y el resto en minuscula *****
String.prototype.ucFirst=function(){
	return this.substr(0,1).toUpperCase()+this.substr(1,this.length).toLowerCase();
};

//***** primer caracter de cada palabra en mayuscula *****
String.prototype.ucWords=function(){
	var arrayWords;
	var returnString = "";
	var len;
	arrayWords = this.split(" ");
	len = arrayWords.length;
	for(i=0;i < len ;i++){
		if(i != (len-1)){
			returnString = returnString+arrayWords[i].ucFirst()+" ";
		}else{
			returnString = returnString+arrayWords[i].ucFirst();
		}
 	}
 
 	return returnString;
};

//***** eliminar los caracteres en blanco: ' ' al principio y final del objeto receptor
String.prototype.trim=function(){
  return this.replace(/^\s+|\s+$/g, '').replace(/ +/g, ' ');
};


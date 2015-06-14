var clic = 1;
function divLogin(){
   if(clic==1){
   document.getElementById("galeria").style.visibility = "hidden";
   clic = clic + 1;
   } else{
     document.getElementById("galeria").style.visibility = "visible";
    clic = 1;
   }
}

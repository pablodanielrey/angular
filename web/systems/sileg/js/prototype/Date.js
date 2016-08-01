Date.month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
Date.month_names_short = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];


Date.prototype.getMonthName = function() {
    return Date.month_names[this.getMonth()];
};

Date.prototype.getMonthNameShort = function() {
    return Date.month_names_short[this.getMonth()];
};


Date.prototype.toISODateString = function(){
   var yyyy = this.getFullYear().toString(); 
   var mm = (this.getMonth()+1).toString(); 
   var dd  = this.getDate().toString();
   return yyyy + "-" + (mm[1]?mm:"0"+mm[0]) + "-" + (dd[1]?dd:"0"+dd[0]);
};

Date.prototype.toLocaleDateStringZero = function(){
   var yyyy = this.getFullYear().toString(); 
   var mm = (this.getMonth()+1).toString(); 
   var dd  = this.getDate().toString();
   return (dd[1]?dd:"0"+dd[0]) + "/" + (mm[1]?mm:"0"+mm[0]) + "/" + yyyy;
};

Date.prototype.createFromTimestamp = function(timestamp){
  var dateAndTime = timestamp.split(" ");
  var date = dateAndTime[0].split("-")
  var time = dateAndTime[1].split(":")
  
  var d = new Date(parseInt(date[2]), parseInt(date[1]) - 1, parseInt(date[0]), parseInt(time[2])+3, parseInt(time[1]), parseInt(time[0]));
}

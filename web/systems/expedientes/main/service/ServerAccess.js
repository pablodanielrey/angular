
app.service("ServerAccess", ["$wamp", function($wamp) {

  var schema = "expedientes.";
  
  this.findById = function(id, label) {
    return $wamp.call(schema + label + '.rowById', [id])
  }

  this.gridData = function(filterParams, label) {
    return $wamp.call(schema + label + '.gridData', [filterParams])
  }

  this.numRows = function(search, label) {
    return $wamp.call(schema + label + '.numRows', [search])
  }

}]);





app.service("Destino", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.destino.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.destino.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.destino.numRows', [search])
  }


}]);
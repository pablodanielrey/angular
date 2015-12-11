
app.service("Participacion", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.participacion.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.participacion.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.participacion.numRows', [search])
  }


}]);
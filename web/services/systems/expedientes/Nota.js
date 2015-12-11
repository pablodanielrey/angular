
app.service("Nota", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.nota.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.nota.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.nota.numRows', [search])
  }


}]);
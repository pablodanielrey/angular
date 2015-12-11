
app.service("Expediente", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.expediente.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.expediente.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.expediente.numRows', [search])
  }


}]);
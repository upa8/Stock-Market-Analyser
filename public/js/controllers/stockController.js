function stockController($scope,$rootScope,$location,$http,$websocket,restApi) {
	
	$scope.results = "";
	$scope.lastTime = "";

	// make http request to get the data 
	restApi.getStockResults().then(function(results){
			var dataInJson = JSON.parse(results);
			angular.forEach(dataInJson, function(value, key){
		  		if(key == 'time'){
		  			$scope.lastTime = value;
		  		}else{
		  			$scope.results = value;
				}
			});
  		},function(err){
			console.log("Error in restApi");
		}
	);

	var dataStream = $websocket('ws://54.242.218.128:9000/sock/ws');
	//var dataStream = $websocket('ws://127.0.0.1:9000/sock/ws');

    dataStream.onMessage(function(message) {
	   	var dataInJson = JSON.parse(message.data);
	  	angular.forEach(dataInJson, function(value, key){
	  		if(key == 'time'){
			  	$scope.lastTime = value;
	  		}else{
	  			$scope.results = value;
			}
	  	});
   	});

	dataStream.onOpen(function() {
	  //console.log('connection open');
	});

	dataStream.onError(function(event) {
 	 console.log('connection Error', event);
	});

	dataStream.onClose(function(event) {
    	console.log('connection closed', event);
	});
}

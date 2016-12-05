function stockController($scope,$rootScope,$location,$http,$websocket,restApi) {
	console.log("Home controller");
	
	$scope.results = "";

	if($scope.results == ""){
		$scope.results = "Data is yet to arrive";
	}

	// make http request to get the data 

	restApi.getStockResults().then(function(results){
				//var data = JSON.parse(results.data);
	  			console.log("Got result "+results);
			},function(err){
				console.log("Error in results");
			});

	
	//var dataStream = $websocket('ws://54.242.218.128:9000/sock/ws');
	var dataStream = $websocket('ws://127.0.0.1:9000/sock/ws');

    dataStream.onMessage(function(message) {
	   	var dataInJson = JSON.parse(message.data);
	  	//console.log("Recieved message "+ JSON.stringify(JSON.parse(message.data),null,4));
	  	//console.log("Time+dataInJson.time "+typeof(dataInJson));
	  	angular.forEach(dataInJson, function(value, key){
	  		if(key == 'time'){
	  			console.log('TIme ' + value);
	  		}else{
	  			console.log(JSON.stringify(value[0],null,4));
	  		}
	  		/*console.log(typeof(key) +" key "+ key);
	  		console.log(typeof(value) +" value "+ value);*/
	  	});
	  	$scope.results = message.data['time'];
   	});

	dataStream.onOpen(function() {
	  console.log('connection open');
	  dataStream.send('Hello World');
	});

	dataStream.onError(function(event) {
 	 console.log('connection Error', event);
	});

	dataStream.onClose(function(event) {
    	console.log('connection closed', event);
	});
    
}

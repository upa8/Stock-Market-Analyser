function restApi($q,$rootScope,$http) {
	
	var baseUrl = 'http://54.242.218.128:9000/api';
	//var baseUrl =  'http://127.0.0.1:9000/api';
	
	var restApi = {};
	
	// getStock results
	restApi.getStockResults = function(username,password){
			var defer=$q.defer();
			$.ajax({
		        type: "GET",
		        url: baseUrl +'/get_latest_data',
		        contentType: "application/json",
		        headers: {
	        		'Access-Control-Allow-Origin': baseUrl 
		        },
		        async:true,
		        success: function(data, textStatus, xhr){
		            defer.resolve(data);
		        },
		        error: function(data, textStatus, xhr){
		            defer.reject(data);
		        },
		        timeout: 15000 
		    });
			return defer.promise;
	};
	return restApi;
}

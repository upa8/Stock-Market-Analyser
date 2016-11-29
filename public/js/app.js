var stockMarketAnalyser = angular.module('stockMarketAnalyser', ['ngRoute','ngWebSocket']);

// ecomApp config Config method
stockMarketAnalyser.config(function($routeProvider){
	// Put all the routing here 
	$routeProvider

		.when('/', {
			controller: 'stockController',
			templateUrl: 'views/stock/displayStock.html'
		})
		.otherwise({redirectTo: '/notFound'})
});

// Custome directives

// Register all the factories 

// Register all the controllers 
stockMarketAnalyser.controller('stockController', stockController);



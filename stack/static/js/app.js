/**
* You must include the dependency on 'ngMaterial' 
*/

var app = angular.module('StarterApp', ['ngMaterial', 'ngMdIcons', 'ngResource']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.config(function($mdThemingProvider) {
  var customBlueMap =     $mdThemingProvider.extendPalette('light-blue', {
  'contrastDefaultColor': 'light',
  'contrastDarkColors': ['50'],
  '50': 'ffffff'
});

$mdThemingProvider.definePalette('customBlue', customBlueMap);

$mdThemingProvider.theme('default').primaryPalette('customBlue', {
  'default': '500',
  'hue-1': '50'
}).accentPalette('pink');

$mdThemingProvider.theme('input', 'default')
    .primaryPalette('grey')
});


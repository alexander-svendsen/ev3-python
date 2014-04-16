
//--------------
// Initializers
//--------------
define([
    'jquery',
    'underscore',
    'backbone',
    'router' // Request router.js
], function($, _, Backbone, Router){
  var initialize = function(){
    console.log("Things are starting properly");
    Router.initialize();
  };

  return {
    initialize: initialize
  };
});
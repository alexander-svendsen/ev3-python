//var LegoApplication = LegoApplication || {};
//
//LegoApplication.SensorCollection = Backbone.Collection.extend({
//    model: LegoApplication.SensorModel,
//    localStorage: new Store("sensor-mockups") //Todo: remove when there is a backend
////    url: "stops"
//});


define([
  'underscore',
  'backbone',
  'models/sensor'
], function(_, Backbone, SensorModel){
    var SensorCollection = Backbone.Collection.extend({
        model: SensorModel,

        initialize : function(){
            this.initialize_websocket("ws://127.0.1.1:9999/");
//            this.subscribe_on_brick('10.0.1.1');
        },
        set_sensor_collection : function(raw_data){

        },
        subscribe_on_brick : function(brick_address){
            this.socket.send(brick_address)
        },
        initialize_websocket: function(address) {
            this.socket = new WebSocket(address);
            this.socket.onopen = function(){
                console.log("Socket has been opened!"); // TODO: should start subscription somewhere
            };
            this.socket.onmessage = function(msg){
        //        console.log(msg);
                //should be in the form
                // { port : {
                //           sensor: color....
                //           mode: id_mode
                //           sample: [0.0]
                // }}
            };
            this.socket.onerror = function(msg){
                alert(msg);
            };
            this.socket.onclose = function(msg){
        //        alert(msg);
            };
        }
    });
    return SensorCollection;
});
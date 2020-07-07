var util = require('util');
var bleno = require('../');

var rasp = require('./rasp');
var RaspService = require('./rasp-service');

var name = 'RaspBleWDJ';
// rsap 의  Rasp() 의 events.EventEmitter.call(this); 와 데이터 셋팅
var raspService = new RaspService(new rasp.Rasp());

bleno.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    bleno.startAdvertising(name, [raspService.uuid], function(err) {
      if (err) {
        console.log(err);
      }
    });
  }
  else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(err) {
  if (!err) {
    console.log('advertising...');
    bleno.setServices([
      raspService
    ]);
  }
});

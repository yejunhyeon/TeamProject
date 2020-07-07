var util = require('util');
var bleno = require('../');
var rasp = require('./rasp');

function RaspInfoCharacteristic(rasp) {
  bleno.Characteristic.call(this, {
    uuid: '13333333333333333333333333330003',
    properties: ['notify', 'write'],
    descriptors: [
      new bleno.Descriptor({
        uuid: '2901',
        value: 'Mobile -> Request and Response, Notifies'
      })
    ]
  });

  this.rasp = rasp;
}

util.inherits(RaspInfoCharacteristic, bleno.Characteristic);

RaspInfoCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
  console.log("rasp-info-characteristic");
  if (offset) {
    callback(this.RESULT_ATTR_NOT_LONG);
  }
  else if (data.length !== 2) {
    callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
  }
  else {
    var temperature = data.readUInt16BE(0);
    var self = this;
    this.rasp.once('ready', function(result) {
      console.log(result);
      console.log("rasp-info-ready-callback");
      if (self.updateValueCallback) {
        var data = new Buffer(1);
        data.writeUInt8(result, 0);
        self.updateValueCallback(data);
      }
    });
    this.rasp.info(temperature);
    callback(this.RESULT_SUCCESS);
  }
};

module.exports = RaspInfoCharacteristic;
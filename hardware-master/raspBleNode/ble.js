// ex -> https://qiita.com/comachi/items/c494e0d6c6d1775a3748
// doc -> https://npmdoc.github.io/node-npmdoc-bleno/build/apidoc.html#apidoc.tableOfContents
// uuid -> https://www.uuidgenerator.net/version4

var util = require('util');
var bleno = require('bleno');

var MY_SERVICE_UUID = '13333333-3333-3333-3333-333333333307';
var NOTIFY_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333301';
var READ_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333302';
var WRITE_CHARACTERISTIC_UUID = '13333333-3333-3333-3333-333333333303';
var DEVICE_NAME = 'WDJ';

let counter = 0;

var Characteristic = bleno.Characteristic;
var PrimaryService = bleno.PrimaryService;

////////// ////////// ////////// ////////// //////////

var NotifyCharacteristic = function() {
  NotifyCharacteristic.super_.call(this, {
    uuid : NOTIFY_CHARACTERISTIC_UUID,
    properties: ['notify'],
    value : null
  });
  this._value = 0;
  this._updateValueCallback = null;
};

var ReadCharacteristic = function() {
  ReadCharacteristic.super_.call(this, {
    uuid : READ_CHARACTERISTIC_UUID,
    properties: ['read'],
    value : null
  });
  this._value = 0;
  this._updateValueCallback = null;
};

var WriteCharacteristic = function() {
  WriteCharacteristic.super_.call(this, {
    uuid : WRITE_CHARACTERISTIC_UUID,
    properties: ['write'],
    value : null
  });
  this._value = 0;
  this._updateValueCallback = null;
};

util.inherits(NotifyCharacteristic, Characteristic);
util.inherits(ReadCharacteristic, Characteristic);
util.inherits(WriteCharacteristic, Characteristic);

////////// ////////// ////////// ////////// //////////

NotifyCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
  console.log('Characteristic - onSubscribe');
  this._updateValueCallback = updateValueCallback;
};

NotifyCharacteristic.prototype.onUnsubscribe = function() {
  console.log('Characteristic - onUnsubscribe');
  this._updateValueCallback = null;
};

ReadCharacteristic.prototype.onReadRequest = function(offset, callback) {
  console.log("onReadRequest");
  callback(this.RESULT_SUCCESS, [1]);
}

WriteCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
  console.log("onWriteRequest"+data);
  notifyCharacteristic._updateValueCallback([0]);
  callback(this.RESULT_SUCCESS);
}

////////// ////////// ////////// ////////// //////////

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);
  if (state === 'poweredOn') {
    bleno.startAdvertising(DEVICE_NAME, [MY_SERVICE_UUID]);
  } else {
    bleno.stopAdvertising();
  }
});

var notifyCharacteristic = new NotifyCharacteristic();
var readCharacteristic = new ReadCharacteristic();
var writeCharacteristic = new WriteCharacteristic();

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));
  if(!error) {
    bleno.setServices([
      new PrimaryService({
        uuid: MY_SERVICE_UUID,
        characteristics: [
          notifyCharacteristic,
          readCharacteristic,
          writeCharacteristic
        ]
      })
    ]);
  }
});

////////// ////////// ////////// ////////// //////////

setInterval(()=>{
  counter++;
  notifyCharacteristic._value = counter;
  if (notifyCharacteristic._updateValueCallback) {
    console.log(`Sending notification with value : ${notifyCharacteristic._value}`);

    const notificationBytes = Buffer.from(String(notifyCharacteristic._value));
    notifyCharacteristic._updateValueCallback(notificationBytes);
  }
}, 1000);
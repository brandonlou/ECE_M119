const noble = require('@abandonware/noble');

const uuid_service = '1101'
const uuid_accel_x = '2101'
const uuid_accel_y = '2102'
const uuid_accel_z = '2103'

noble.on('stateChange', async (state) => {
  if (state === 'poweredOn') {
    console.log('Scanning...')
    await noble.startScanningAsync([uuid_service], false);
  }
});

noble.on('discover', async (peripheral) => {
  await noble.stopScanningAsync();
  await peripheral.connectAsync();
  const {characteristics} = await peripheral.discoverSomeServicesAndCharacteristicsAsync([uuid_service], [uuid_accel_x, uuid_accel_z, uuid_accel_y]);
  readData(characteristics)
});

/* Read data periodically */
let readData = async (characteristic) => {
  const xValue = (await characteristic[0].readAsync());
  const yValue = (await characteristic[1].readAsync());
  const zValue = (await characteristic[2].readAsync());

  console.log(`${xValue.readFloatLE(0)}, ${yValue.readFloatLE(0)}, ${zValue.readFloatLE(0)}`);

  /* Read again in 10 ms */
  setTimeout(() => {
    readData(characteristic)
  }, 10);
}


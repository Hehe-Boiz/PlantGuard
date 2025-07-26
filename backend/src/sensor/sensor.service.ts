// src/services/sensor.service.ts
import { Injectable } from '@nestjs/common';
import { Cron } from '@nestjs/schedule';
import { SensorGateway } from './sensor.gateway';
import { SensorDataDto } from './dto/sensor-data.dto';

@Injectable()
export class SensorService {
  constructor(private readonly gateway: SensorGateway) {}

  // Ví dụ: mỗi giây gửi 1 lần
  @Cron('*/1 * * * * *')
  handleCron() {
    const fakeData: SensorDataDto = {
      temperature: random(20, 30),
      humidity: random(40, 60),
      wind: random(0, 5),
      soilMoisture: random(30, 80),
      pH: parseFloat((6 + Math.random()).toFixed(2)),
    };
    this.gateway.broadcastSensorData(fakeData);
  }
}

function random(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

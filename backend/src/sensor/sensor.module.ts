import { Module } from '@nestjs/common';

import { SensorGateway } from './sensor.gateway';
import { SensorService } from './sensor.service';
import { ScheduleModule } from '@nestjs/schedule';

@Module({
  imports: [
    ScheduleModule.forRoot(), // để dùng @Cron
  ],
  providers: [SensorGateway, SensorService],
})
export class SensorModule {}

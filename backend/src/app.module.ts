import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DbconnectionModule } from './dbconnection/dbconnection.module';
import { DetectModule } from './detect/detect.module';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [DbconnectionModule, DetectModule, HttpModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

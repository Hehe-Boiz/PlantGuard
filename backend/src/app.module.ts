import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DbconnectionModule } from './dbconnection/dbconnection.module';

@Module({
  imports: [DbconnectionModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

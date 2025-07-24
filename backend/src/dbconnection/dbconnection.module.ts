import { Global, Module } from '@nestjs/common';
import { DbconnectionService } from './dbconnection.service';

@Global()
@Module({
  providers: [DbconnectionService],
  exports: [DbconnectionService],
})
export class DbconnectionModule {}

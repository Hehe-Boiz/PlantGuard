/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  ConnectedSocket,
  MessageBody,
  OnGatewayConnection,
  OnGatewayDisconnect,
  OnGatewayInit,
  SubscribeMessage,
  WebSocketGateway,
  WebSocketServer,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { SensorDataDto } from './dto/sensor-data.dto';

@WebSocketGateway(8000, {
  path: '/ws',
  cors: { origin: '*' },
})
export class SensorGateway
  implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect
{
  @WebSocketServer()
  server: Server;

  afterInit(server: Server) {
    console.log('>> WebSocket server initialized');
  }

  handleConnection(client: Socket) {
    console.log('>> Client connected');
  }

  handleDisconnect(client: Socket) {
    console.log('>> Client disconnected');
  }

  @SubscribeMessage('message')
  onMessage(@MessageBody() data: any, @ConnectedSocket() client: Socket) {
    console.log(`Received message from ${client.id}:`, data);
    client.emit('messageAck', { status: 'ok' });
  }

  @SubscribeMessage('sensorData')
  broadcastSensorData(data: SensorDataDto) {
    this.server.emit('sensorData', data);
  }
}

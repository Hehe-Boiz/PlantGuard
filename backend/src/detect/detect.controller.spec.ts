import { Test, TestingModule } from '@nestjs/testing';
import { DetectController } from './detect.controller';

describe('DetectController', () => {
  let controller: DetectController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DetectController],
    }).compile();

    controller = module.get<DetectController>(DetectController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});

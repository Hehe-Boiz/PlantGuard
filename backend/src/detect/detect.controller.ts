import {
  Controller,
  HttpException,
  HttpStatus,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { DetectService } from './detect.service';
import { FileInterceptor } from '@nestjs/platform-express';
import { InferImageDto } from './dto/infer-image.dto';

@Controller('detect')
export class DetectController {
  constructor(private readonly detectService: DetectService) {}

  @Post('image')
  @UseInterceptors(FileInterceptor('image'))
  async uploadImage(@UploadedFile() file: InferImageDto) {
    if (!file) {
      throw new HttpException('No file uploaded', HttpStatus.BAD_REQUEST);
    }
    console.log(file);
    return this.detectService.detectImage(
      file.image.buffer,
      file.image.mimetype,
    );
  }
}

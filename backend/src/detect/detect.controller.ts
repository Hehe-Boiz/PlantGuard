import {
  Body,
  Controller,
  HttpException,
  HttpStatus,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { DetectService } from './detect.service';
import { FileInterceptor } from '@nestjs/platform-express';
import { memoryStorage } from 'multer';
import { ImageJsonDto } from './dto/image-json.dto';
import { writeFile } from 'fs/promises';

@Controller('detect')
export class DetectController {
  constructor(private readonly detectService: DetectService) {}

  @Post('image')
  @UseInterceptors(
    FileInterceptor('image', {
      storage: memoryStorage(),
      limits: { fileSize: 50 * 1024 * 1024 },
    }),
  )
  async uploadImage(@UploadedFile() file: Express.Multer.File) {
    console.log(file);
    if (!file) {
      throw new HttpException(
        'No file uploaded under field "image"',
        HttpStatus.BAD_REQUEST,
      );
    }
    return this.detectService.detectImage(file.buffer, file.mimetype);
  }

  @Post('image-json')
  async uploadImageJson(@Body() body: ImageJsonDto) {
    const imageBuffer = Buffer.from(body.imageData, 'base64');

    await writeFile(`${body.filename}`, imageBuffer);
    return { message: 'Upload successfully', filename: body.filename };
  }
}

import { HttpService } from '@nestjs/axios';
import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { AxiosResponse } from 'axios';
import FormData from 'form-data';
import { firstValueFrom } from 'rxjs';
import { DetectionResponseDto } from './dto/detect-response.dto';

@Injectable()
export class DetectService {
  constructor(private readonly http: HttpService) {}
  private readonly modelUrl =
    process.env.PYTHON_MODEL_URL || 'http://python-ai:8000';

  async detectImage(imageBuf: Buffer, mimeType: string) {
    try {
      const form = new FormData();
      form.append('image', imageBuf, {
        filename: 'upload',
        contentType: mimeType,
      });

      const { data } = await firstValueFrom<
        AxiosResponse<DetectionResponseDto>
      >(
        this.http.post(this.modelUrl, form, {
          headers: form.getHeaders(),
        }),
      );
      return data;
    } catch {
      throw new HttpException(
        'AI service unavailable',
        HttpStatus.SERVICE_UNAVAILABLE,
      );
    }
  }
}

import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { AxiosResponse } from 'axios';
import FormData from 'form-data';
import { firstValueFrom } from 'rxjs';
import { InferResponseDto } from './dto/infer-response.dto';

@Injectable()
export class DetectService {
  constructor(private readonly http: HttpService) {}
  private readonly modelUrl =
    process.env.PYTHON_MODEL_URL || 'http://python-ai:8000';

  async detectImage(imageBuffer: Buffer, mimetype: string) {
    const form = new FormData();
    form.append('file', imageBuffer, {
      filename: 'upload.jpg',
      contentType: mimetype,
    });

    const { data } = await firstValueFrom<AxiosResponse<InferResponseDto>>(
      this.http.post(this.modelUrl, form, {
        headers: form.getHeaders(),
      }),
    );
    return data;
  }
}

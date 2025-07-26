import { IsNotEmpty } from 'class-validator';

export class ImageJsonDto {
  @IsNotEmpty()
  filename: string;

  @IsNotEmpty()
  imageData: string;
}

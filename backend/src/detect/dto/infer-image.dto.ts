import { IsNotEmpty } from 'class-validator';

export class InferImageDto {
  @IsNotEmpty()
  image: Express.Multer.File;
}

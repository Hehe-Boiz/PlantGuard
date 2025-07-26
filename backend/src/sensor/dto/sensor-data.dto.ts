import { IsDecimal } from 'class-validator';

export class SensorDataDto {
  @IsDecimal({ decimal_digits: '3' })
  temperature: number;

  @IsDecimal({ decimal_digits: '3' })
  humidity: number;

  @IsDecimal({ decimal_digits: '3' })
  wind: number;

  @IsDecimal({ decimal_digits: '3' })
  soilMoisture: number;

  @IsDecimal({ decimal_digits: '3' })
  pH: number;
}

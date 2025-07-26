export interface DetectionItem {
  detection_box: [number, number, number, number];
  detection_confidence: number;
  cropped_image_file: string;
}

export interface DetectionResponseDto {
  original_image: string;
  detections_found: number;
  results: DetectionItem[];
}

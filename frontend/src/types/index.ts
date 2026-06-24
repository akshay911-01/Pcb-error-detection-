export interface Defect {
  class: string;
  count: number;
}

export interface PredictResponse {
  image: string; // Base64 encoded image
  detections: Defect[];
}

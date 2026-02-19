export interface SessionResponse {
  session_id: string;
  created_at: string;
}

export interface DocumentUploadResponse {
  id: string;
  session_id: string;
  filename: string;
  document_type: string;
  file_size_bytes: number;
  created_at: string;
}

export interface DocumentListResponse {
  documents: DocumentUploadResponse[];
}

export interface RiskFinding {
  category: string;
  severity: string;
  title: string;
  description: string;
  source: string;
}

export interface RiskScore {
  overall_score: number;
  risk_level: string;
  category_scores: Record<string, number>;
  findings: RiskFinding[];
}

export interface BiddingAdvice {
  strategy: string;
  min_price: number;
  max_price: number;
  recommended_price: number;
  explanation: string;
}

export interface PropertyData {
  address?: string | null;
  postal_code?: string | null;
  city?: string | null;
  square_meters?: number | null;
  year_built?: number | null;
  energy_label?: string | null;
  property_type?: string | null;
  asking_price?: number | null;
  hoa_monthly_cost?: number | null;
  num_rooms?: number | null;
  has_garden?: boolean | null;
  has_parking?: boolean | null;
}

export interface AnalysisResponse {
  id: string;
  session_id: string;
  status: string;
  property_data: PropertyData | null;
  strengths: string[];
  weaknesses: string[];
  risk_score: RiskScore | null;
  market_position: MarketPosition | null;
  bidding_advice: Record<string, BiddingAdvice> | null;
  created_at: string;
  completed_at: string | null;
  error_message: string | null;
}

export interface AnalysisStatusResponse {
  session_id: string;
  status: string;
  progress_message: string;
}

export interface MarketPosition {
  bag_data?: Record<string, unknown> | null;
  energy_label_data?: Record<string, unknown> | null;
  area_statistics?: Record<string, unknown> | null;
}

export interface MarketDataResponse {
  municipality: string | null;
  avg_purchase_price: number | null;
  num_transactions: number | null;
  price_index: number | null;
  period: string | null;
  bag_data: Record<string, unknown> | null;
  energy_label_data: Record<string, unknown> | null;
}

export interface OrderItem {
  id: number;
  product: number | null;
  product_name: string;
  quantity: number;
  price_at_purchase: string;
}

export interface Order {
  id: number;
  user: number | null;
  tracking_number: string;
  total_amount: string;
  status: string;
  shipping_address: {
    full_name?: string;
    phone?: string;
    city?: string;
    address_line?: string;
  } | null;
  created_at: string;
  items: OrderItem[];
}

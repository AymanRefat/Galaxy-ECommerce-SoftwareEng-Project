export interface CartItem {
  id: number;
  product: number;
  product_name: string;
  price: string;
  quantity: number;
}

export interface Cart {
  id: number;
  user: number | null;
  session_id: string | null;
  created_at: string;
  items: CartItem[];
  total_price: string;
}

export interface CheckoutPayload {
  payment_token: string;
  shipping_address: {
    full_name: string;
    phone: string;
    city: string;
    address_line: string;
  };
}

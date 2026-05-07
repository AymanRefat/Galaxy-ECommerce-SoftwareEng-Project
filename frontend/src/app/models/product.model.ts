export interface ProductImage {
  id: number;
  image: string;
  is_primary: boolean;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  parent: number | null;
}

export interface Product {
  id: number;
  vendor_name: string;
  category: Category | null;
  name: string;
  description: string;
  price: number;
  stock_quantity: number;
  sku: string;
  images: ProductImage[];
  average_rating: number;
  created_at: string;
  updated_at: string;
}

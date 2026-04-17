export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

// Type definitions matching Backend Serializers
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
  category: Category;
  name: string;
  description: string;
  price: number;
  stock_quantity: number;
  sku: string;
  images: ProductImage[];
  created_at: string;
  updated_at: string;
}

export async function getProducts(categorySlug?: string): Promise<Product[]> {
  const url = categorySlug 
    ? `${API_BASE_URL}/api/products/?category__slug=${categorySlug}`
    : `${API_BASE_URL}/api/products/`;
  
  // Use a slightly different URL for Server Side Rendering if needed
  // In a real Docker env, this might need to be 'http://backend:8000/api/...'
  // but since Nginx is proxying at port 80, the client-facing port 80 works for both if configured correctly.
  
  const res = await fetch(url, { cache: 'no-store' });
  
  if (!res.ok) {
    throw new Error('Failed to fetch products');
  }
  
  return res.json();
}

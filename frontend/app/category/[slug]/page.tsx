import { ProductCard } from '@/components/ui/ProductCard';
import { getProducts } from '@/lib/api';

export default async function CategoryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const products = await getProducts(slug);

  return (
    <div className="container mx-auto px-4 py-16">
      <div className="mb-12">
        <h1 className="text-4xl font-bold capitalize">{slug.replace('-', ' ')}</h1>
        <p className="text-gray-500 mt-2 text-lg">Browse the best products in {slug}.</p>
      </div>

      {products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {products.map(product => (
            <ProductCard key={product.id} {...product} />
          ))}
        </div>
      ) : (
        <div className="bg-gray-50 rounded-xl p-16 text-center border-2 border-dashed border-gray-200">
          <p className="text-gray-500">We currently do not have any products in this category.</p>
        </div>
      )}
    </div>
  );
}

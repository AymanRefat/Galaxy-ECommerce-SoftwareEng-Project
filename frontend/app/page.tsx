import { mockProducts } from '@/lib/mockProducts';
import { ProductCard } from '@/components/ui/ProductCard';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export default function Home() {
  const featured = mockProducts.slice(0, 4);

  return (
    <div className="flex flex-col">
      <section className="relative h-[65vh] min-h-[500px] flex items-center justify-center overflow-hidden">
        {/* Deep dark base for maximum contrast */}
        <div className="absolute inset-0 bg-slate-950 z-0"></div>
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=2000')] bg-cover bg-center mix-blend-overlay opacity-30 z-0"></div>
        
        {/* Additional gradient overlay specifically for text readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-900/40 to-transparent z-0"></div>
        
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto space-y-6 animate-in slide-in-from-bottom-8 duration-700">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight drop-shadow-[0_4px_4px_rgba(0,0,0,0.5)]">
            Next Generation E-Commerce
          </h1>
          <p className="text-xl md:text-2xl text-slate-200 font-medium max-w-2xl mx-auto drop-shadow-md">
            Discover premium products or launch your own digital storefront today with Galaxy Store.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
            <Link href="/search">
              <Button size="lg" className="w-full sm:w-auto font-bold px-10 py-6 text-lg shadow-2xl cursor-pointer">
                Start Shopping
              </Button>
            </Link>
            <Link href="/seller/register">
              <Button size="lg" className="w-full sm:w-auto bg-black/40 backdrop-blur-md border border-white/30 text-white hover:bg-black/60 font-bold px-10 py-6 text-lg shadow-2xl cursor-pointer">
                Become a Seller
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <section className="py-24 container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight">Featured Categories</h2>
          <div className="flex flex-wrap justify-center gap-4 mt-8">
            {['Electronics', 'Accessories', 'Furniture', 'Home-Goods'].map(cat => (
              <Link key={cat} href={`/category/${cat.toLowerCase()}`}>
                <Button variant="secondary" className="px-8 py-6 text-lg rounded-full shadow hover:shadow-md hover:-translate-y-0.5 transition-all capitalize border border-border cursor-pointer">
                  {cat.replace('-', ' ')}
                </Button>
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-32">
          <div className="flex justify-between items-end mb-8 border-b border-border pb-4">
            <h2 className="text-3xl font-bold tracking-tight">Trending Products</h2>
            <Link href="/search" className="text-primary hover:underline font-medium">View all curated items -{">"}</Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {featured.map(product => (
              <ProductCard key={product.id} {...product} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

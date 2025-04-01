import Link from "next/link";

export default function Home() {
  return (
    <main>
      <h1 className="text-3xl font-bold text-blue-600">Hello, Next.js!</h1>
      <div>
        <Link href="/blog">Blog</Link>
      </div>
      <div>
        <Link href="/rss">RSS</Link>
      </div>
    </main>
  );
}

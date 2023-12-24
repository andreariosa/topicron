import Link from "next/link";

import { getAllFeeds } from "@/lib/rss/parser";

export default async function Rss() {
  const allFeeds = await getAllFeeds();

  return (
    <>
      <ul>
        {allFeeds.map(({ slug, title }) => (
          <li key={slug}>
            <Link href={`/rss/${slug}`}>{title}</Link>
          </li>
        ))}
      </ul>
      <Link href="/">&larr; Home</Link>
    </>
  );
}

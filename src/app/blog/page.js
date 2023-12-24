import Link from "next/link";

import { getSortedPostsData } from "@/lib/blog/posts";
import BlogDate from "@/components/blog/date";

export default function Blog() {
  const allPostsData = getSortedPostsData();

  return (
    <>
      <ul>
        {allPostsData.map(({ id, date, title }) => (
          <li key={id}>
            <div>
              <Link href={`/blog/${id}`}>{title}</Link>
            </div>
            <small>
              <BlogDate dateString={date} />
            </small>
          </li>
        ))}
      </ul>
      <Link href="/">&larr; Home</Link>
    </>
  );
}

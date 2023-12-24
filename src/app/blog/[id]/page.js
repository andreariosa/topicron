import Link from "next/link";

import { getPostData } from "@/lib/blog/posts";
import BlogDate from "@/components/blog/date";

export async function generateMetadata({ params }) {
  const postData = await getPostData(params.id);

  return {
    title: postData.title,
  };
}

export default async function Post({ params }) {
  const postData = await getPostData(params.id);

  return (
    <>
      <h1>{postData.title}</h1>
      <div>
        <BlogDate dateString={postData.date} />
      </div>
      <div dangerouslySetInnerHTML={{ __html: postData.contentHtml }} />
      <div>
        <Link href="/blog">&larr; Back</Link>
      </div>
    </>
  );
}

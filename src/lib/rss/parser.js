import path from "path";
import { promises as fs } from "fs";

import rssParser from "rss-parser";

// Load Data from a File in Next.js
// https://vercel.com/guides/loading-static-file-nextjs-api-route
const feedsFile = path.join(process.cwd(), "rss/feeds.json");

export async function getAllFeeds() {
  const feeds = await fs.readFile(feedsFile, "utf8");
  const feedsData = JSON.parse(feeds);

  return feedsData;
}

export async function getFeedData(slug) {
  const feeds = await fs.readFile(feedsFile, "utf8");
  const feedsData = JSON.parse(feeds);
  const data = feedsData.filter((feed) => feed.slug.includes(slug));

  return data[0];
}

export async function getFeedRssData(url) {
  // Use rss-parser to parse the feed metadata
  const rss = new rssParser();
  const feed = await rss.parseURL(url);

  return feed;
}

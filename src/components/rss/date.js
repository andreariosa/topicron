"use client";

import { format } from "date-fns";

export default function RssDate({ dateString }) {
  return (
    <time dateTime={dateString}>{format(new Date(dateString), "PPP")}</time>
  );
}

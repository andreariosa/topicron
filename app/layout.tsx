import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Topicron",
  description:
    "A research publication for people who read markets more than they trade them.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}

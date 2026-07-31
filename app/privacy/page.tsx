// Privacy policy page. Static content only — Topicron does not currently
// use cookies or analytics, so nothing here should imply otherwise.

import Link from "next/link";

export default function PrivacyPolicy() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 px-6 py-16">
      <div className="space-y-2">
        <Link
          href="/"
          className="text-sm text-slate-500 underline underline-offset-2 hover:text-slate-700"
        >
          ← Back to Topicron
        </Link>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Privacy Policy
        </h1>
        <p className="text-sm text-slate-500">Last updated: July 31, 2026</p>
      </div>

      <p className="text-base leading-relaxed text-slate-700">
        Topicron (&quot;we,&quot; &quot;us&quot;) operates topicron.vercel.app.
        This page explains what information we collect and how we use it.
        Topicron is an early-stage, pre-revenue research project — this
        policy is deliberately short because the site currently does very
        little with personal data.
      </p>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          What we collect
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          The only personal information we collect directly is the email
          address you provide if you sign up for our mailing list. We do not
          require an account, and we do not collect names, payment
          information, or other personal details.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          How we use it
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          Your email address is used solely to send you Topicron&apos;s
          research content (a periodic digest). We do not sell, rent, or
          share your email address with any third party for marketing
          purposes.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          Who processes it
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          We use Resend (resend.com) as our email delivery provider. Your
          email address is stored in Resend&apos;s systems to manage the
          mailing list and send you content. Resend&apos;s own privacy policy
          governs how they handle this data on our behalf.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          Hosting and basic logs
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          This site is hosted on Vercel. Like most web hosts, Vercel
          automatically logs basic technical information (such as IP address
          and browser type) for security and reliability purposes. We do not
          currently use cookies or analytics tracking on this site.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          Your choices
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          Every email we send includes an unsubscribe link. You can also
          email us at{" "}
          <a
            href="mailto:andrea.riosa@hotmail.it"
            className="font-semibold text-slate-900 underline underline-offset-2"
          >
            andrea.riosa@hotmail.it
          </a>{" "}
          to request that we delete your email address from our list.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">
          Changes to this policy
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          If Topicron starts collecting additional information (for example,
          if we add site analytics or a paid subscription), we will update
          this page and note the change here.
        </p>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-slate-900">Contact</h2>
        <p className="text-base leading-relaxed text-slate-700">
          Questions about this policy:{" "}
          <a
            href="mailto:andrea.riosa@hotmail.it"
            className="font-semibold text-slate-900 underline underline-offset-2"
          >
            andrea.riosa@hotmail.it
          </a>
        </p>
      </div>
    </main>
  );
}

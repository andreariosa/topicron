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
        <p className="text-sm text-slate-500">Last updated: November 3, 2026</p>
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
        <p className="text-base leading-relaxed text-slate-700">
          If you answer our optional survey, we also receive your answers:
          the choices you tick and any text you write. The survey does not ask
          for your name or email address, so please do not put personal
          details in the free-text box.
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
        <p className="text-base leading-relaxed text-slate-700">
          The survey is a form hosted by Tally (tally.so), a separate website
          that this site links to and does not embed. Your answers are stored
          in our Tally account. How Tally handles technical data when you
          open its form is described in{" "}
          <a
            href="https://tally.so/help/privacy-policy"
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-slate-900 underline underline-offset-2"
          >
            Tally&apos;s own privacy policy
          </a>
          . We use the answers only to understand whether Topicron is useful.
          We may report them as totals and quote free-text answers without
          any personal details.
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
        <p className="text-base leading-relaxed text-slate-700">
          Survey answers are anonymous, so we cannot tell which answers are
          yours and cannot delete them on request. Our plan with Tally does
          not delete answers automatically; we will delete them when we no
          longer need them.
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

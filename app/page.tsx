// M0 landing page (docs/ROADMAP.md, M0 deliverable: "landing page + email
// list live"). Deliberately minimal, single hand-built page and endpoint —
// expected to be superseded by the real public topic/thesis pages in M3
// (docs/ROADMAP.md, M3: "Publication v1").

import Link from "next/link";
import { SubscribeForm } from "./subscribe-form";

// Public links. The thesis files live in the public repository until the
// public thesis pages exist (docs/ROADMAP.md, M3). The survey is a Tally form
// (ADR-0004, D-34): it is linked, never embedded, so this page keeps loading
// no third-party script and setting no cookies.
const REPO_URL = "https://github.com/andreariosa/topicron/blob/main/m0";
const ONE_PAGE_URL = `${REPO_URL}/topic-thesis-13-one-page.md`;
const FULL_TEXT_URL = `${REPO_URL}/topic-thesis-13-us-wireless-spacex.md`;
const SURVEY_URL = "https://tally.so/r/OQaZNk";

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-10 px-6 py-16">
      <div className="space-y-4">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
          Topicron
        </h1>
        <p className="text-lg text-slate-600">
          A research publication for people who read markets more than they
          trade them.
        </p>
      </div>

      <p className="text-base leading-relaxed text-slate-700">
        Every week, Topicron surfaces an emerging investment narrative — the
        kind you&apos;d otherwise only encounter as an unexplained headline —
        and builds the structured case around it: a bull case, a bear case,
        and the risks that could derail either one. Then we track what
        actually happens, including when we&apos;re wrong.
      </p>

      <ul className="space-y-5">
        <li className="flex gap-3">
          <span aria-hidden="true" className="text-slate-400">
            01
          </span>
          <p className="text-slate-700">
            <span className="font-semibold text-slate-900">
              The argument, not the alert.
            </span>{" "}
            A bull case and a bear case, argued with equal seriousness — not
            a buy/sell signal.
          </p>
        </li>
        <li className="flex gap-3">
          <span aria-hidden="true" className="text-slate-400">
            02
          </span>
          <p className="text-slate-700">
            <span className="font-semibold text-slate-900">
              Grounded and cited.
            </span>{" "}
            Every claim traces back to real source material — no fabricated
            facts, no confident guesses dressed up as certainty.
          </p>
        </li>
        <li className="flex gap-3">
          <span aria-hidden="true" className="text-slate-400">
            03
          </span>
          <p className="text-slate-700">
            <span className="font-semibold text-slate-900">
              A public scoreboard, win or lose.
            </span>{" "}
            Every thesis gets a tracked hypothetical portfolio, visible
            whether it worked or not — including the losers.
          </p>
        </li>
      </ul>

      <div className="space-y-3 border-t border-slate-200 pt-8">
        <h2 className="text-xl font-semibold text-slate-900">Latest thesis</h2>
        <p className="text-base leading-relaxed text-slate-700">
          Thesis 13 asks whether a basket of Verizon, AT&amp;T and T-Mobile
          beats the S&amp;P 500 by at least 5 percentage points over 90 days,
          after the SpaceX spectrum deal. It is tracked in public, with
          results at 30, 60 and 90 days, whichever way they go.
        </p>
        <p className="text-base leading-relaxed text-slate-700">
          <a
            href={ONE_PAGE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-slate-900 underline underline-offset-2"
          >
            Read the one-page version
          </a>{" "}
          (about three minutes) or{" "}
          <a
            href={FULL_TEXT_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-slate-900 underline underline-offset-2"
          >
            the full text
          </a>
          .
        </p>
      </div>

      <div className="space-y-3 rounded-lg border border-slate-300 bg-slate-50 p-6">
        <h2 className="text-xl font-semibold text-slate-900">
          Read it? Tell us what you think
        </h2>
        <p className="text-base leading-relaxed text-slate-700">
          Two quick questions, about 30 seconds. No email needed. Your answers
          help us decide what Topicron does next.
        </p>
        <a
          href={SURVEY_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block rounded-md bg-slate-900 px-5 py-3 text-base font-semibold text-white hover:bg-slate-700"
        >
          Take the survey
        </a>
        <p className="text-xs leading-relaxed text-slate-500">
          The survey is hosted by Tally. See the Privacy Policy below.
        </p>
      </div>

      <div className="space-y-3 border-t border-slate-200 pt-8">
        <SubscribeForm />
      </div>

      <p className="text-xs leading-relaxed text-slate-500">
        Topicron is a research and educational publication, not a registered
        investment adviser. Nothing here is personalized investment advice or
        a recommendation to buy or sell any security.
      </p>

      <Link
        href="/privacy"
        className="text-xs text-slate-500 underline underline-offset-2 hover:text-slate-700"
      >
        Privacy Policy
      </Link>
    </main>
  );
}

// M0 landing page (docs/ROADMAP.md, M0 deliverable: "landing page + email
// list live"). Deliberately minimal, single hand-built page and endpoint —
// expected to be superseded by the real public topic/thesis pages in M3
// (docs/ROADMAP.md, M3: "Publication v1").

import { SubscribeForm } from "./subscribe-form";

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
        <SubscribeForm />
      </div>

      <p className="text-xs leading-relaxed text-slate-500">
        Topicron is a research and educational publication, not a registered
        investment adviser. Nothing here is personalized investment advice or
        a recommendation to buy or sell any security.
      </p>
    </main>
  );
}

// M0 landing page endpoint (docs/ROADMAP.md, M0 deliverable: "landing page
// + email list live"). Deliberately minimal — expected to be superseded by
// the real public pages/digest pipeline in M3 (docs/ROADMAP.md, M3).
//
// Resend's contact model: Audiences were renamed Segments, and contacts are
// now a global entity keyed by email — `audienceId` is deprecated in favor
// of `segments` (see node_modules/resend/dist/index.d.mts, checked against
// resend@6.18.0's actual shipped types before writing this call).

import { Resend } from "resend";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MAX_EMAIL_LENGTH = 254;

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: "Invalid request." }, { status: 400 });
  }

  if (typeof body !== "object" || body === null) {
    return Response.json({ error: "Invalid request." }, { status: 400 });
  }

  const { email, company } = body as { email?: unknown; company?: unknown };

  // Honeypot: this field is invisible to real users (see subscribe-form.tsx)
  // and never sent by a genuine submission. A bot that fills it out still
  // gets a normal-looking success response, so it has no signal to adapt to.
  if (typeof company === "string" && company.trim() !== "") {
    return Response.json({ ok: true });
  }

  if (
    typeof email !== "string" ||
    email.length === 0 ||
    email.length > MAX_EMAIL_LENGTH ||
    !EMAIL_REGEX.test(email)
  ) {
    return Response.json({ error: "Enter a valid email address." }, { status: 400 });
  }

  const segmentId = process.env.RESEND_SEGMENT_ID;
  if (!segmentId) {
    console.error(
      "Missing RESEND_SEGMENT_ID environment variable — see .env.local.example."
    );
    return Response.json(
      { error: "Subscription temporarily unavailable." },
      { status: 500 }
    );
  }

  const resend = new Resend(process.env.RESEND_API_KEY);

  const { error } = await resend.contacts.create({
    email: email.trim().toLowerCase(),
    segments: [{ id: segmentId }],
  });

  if (error) {
    // Resend's global contact model treats "already exists" as a normal,
    // non-error outcome for re-subscribing — but if it ever does come back
    // as an error, never show the raw provider error to the reader.
    console.error("Resend contacts.create failed:", error);
    return Response.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }

  return Response.json({ ok: true });
}

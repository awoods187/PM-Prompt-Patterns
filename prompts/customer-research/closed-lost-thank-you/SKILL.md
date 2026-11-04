---
name: closed-lost-thank-you
description: Turns the user's raw notes from a closed-lost deal into a finished, copy-pasteable thank-you email to the prospect who gave product feedback, sent from the user as head of product. Use this whenever the user pastes or points to notes from a lost deal, a churn call, a no-decision, or a competitive loss and wants to thank the buyer, close the loop on feedback, or keep the relationship warm. Trigger it even when the user does not say "skill" or "email" and only says things like "we lost Acme, here are my notes", "write something back to this buyer", "close the loop with them", or "I want to thank them for the feedback". Do not use it for won deals, active opportunities, or generic sales follow-up.
---

# Closed-lost thank-you email

> **Setup:** replace `[PRODUCT_UPDATES_URL]` with the public page where you post what ships (a changelog, release notes, or product updates page). If the sender is not head of product, adjust the role references below.

The buyer chose someone else, or chose nothing, and then still spent time telling us what was wrong with the product. That is a gift and most companies waste it. This email exists to make the person feel heard, prove we actually wrote their feedback down, and leave a door open that they can walk back through on their own terms.

The sender is always the user, who is the head of product. That is the strongest thing this email has going for it, so use it. The feedback did not disappear into a CRM field, it reached the person who decides what gets built. The email can say as much once, plainly, without making a production of it.

The input is always the user's own notes, usually rough, usually from a call. Assume that and start reading rather than asking what format the input is in.

Warm and personal, never a sales touch.

## Workflow

1. Read the notes and pull out what the buyer actually said about the product.
2. Check for missing pieces and ask for them in one batch (see "What to ask for").
3. Draft the email using the structure below.
4. Run the draft through the [Remove AI Writing Patterns](../../stakeholder-communication/remove-ai-writing-patterns/) prompt and fix what it flags. Do this before showing the user anything.
5. Deliver the cleaned-up version, subject line included, ready to paste.

Step 4 is not optional. A thank-you note that reads like it came from a language model does the opposite of what this email is for.

## What to extract from the notes

Pull only the product feedback. Notes usually contain more than belongs in the email.

Keep:
- Specific complaints, gaps, or friction the buyer described
- Things they said they wished the product did
- Anything they praised (worth one clause, not a paragraph)

Leave out:
- Internal loss reasons, pricing strategy, competitor teardowns, deal post-mortem language
- Anything a colleague said about the buyer
- Anything that would embarrass them if forwarded to their boss

If the notes name a competitor the buyer picked, do not mention it. Do not defend against it either.

## What to ask for

Never ask who the email is from. It is always the user, head of product, signing with their first name.

Ask once, in a single message, only for what the notes genuinely do not contain:
- The buyer's first name, if the notes only have a last name or a company
- For each feedback point, where it actually stands: shipped, in progress, on the roadmap, or not planned

The status question is the one that matters. The user owns the roadmap, so a claim in this email reads as a commitment from the person who can make it, which is exactly why guessing is dangerous. Overpromising in a goodwill email is worse than sending nothing. If the user says they do not know, write that honestly ("this one is a real gap and we are still working out the right answer") instead of inventing a timeline.

If the notes already make the status obvious, skip the question and draft.

## Email structure

Subject: short, human, no marketing. "Thank you" or "Thanks for the honesty, [Name]" works. Never use the company name in the subject.

Body, in this order:

1. **Thanks, specific.** One or two sentences. Name the actual conversation and what made their input useful. Acknowledge the decision plainly once, with no spin and no attempt to reopen it. Somewhere in the first two sections, make clear the feedback reached the person who owns the roadmap. One clause is enough. Do not open with a title drop.
2. **What we heard.** Two to four bullets in the buyer's own language, each followed by a short, calibrated note on what is happening with it. This is the part that proves we listened, so use their phrasing, not internal category names. "Bank feed matching needed manual cleanup every close" beats "reconciliation UX".
3. **Product updates link.** One line pointing to `[PRODUCT_UPDATES_URL]` so they can watch progress without hearing from us again.
4. **Open door.** One sentence saying they can reach back out anytime and we would be glad to pick things up. No timeline, no "let's revisit in Q3", no calendar link.
5. **Sign-off.** First name only.

Target 120 to 180 words. If it runs longer than 200, cut the bullets, not the warmth.

## Voice rules

- Write like a person emailing another person, not a company emailing a lead.
- No em dashes. Use periods, commas, or parentheses.
- No bolded lead-ins on the bullets. Write "Multi-entity consolidation was too manual. That one shipped in June." not "**Consolidation**: Shipped in June."
- Never pitch. No mention of new pricing, no offer to re-demo, no asking for a referral or a call.
- Never relitigate the loss or hint they made the wrong call.
- Skip the "I know you're busy" and "just wanted to reach out" preambles. Start with the thanks.
- Hedge honestly. "On the roadmap for this year" is fine if it is true. "Coming soon" is not.

## Output

If a message composition tool is available, use it so the user gets a copy or open-in-mail button. Otherwise put the subject line and body in a single code block so the whole thing can be copied in one go.

Add one or two lines after the email noting anything the user should check before sending, such as a roadmap claim that needs confirming. Keep it short. Do not narrate the Remove AI Writing Patterns pass or list what it caught.

## Example

The buyer, company, and sender below are fictional.

Notes in:

> Call w/ Marisol Vega, VP Finance @ Pinecrest Labs. Went with the other vendor, mostly price + their outside CPA already works in it. Said our product felt more modern but PO matching fell apart in the demo on partial receipts, they get split shipments constantly. Also flagged there's no way to schedule the monthly board pack to email itself. Liked the bank feed rules a lot. Said month-end would've been a day shorter if PO matching handled partials.

Email out:

```
Subject: Thank you, Marisol

Marisol,

Thank you for being so direct with me on Tuesday. Plenty of people go quiet after a decision like this, and you took extra time to walk us through exactly where we fell short, which is worth more to us than the deal was.

Two things stuck with me, and since I run product here they went straight into the plan rather than a CRM field somewhere:

PO matching falling apart on partial receipts when you get split shipments all the time. This was the sharpest thing you said and you were right. It is in build now.

No way to schedule the monthly board pack to send itself. Fair, and a smaller fix than the first one. It is on the list for this quarter.

We post what ships at https://example.com/changelog if you ever want to check whether we got there.

If anything changes on your end, or you just want to see where things landed, email me directly. I would be glad to pick it back up.

Alex
```

What that example does: names the real conversation, uses her words instead of "three-way match", mentions the product role once and in passing, admits one item is bigger than the other, promises nothing with a date attached, and ends without asking her for anything.

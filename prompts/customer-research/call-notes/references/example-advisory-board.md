# Product feedback call: Marcus Hale (Brightline Clinics), CFO Advisory Board

<!-- Fictional exemplar. People, company, product state, and links are invented. -->

## Where things stand

Marcus has been a customer for two years and joined the advisory board this spring. Brightline is growing from four clinics to nine through acquisitions closing over the next two quarters, and every acquired clinic arrives with its own chart of accounts and its own bookkeeper.

His hard constraint: acquired clinics keep their existing payroll provider for at least a year after close, because switching payroll mid-year is a compliance headache he won't take on. Anything we build for acquisitions has to work with three or four payroll providers at once, not assume one.

The two asks from his last session have both shipped and he reacted well to each one: entity templates, so a new clinic starts with Brightline's dimensions already set, and the consolidated cash flow statement. On the cash flow statement he said it's the first time he's handed his lender a consolidated report without rebuilding it in Excel first.

## What he liked

  - Entity templates. Setting up the last clinic took an afternoon instead of a week, and his controller didn't have to recreate the location and provider dimensions by hand.
  - Consolidated cash flow. He specifically called out that intercompany management fees eliminate cleanly now.
  - Location-level P&L. His clinic directors finally look at their own numbers, because the report is one click instead of an export.

## What felt weak or missing

  - Importing an acquired clinic's history is still painful. Their old chart of accounts has to be mapped to Brightline's line by line in a spreadsheet before import. Maps to [Import mapping improvements](https://linear.app/your-workspace/project/import-mapping-improvements-example).
  - Budget vs. actual can't roll up by region yet, only by entity or location. He needs regional rollups for the board once they're past six clinics.

## Feature wishlist

  - **Chart of accounts mapping on import.** His strongest ask. Upload the acquired clinic's trial balance, suggest mappings to the parent chart, and let the controller confirm. No Linear project exists yet; the closest is the import mapping project above, which covers vendor and customer fields only.
  - **Regional rollups in budget vs. actual.** Maps to [Budget reporting dimensions](https://linear.app/your-workspace/project/budget-reporting-dimensions-example) (backlog).
  - Multiple payroll providers per organization, one per entity. Partly supported today; the gap is a single combined payroll summary across providers.

One color note: his team tried a spreadsheet AI add-in for consolidation last quarter and dropped it after it double-counted an intercompany fee, so he's skeptical of AI features that touch eliminations.

## Next steps

Follow-up in three weeks, and he gave availability: Tuesdays or Thursdays before 11am Central. The last week of the month is out (close).

  1. Walk his controller through the import mapping beta with one acquired clinic's trial balance.
  2. Share the regional rollup design for feedback before it's built.

The third action item (confirming management fees eliminate in consolidation) was resolved live when we ran his own October numbers on the call.

Alex

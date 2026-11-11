# Product Strategy

## Available Prompts

- **[Meta-Prompt Designer](./meta-prompt-designer/)** - provider-optimized prompt
- **[Architect-Builder Pattern](./architect-builder-pattern/)** - provider-optimized prompt

### Product factory skills

These Claude Code skills are part of the [product factory](../../README.md#-product-factory). They use the [PRD template](../../templates/prd-template.md) and read workspace values from [`factory-config.example.md`](../../templates/factory-config.example.md).

- **[Write PRD](./write-prd/)** - 🔴 Advanced (Claude Code skill)
  - Gathers evidence, then interrogates the PM through five hard gates before drafting
  - Drafts a one-page PRD with stable requirement IDs and one-line pass/fail acceptance criteria
  - **Best for**: Turning a prioritized project into a spec engineering can build from

- **[Review PRD](./review-prd/)** - 🟡 Intermediate (Claude Code skill)
  - Structural checks plus six judgment lenses, including product invariants and buildability
  - Sets Spec ready only at zero errors
  - **Best for**: The gate between spec and build

- **[Specify Evals](./specify-evals/)** - 🔴 Advanced (Claude Code skill)
  - Eval cases in real user wording, including negative and near-miss cases
  - A deterministic grader per case where possible, draft cases for engineering's eval harness, and a launch gate linked from the PRD's AI module
  - **Best for**: AI features before review-prd

## Coming Soon

Planned prompts:
- Competitive analysis
- Market sizing estimation
- Product positioning statements
- Go-to-market planning
- OKR generation from strategy

See [TODO.md](../../TODO.md) for planned content.

Check back soon or [contribute](../../CONTRIBUTING.md)!

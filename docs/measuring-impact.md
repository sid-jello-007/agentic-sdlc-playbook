# Measuring impact: DORA plus SPACE

Leadership will ask one question: "Is it making us faster without making us worse?" DORA answers the delivery half; SPACE keeps the human half honest.

## DORA: delivery outcomes

| Metric | What it tells you | Expected effect of SDLC agents |
|---|---|---|
| Lead time for changes | Time from commit (or ticket ready) to production | Down, mainly from faster refinement and test writing |
| Deployment frequency | How often you ship | Up, if batch sizes shrink |
| Change failure rate | Share of changes causing incidents | Flat or down. **If it rises, stop and investigate** |
| Time to restore | How fast you recover | Flat; agents are not in the incident path at first |

Add one leading indicator that DORA misses: **time from spec approved to tickets ready**. It moves first, often within a sprint.

## SPACE: the human side

| Dimension | Example measure |
|---|---|
| Satisfaction | Short pulse: "Did the agent save you time this sprint?" |
| Performance | Share of agent drafts accepted with minor or no edits |
| Activity | Agent sessions per engineer (context only, never a target) |
| Communication | Refinement meeting time per ticket |
| Efficiency | Time spent writing tests per story point |

## Rules I use
1. **Baseline before rollout.** Two to four sprints of data first, or there is nothing to compare against.
2. **Pair every speed metric with a quality metric.** Lead time with change failure rate; drafts accepted with defects found later.
3. **Never target activity.** Rewarding "lines generated" or "prompts sent" gets you more of both and nothing else.
4. **Report ranges, not points.** Sprint to sprint noise is large; show trend and spread.

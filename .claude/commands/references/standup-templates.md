# Standup Templates Reference

Templates and patterns for the `/team:standup-notes` command.

## Standard Standup Format

```markdown
# Standup - YYYY-MM-DD

## Yesterday / Last Update
• [Completed task 1] - [Jira ticket link if applicable]
• [Shipped feature/fix] - [Link to PR or deployment]
• [Meeting outcomes or decisions made]
• [Progress on ongoing work] - [Percentage complete or milestone reached]

## Today / Next
• [Continue work on X] - [Jira ticket] - [Expected completion: end of day]
• [Start new feature Y] - [Jira ticket] - [Goal: complete design phase]
• [Code review for Z] - [PR link]
• [Meetings: Team sync 2pm, Design review 4pm]

## Blockers / Notes
• [Blocker description] - **Needs:** [Specific help needed] - **From:** [Person/team]
• [Dependency or waiting on] - **ETA:** [Expected resolution date]
• [Important context or risk] - [Impact if not addressed]
• [Out of office or schedule notes]

[Optional: Links to related docs, PRs, or Jira epics]
```

## Slack-Formatted Standup

```markdown
**🌅 Standup - Friday, Oct 11** | Posted 9:15 AM ET | @here

**✅ Since last update (Thu evening)**
• Merged PR #789 - New search filters now in production 🚀
• Closed JIRA-445 (the CSS rendering bug) - Fix deployed and verified
• Documented API changes in Confluence - [Link]
• Helped @alex debug the staging environment issue

**🎯 Today's focus**
• Finish user permissions refactor (JIRA-501) - aiming for code complete by EOD
• Deploy search performance improvements to prod (pending final QA approval)
• Kick off spike on GraphQL migration - research phase, doc by end of day

**🚧 Blockers**
• ⚠️ Need @product approval on permissions UX before I can finish JIRA-501
  - I've posted in #product-questions, following up in standup if no response by 11am

**📅 Schedule notes**
• OOO 2-3pm for doctor appointment
• Available for pairing this afternoon if anyone needs help!

---
React with 👀 when read | Reply in thread with questions
```

## Blocker Escalation Format

```markdown
## 🚨 CRITICAL BLOCKER

**Issue:** Production database read access for migration dry-run
**Blocked since:** Tuesday (3 days)
**Impact:**
- Cannot test migration on real data before production cutover
- Risk of data loss if migration fails in production
- Blocking sprint goal (migration scheduled for Monday)

**What I need:**
- Read-only credentials for production database replica
- Alternative: Sanitized production data dump in staging

**From:** @database-team (pinged @john and @maria)

**What I've tried:**
- Submitted access request via IT portal (Ticket #12345) - No response
- Asked in #database-help channel - Referred to IT portal
- DM'd @john yesterday - Said he'd check today

**Escalation:**
- If not resolved by EOD today, will need to reschedule Monday migration
- Requesting manager (@sarah) to escalate to database team lead
- Backup plan: Proceed with staging data only (higher risk)

**Next steps:**
- Following up with @john at 10am
- Will update this thread when resolved
- If unblocked, can complete testing over weekend to stay on schedule

---
@sarah @john - Please prioritize, this is blocking sprint delivery
```

## AI-Generated Standup from Git

```markdown
# Standup - 2025-10-11 (Auto-generated from Git commits)

## Yesterday (12 commits analyzed)
• **Feature work:** Implemented caching layer for API responses
  - Added Redis integration (3 commits)
  - Implemented cache invalidation logic (2 commits)
  - Added monitoring for cache hit rates (1 commit)
  - *Related tickets:* JIRA-567, JIRA-568

• **Bug fixes:** Resolved 3 production issues
  - Fixed null pointer exception in user service (JIRA-601)
  - Corrected timezone handling in reports (JIRA-615)
  - Patched memory leak in background job processor (JIRA-622)

• **Maintenance:** Updated dependencies and improved testing
  - Upgraded Node.js to v20 LTS (2 commits)
  - Added integration tests for payment flow (2 commits)
  - Refactored error handling in API gateway (1 commit)

## Today (From Jira: 3 tickets in progress)
• **JIRA-670:** Continue performance optimization work - Add database query caching
• **JIRA-681:** Review and merge teammate PRs (5 pending reviews)
• **JIRA-690:** Start user notification preferences UI - Design approved yesterday

## Blockers
• None currently

---
*Auto-generated from Git commits (24h) + Jira tickets. Reviewed and approved by human.*
```

## Data Collection Script

```bash
#!/bin/bash
# generate-standup.sh - AI-powered standup note generator

DATE=$(date +%Y-%m-%d)
USER=$(git config user.name)

echo "🤖 Generating standup note for $USER on $DATE..."

# 1. Collect Git commits
COMMITS=$(git log --author="$USER" --since="24 hours ago" \
  --pretty=format:"%h|%s|%cr" --no-merges)

# 2. Query Jira (requires jira CLI)
JIRA_DONE=$(jira issues list --assignee currentUser() \
  --jql "status CHANGED TO 'Done' DURING (-1d, now())" \
  --template json)

JIRA_PROGRESS=$(jira issues list --assignee currentUser() \
  --jql "status = 'In Progress'" \
  --template json)

# 3. Generate standup note
echo "## Yesterday"
echo "$COMMITS" | while IFS='|' read hash message time; do
    echo "• $message ($time)"
done

echo ""
echo "## Today"
echo "$JIRA_PROGRESS" | jq -r '.[] | "• \(.key): \(.fields.summary)"'
```

## System Architecture for AI Generation

```
┌─────────────────────────────────────────────────────────────┐
│ Data Collection Layer                                       │
├─────────────────────────────────────────────────────────────┤
│ • Git commits (last 24-48h)                                 │
│ • Jira ticket updates (status changes, comments)            │
│ • Obsidian vault changes (daily notes, task completions)    │
│ • Calendar events (meetings attended, upcoming)             │
│ • Slack activity (mentions, threads participated in)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ AI Analysis & Correlation Layer                             │
├─────────────────────────────────────────────────────────────┤
│ • Link commits to Jira tickets (extract ticket IDs)         │
│ • Group related commits (same feature/bug)                  │
│ • Extract business value from technical changes             │
│ • Identify blockers from patterns (repeated attempts)       │
│ • Summarize meeting notes → extract action items            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Generation & Formatting Layer                               │
├─────────────────────────────────────────────────────────────┤
│ • Generate "Yesterday" from commits + completed tickets     │
│ • Generate "Today" from in-progress tickets + calendar      │
│ • Flag potential blockers from context clues                │
│ • Format for target platform (Slack/Discord/Email)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Human Review & Enhancement Layer                            │
├─────────────────────────────────────────────────────────────┤
│ • Present draft for review                                  │
│ • Human adds context AI cannot infer                        │
│ • Adjust priorities based on team needs                     │
│ • Approve and post to team channel                          │
└─────────────────────────────────────────────────────────────┘
```

## Async Standup Patterns

### Written-Only (No Sync Meeting)

Post daily in #standup-team-name Slack channel at consistent time.

### Thread-Based

- Post standup as Slack thread parent message
- Teammates reply in thread with questions or offers to help
- Use emoji reactions: 👀 = read, ✅ = noted, 🤝 = I can help

### Video Async

- Record 2-3 minute Loom video walking through work
- Post video link with text summary
- Useful for demoing UI work, explaining complex issues

### Rolling 24-Hour

- Post update anytime within 24h window
- Accommodates distributed teams across timezones
- Weekly summary thread consolidates key updates

## Follow-Up Tracking

```markdown
## Follow-Up Tasks (Auto-generated from standup)
- [ ] Follow up with @infra-team on staging access (from blocker) - Due: Today EOD
- [ ] Review PR #789 feedback from @teammate (from yesterday's post) - Due: Tomorrow
- [ ] Document deployment process (from today's plan) - Due: End of week
- [ ] Check in on JIRA-456 migration (from today's priority) - Due: Tomorrow standup
```

## Weekly Retrospective

```markdown
# Review week of standup notes
Patterns observed:
• ✅ Completed all 5 sprint stories
• ⚠️ Database blocker cost 1.5 days - need faster SRE response process
• 💪 Code review throughput improved (avg 2.5 reviews/day vs 1.5 last week)
• 🎯 Pairing sessions very productive (3 this week) - schedule more next sprint

Action items:
• Talk to @sre-lead about expedited access request process
• Continue pairing schedule (blocking 2hrs/week)
• Next week: Focus on rate limiting implementation and technical debt
```

## Priority-Based Planning

```
1. Urgent blockers for others (unblock teammates first)
2. Sprint/iteration commitments (tickets in current sprint)
3. High-priority bugs or production issues
4. Feature work in progress (continue momentum)
5. Code reviews and team support
6. New work from backlog (if capacity available)
```

## Best Practices Checklist

**Formatting:**
- [ ] Use bullet points for scanability
- [ ] Include links to tickets, PRs, docs
- [ ] Bold blockers and key information
- [ ] Add time estimates where relevant
- [ ] Keep each bullet 1-2 lines max

**Content:**
- [ ] Focus on delivered value, not just activity
- [ ] Include impact when known
- [ ] Connect to team/sprint goals
- [ ] Be specific about timeline and scope

**Async Communication:**
- [ ] Post at consistent time daily
- [ ] Include enough context for all timezones
- [ ] Make blockers actionable
- [ ] Offer help when you see blockers you can resolve

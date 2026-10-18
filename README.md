# Conways Game of Life using Antigravity
Generate Conway's Game of Life using AI-Assisted Coding

# Links
- [Real Python - Live AI Assisted Coding Repository](https://github.com/realpython/live-ai-assisted-coding)
- [You Tube - Conways Game of Life Explanation](https://youtu.be/484FWxvO-Ro?si=lD4WLgAttiOk1QwG)
- 

# Conway's Game of Life Rules 
1. Alive cells die if they have fewer than two (underpopulation) or more than three living neighbors (overpopulation).
2. Alive cells stay alive if they have two or three living neighbors.
3. Dead cells with exactly three living neighbors become alive (reproduction).

# Strategy
* Agreed on the aims and the definition of done before any code was written
* Asked the AI agent to research the tricky bits and draft a plan, and then had a second model review that plan

# Setup
## Initial
### Antigravity CLI
- curl -fsSL https://antigravity.google/cli/install.sh | bash
- echo 'export PATH="/Users/vrbabu/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
- agy --version
NOTE :  Antigravity CLI updates itself in place whenever a newer release is available. But you can trigger that manually at any time with agy update.
- To authenticate : agy
- To get available models : agy models
- Set model from list : agy --model "Gemini 3.8 Flash (High)"
### Useful commands
- Setting reasoning effort directly: agy --effort high
- Non-interactive / Print mode : agy -p "Explain the Game of Life rules" --model gemini-3.8-flash-high
- The agent might autonomously write its findings to an artifact. Artifacts are files saved alongside your conversations that serve as a structured record of the agent’s plans, execution results, and summaries for your review. You can reveal them in the artifact review panel by pressing Ctrl+R or using the /artifact slash command at any time.
<br> Note: If the agent doesn’t create one automatically, then you can explicitly prompt it to formalize its findings into an artifact for you to review.
- Implement the refactor you proposed and check if the code runs correctly.
- Resume a Past Conversation : agy --conversation=2aac6e9d-f723-4361-8b69-da94c2b6d89e (or -c)
- agy -p "Summarize the staged changes in one line for a commit message."

### Useful / slash commands
- Check your remaining allowance : /usage or /quota
- Prefix a prompt with /grill-me, and the agent interviews you with clarifying questions before it writes a single line, which suits fuzzy, underspecified tasks. Prefix it with /goal, and the agent runs straight through to completion without the intermediate approvals 
- /planning when a task sits between those extremes. The agent works out an approach before it starts, which suits deep research, complex multi-step work, or collaborative sessions where you want to see the shape of the plan before code lands.
- /fork command splits the current conversation so you can explore an alternative approach without losing your original thread. Meanwhile, /rewind rolls the history back to an earlier message when a session drifts off course.
- 

### Useful Prompts
- What does this project do? Give a concise high-level summary.
- Review @transactions.py for correctness and code-quality problems,
  and check it against this project's conventions. Be specific about
  any bugs.
- Use subagents : Add JSON, Markdown, and HTML export formats alongside the
  existing text report. Treat each as an independent job and
  spin up a subagent per format, each in its own formats
  module mirroring the format_report() signature. Then wire
  them into @cli.py behind a --format option and run the CLI
  once per format to verify.

### Setting House Rule for agents
Antigravity CLI reads an AGENTS.md file from your project root, the same way Gemini CLI reads GEMINI.md. The sample project ships one that spells out a few house rules: See AGENTS.md
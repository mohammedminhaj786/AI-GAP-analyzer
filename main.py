import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.align import Align
from rich.layout import Layout
from rich import print as rprint

# Internal modules
from resume_parser import extract_text, extract_skills
from github_analyzer import analyze_github, calculate_github_score
from analyzer import get_match_results, get_recommendations
from job_roles_data import get_job_roles, get_skills_for_role

console = Console()

def show_welcome():
    console.clear()
    welcome_text = """
    [bold cyan]AI OPPORTUNITY GAP ANALYZER[/bold cyan]
    [italic white]Building the bridge between your skills and industry expectations.[/italic white]
    """
    console.print(Panel(Align.center(welcome_text), border_style="blue"))

def run_analysis():
    show_welcome()
    
    # 1. Job Role Selection
    roles = get_job_roles()
    console.print("\n[bold yellow]Step 1: Select Target Profile[/bold yellow]")
    for i, role in enumerate(roles):
        console.print(f"  {i+1}. {role}")
    
    choice = IntPrompt.ask("\nSelect role number", choices=[str(i+1) for i in range(len(roles))])
    selected_role = roles[choice-1]
    job_skills = get_skills_for_role(selected_role)
    
    # 2. Resume Input
    console.print("\n[bold yellow]Step 2: Provide Resume[/bold yellow]")
    resume_path = Prompt.ask("Enter path to your resume (.pdf, .docx, .txt)", default="sample_resume.txt")
    
    # 3. GitHub Input
    console.print("\n[bold yellow]Step 3: GitHub Activity (Optional)[/bold yellow]")
    gh_username = Prompt.ask("Enter GitHub username (Press Enter to skip)")
    
    console.print("\n" + "="*50)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # Task 1: Resume Analysis
        progress.add_task(description="Parsing Resume Content...", total=None)
        resume_text = extract_text(resume_path)
        user_skills = extract_skills(resume_text)
        
        # Task 2: GitHub Analysis
        gh_data = None
        gh_score = 0
        if gh_username:
            progress.add_task(description="Evaluating GitHub Contributions...", total=None)
            gh_data = analyze_github(gh_username)
            gh_score = calculate_github_score(gh_data)
            
        # Task 3: Matching
        progress.add_task(description="Identifying Knowledge Gaps...", total=None)
        matched, missing, match_score = get_match_results(user_skills, job_skills)
        
        # Task 4: Recommendations
        progress.add_task(description="Generating Recommendations...", total=None)
        recommendations = get_recommendations(missing, gh_score)

    # --- Display Results ---
    console.print("\n" + "="*50)
    console.print(Align.center(f"[bold green]ANALYSIS COMPLETE FOR: {selected_role.upper()}[/bold green]"))
    console.print("="*50 + "\n")

    # Metrics Table
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Metric", style="dim")
    table.add_column("Score", justify="right")
    
    overall_readiness = (match_score * 0.7) + (gh_score * 0.3)
    
    table.add_row("Resume Match Score", f"{match_score:.1f}%")
    table.add_row("GitHub Activity Score", f"{gh_score:.1f}%")
    table.add_row("[bold]Overall Career Readiness[/bold]", f"[bold green]{overall_readiness:.1f}%[/bold green]")
    
    console.print(table)

    # Skills Comparison
    col1_text = "\n".join([f"[green]✔[/green] {s}" for s in matched]) if matched else "[dim]No matches found[/dim]"
    col2_text = "\n".join([f"[red]✘[/red] {s}" for s in missing]) if missing else "[green]Perfect match![/green]"
    
    skill_table = Table(show_header=True, header_style="bold yellow", box=None, expand=True)
    skill_table.add_column("Matched Skills", style="green")
    skill_table.add_column("Missing / Gap Skills", style="red")
    skill_table.add_row(col1_text, col2_text)
    
    console.print(Panel(skill_table, title="Skill Gap Identification", border_style="yellow"))

    # GitHub Insights
    if gh_data:
        gh_info = f"""
        [bold]Profile:[/bold] {gh_data['name']} ({gh_data['username']})
        [bold]Public Repos:[/bold] {gh_data['public_repos']} | [bold]Followers:[/bold] {gh_data['followers']} | [bold]Total Stars:[/bold] {gh_data['total_stars']}
        [bold]Primary Languages:[/bold] {', '.join(gh_data['top_languages'])}
        """
        console.print(Panel(gh_info, title="GitHub Activity Insights", border_style="cyan"))

    # Recommendations
    rec_panel = "\n".join([f"• {r}" for r in recommendations])
    console.print(Panel(rec_panel, title="[bold]Actionable Recommendations[/bold]", border_style="green"))

    console.print("\n[dim italic]Built with AI Opportunity Gap Analyzer Engine[/dim italic]")

if __name__ == "__main__":
    try:
        run_analysis()
    except KeyboardInterrupt:
        console.print("\n[bold red]Analysis cancelled by user.[/bold red]")
        sys.exit(0)
